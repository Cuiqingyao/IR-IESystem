"""
    @Time: 2018/7/16 14:44
    @Author: qingyaocui
"""
import os
from utils.util import save_to_json, load_from_json

cuts_dir = './data/cuts'

# 这个构建词典的方式，是 词：id号 在构建向量的时候可以标识位置
def build_word_dictionary_id(directory, out):
    '''
    构建词典 键：word 值:序号
    :param directory: 分词文件目录
    :param out: txt格式的词典
    :return:
    '''
    print("构建词典 键：word 值:序号")
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

    save_to_json(filename=out, data=word_dict)
    print("词典构建完成！")

def indexing(word_dict, directory, out):
    '''
    构建倒排索引：{'word1':[d1,d3, ..., dn],'word2':[d2,d4, ..., dm], ...}
    :param word_dict: 词典
    :param directory: 分词结果文件目录
    :param out: indexing.json文件
    :return:
    '''
    print("构建倒排索引：{'word1':[d1,d3, ..., dn],'word2':[d2,d4, ..., dm], ...}")
    files = os.listdir(directory)
    indexing_dict = {}
    for word in word_dict:
        indexing_dict[word] = []
    i = 1
    l = len(word_dict)
    for file in files:
        if os.path.isfile(directory + '/' + file):
            with open(directory + '/' + file, 'r', encoding='utf-8') as f:
                # 对词表进行去重
                words = set(f.readline().split('/'))
                for word in words:
                    indexing_dict[word].append(int(file.split('_')[0]))

    save_to_json(filename=out, data=indexing_dict)
    print("倒排索引文件构建完成！")

def build():
    build_word_dictionary_id(cuts_dir, './data/dictionary_id.json')
    word_dict = load_from_json('./data/dictionary_id.json')
    indexing(word_dict, cuts_dir, './data/indexing.json')
