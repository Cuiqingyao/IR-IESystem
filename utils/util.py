"""
    @Time: 2018/7/11 19:04
    @Author: qingyaocui
"""
import re


def clean_str(str):
    return re.sub('[\'\"]', '', str)

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


