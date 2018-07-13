"""
    @Time: 2018/7/11 16:59
    @Author: qingyaocui
"""
'''
学历简写与中文对照
'''
ACADEMIC = {
    'bk' : '本科',
    'ss' : '硕士',
    'bs' : '博士'
}


'''
不同学历的招聘信息条目：
bk -> 本科 : num -> 默认爬取20页 每页50条 共1000条
ss -> 硕士 : num -> 默认爬取20页 每页50条 共1000条
bs -> 博士 : num -> 默认爬取8页 每页50条 共400条
总计：10400条招聘信息
'''
DATA_CAPACITY = {
    'bk' : 20,
    'ss' : 20,
    'bs' : 8
}


'''
不同学历的招聘信息：
bk -> 本科 : url -> 本科学历的招聘首页
ss -> 硕士 : url -> 硕士学历的招聘首页
bs -> 博士 : url -> 博士学历的招聘首页
'''


ACADEMIC_REQUIRE_DICT = {'bk' : 'https://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=04&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
                         'ss' : 'https://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=05&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
                         'bs' : 'https://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=06&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='}


# 请求头信息，伪装成浏览器，放置被拒绝访问
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


# 匹配招聘条目，抽取的字段为：招聘url，职位名称，公司名称，公司url，工作地点-略，薪资，发布时间
JOB_PATTERN = '<div class="el">.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?'+\
              '<span class="t2".*?title="(.*?)".*?href="(.*?)">.*?</a></span>.*?'+\
              '<span class="t3">(.*?)</span>.*?'+\
              '<span class="t4">(.*?)</span>.*?'+\
              '<span class="t5">(.*?)</span>.*?'+\
              '</div>'




