"""
    @Time: 2018/7/11 19:04
    @Author: qingyaocui
"""
import re
import jieba
import json


def clean(s):
    return re.sub('\s+', ',', s)

def clean_str(s):
    return re.sub('[\'\"]', '', s)


def str_to_int(str):

    if str:
        try:
            num = int(str)
            return num
        except Exception as e:
            print("数字格式错误！")
            print(e)
            return None
    else:
        return None


def load_stopwords(stop_words_file):
    '''
    加载停用词表
    :param file:停用词词典文件
    :return: 停用词列表
    '''
    with open(stop_words_file, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
        return stopwords


def seg_list(sentence, isstop=False, stopwords=None):
    '''
    对文本进行分词，默认不加载停用词表
    :param sentence: 需要分词的文本
    :param isstop: 是否进行分词
    :param stopwords: 停用词列表（若要进行分词，则必须提供停用词列表）
    :return: 分词后的列表
    '''

    if sentence:
        words = jieba.lcut_for_search(sentence)
        results = []
        if isstop:
            if stopwords:
                l_stopwords = load_stopwords(stopwords)
                for word in words:
                    if word not in l_stopwords and word != ',':
                        results.append(word)
                return results
            else:
                print("找不到停用词列表！,未加载停用词")
        else:
            return words
    else:
        return None


def save_to_json(filename, word_dict):
    with open(filename, 'w') as f:
        json.dump(word_dict, f)

def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

