"""
    @Time: 2018/7/15 14:26
    @Author: qingyaocui
"""
import os
# import numpy as np
import math
from utils.util import save_to_json, load_from_json
from multiprocessing import Pool

# 词典大小
dictionary_size = 52444
# 文档集总数
document_size = 2267
# 输出非稀疏tf_idf向量的目录
# tf_idf_weight_dir = './weight/tf_idf'
# 输出稀疏tf_idf向量的目录
tf_idf_weight_sparse_dir = './weight/sparse_tf_idf'
# 分词目录
cuts_dir = './data/cuts'
# 加载索引文件
indexing_dict = load_from_json('./data/indexing.json')
# 加载词典
word_dict = load_from_json('./data/dictionary_id.json')

# 这个构建词典的方式，是 词：整个文档集的频率 (感觉没什么用 就放在这里吧)
def build_word_dictionary(directory, out):
    '''
    构建词典
    :param directory:分词文件目录
    :param out: json格式的词典
    :return:
    '''
    word_dict = {}
    files = os.listdir(directory)
    for file in files:
        if os.path.isfile(directory + '/' + file):
            with open(directory + '/' + file, 'r', encoding='utf-8') as f:
                words = f.readline().split('/')
                for word in words:
                    if word in word_dict:
                        word_dict[word] += 1
                    else:
                        word_dict.setdefault(word, 1)

    save_to_json(filename=out, word_dict=word_dict)


# 这个构建词典的方式，是 词：id号 在构建向量的时候可以标识位置
def build_word_dictionary_id(directory, out):
    '''
    构建词典 键：word 值:序号
    :param directory: 分词文件目录
    :param out: txt格式的词典
    :return:
    '''
    word_dict = {}
    i = 1
    files = os.listdir(directory)
    for file in files:
        if os.path.isfile(directory + '/' + file):
            with open(directory + '/' + file, 'r', encoding='utf-8') as f:
                words = f.readline().split('/')
                for word in words:
                    if word not in word_dict:
                        word_dict.setdefault(word, i)
                        i += 1

    save_to_json(filename=out, word_dict=word_dict)


def indexing(word_dict, directory, out):
    '''
    构建倒排索引：{'word1':[d1,d3, ..., dn],'word2':[d2,d4, ..., dm], ...}
    :param word_dict: 词典
    :param directory: 分词结果文件目录
    :param out: indexing.json文件
    :return:
    '''
    files = os.listdir(directory)
    indexing_dict = {}
    i = 1
    l = len(word_dict)
    for word in word_dict:
        index_l = []
        for file in files:
            if os.path.isfile(directory + '/' + file):
                with open(directory + '/' + file, 'r', encoding='utf-8') as f:
                   if word in f.readline().split('/'):
                       index_l.append(int(file.split('_')[0]))

        print("完成%d" % (i) + '个词，共%d' % (l) + '个词')
        i += 1
        indexing_dict[word] = index_l

    save_to_json(filename=out, word_dict=indexing_dict)

def tf(file):
    '''
    计算每篇文档的词频
    :param file: 文档
    :return: 每个词的词频,字典格式
    '''
    document = {}
    with open(file, 'r', encoding='utf-8') as f:
        words = f.readline().split('/')
        l = len(words)
        for word in words:
            if word in document:
                document[word] += 1
            else:
                document.setdefault(word, 1)
    for word in document:
        document[word] /= l

    return document

def idf(word):
    '''
    计算idf：log(文档集总数，(包含该词的文档数+1)) +1的目的是为了避免0在坟墓
    :param word:词
    :return:每个词对应的idf值
    '''
    return math.log(document_size/(len(indexing_dict[word])+1))

def tf_idf(file_out):
    '''
    计算每篇文档的tf-idf值的向量
    :param file_out: 词典 file对应着输入的文档，out对应着输出tf_idf向量的文件
    :return:
    '''


    # 计算每篇文档的词频得到词频字典 tf_dict
    tf_dict = tf(file_out['file'])

    # 稀疏tf_idf， 计算tf_idf向量后 ---向文件写入---> 位置,值 (所有0都不记录)
    with open(file_out['out'], 'w', encoding='utf-8') as f:
        vec = ''
        for word in tf_dict:
            vec += '%d,%f'%(word_dict[word],idf(word)*tf_dict[word]) + ' '
        f.write(vec)
    # 不加稀疏处理, 跑的有点慢
    # 初始化tf_idf向量为全0向量
    # tf_idf_vec = np.zeros(shape=(1, dictionary_size), dtype=np.float)
    # for word in tf_dict:
    #
    #     tf_idf_vec[0, word_dict[word] - 1] = idf(word)*tf_dict[word]
    #
    # np.savetxt(file_out['out'], tf_idf_vec)


if __name__ == '__main__':
    '''
    整个统计流程分为三步:1.构建词典 2.构建倒排索引 3.计算tf_idf向量
    '''

    # step 1: 构建词典
    # build_word_dictionary(cuts_dir, './data/dictionary.json') 这个感觉没啥用
    build_word_dictionary_id(cuts_dir, './data/dictionary_id.json')

    # step 2: 构建倒排索引
    indexing(word_dict, './data/cuts/', './data/indexing.json')

    # step 3: 计算tf_idf向量，稀疏处理
    files = os.listdir(cuts_dir)
    files_outs = []
    for file in files:
        if os.path.isfile(cuts_dir + '/' + file):
            file_out = {
                'file':cuts_dir + '/' + file,
                'out':tf_idf_weight_sparse_dir + '/' + file.split('_')[0] + '-tf_idf.txt'
            }
            files_outs.append(file_out)
    pool = Pool(5)
    pool.map(tf_idf, files_outs)
