"""
    @Time: 2018/7/16 14:41
    @Author: qingyaocui
"""
from word_cut.cut import process
from word_cut.construct import build
from word_cut.statistics import statistics
def main():
    process()
    build()
    statistics()

if __name__ == '__main__':
    main()