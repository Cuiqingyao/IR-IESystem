from django.shortcuts import render, HttpResponse
import jieba
import json
import math
import os
import pymysql
import re
# Create your views here.


def index(request):
    return render(request, 'index.html')

def search(request):

    keywords = request.GET.get('keywords', None)
    if keywords :
        if len(keywords.strip())==0:
            return render(request, 'index.html', {'isNone':True})
        else:

            words = jieba.lcut_for_search(keywords)

            isHave = False
            with open('./data/dictionary_id.json') as f:
                word_dict = json.load(f)
            for word in words:
                if word in word_dict:
                    isHave = True
                    break
            if isHave:
                with open('./data/indexing.json') as f:
                    indexing_dict = json.load(f)
                l = len(words)
                # 计算tf_idf
                user_query_tf_idf = {}
                user_query_tf = {}
                user_query_idf = {}
                for word in words:
                    if word in word_dict:
                        if word in user_query_tf:
                            user_query_tf[word] += 1
                        else:
                            user_query_tf.setdefault(word, 1)
                        # 计算idf
                        user_query_idf[word] = math.log(2267 / (len(indexing_dict[word]) + 1))
                if len(user_query_tf) != 0:
                    for word in user_query_tf:
                        user_query_tf[word] /= l
                    for word in user_query_tf:
                        user_query_tf_idf[word] = user_query_tf[word] * user_query_idf[word]
                    weight_dir = './weight/sparse_tf_idf'
                    # 计算query的模
                    sum1 = 0.0
                    for word in user_query_tf_idf:
                        sum1 += user_query_tf_idf[word]**2

                    query_mo = math.sqrt(sum1)

                    # 全文档集相似度
                    sim_ranking = {}

                    # 计算相似度
                    files = os.listdir(weight_dir)
                    for file in files:
                        if os.path.isfile(weight_dir + '/' + file):
                            with open(weight_dir + '/' + file, 'r', encoding='utf-8') as f:
                                # 加载文档向量
                                index_weight = f.readline().strip().split(' ')
                                # 计算文档向量的模
                                sum2 = 0.0
                                for item in index_weight:
                                    w = item.split(',')[1]
                                    sum2 += float(w)**2
                                doc_mo = math.sqrt(sum2)
                                fenmu = query_mo * doc_mo

                                # 计算余弦相似度的分子
                                fenzi = 0.0
                                for word in user_query_tf_idf:
                                    for item in index_weight:
                                        i = int(item.split(',')[0])
                                        w = float(item.split(',')[1])
                                        if word_dict[word] == i:
                                            fenzi += user_query_tf_idf[word] * float(w)

                                sim = fenzi/fenmu
                            sim_ranking[file.split('-')[0]] = sim
                            # print(sim)


                    # 相似度排序
                    results = sorted(sim_ranking.items(), key=lambda item:item[1], reverse=True)[0:30]
                    # results = [(id,sim),(id,sim),(id,sim)]
                    # print(results)
                    # 查询结果, 返回给前段 id, 招聘标题，job_url, 公司名称，薪水
                    data = []
                    conn = pymysql.connect(host='localhost',
                                           user='root',
                                           password='123',
                                           port=3306,
                                           db='jobs',
                                           charset='utf8',
                                           cursorclass=pymysql.cursors.DictCursor)
                    cursor = conn.cursor()
                    for result in results:
                        id = result[0]
                        sql = 'select job_id, job_title, job_url, com_name, com_loc_simple, salary from jobinfomation where job_id=%s'%(id)
                        cursor.execute(sql)
                        data_item = cursor.fetchone()
                        data_item['sim'] = result[1]
                        data.append(data_item)

                    return render(request, 'results.html', {'data':data})
                else:
                    return render(request, 'index.html', {'isHave':False})
            else:
                return render(request, 'index.html', {'isHave':False})
    else:
        return render(request, 'index.html', {'isNone': True})



def detail(request):

    job_id = request.GET.get('job_id', None)
    sql = "SELECT com_name,com_type,com_size,busi_type,com_info,com_loc_simple,com_loc_detail,job_title," + \
          "salary,num_of_recruits,academic_require,treatment,job_info,job_url,com_url FROM jobinfomation WHERE job_id=%s"%(job_id)
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123',
                           port=3306,
                           db='jobs',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    job_info = data['job_info']

    extraction = {
        "language": None,
        "framework": None,
        "platform": None,
        "major": None
    }
    extraction['language'] = set(
        re.findall('Python|python|C\+\+|c\+\+|C|c|JAVA|Java|java|Matlab|matlab|Objective-C|objctive-c', job_info, re.S))
    extraction['platform'] = set(
        re.findall('Linux|linux|windows|Windows|Unix|unix|Mac OS|MacOS|iOS|ios|Android|android', job_info, re.S))
    extraction['framework'] = set(re.findall(
        'TensorFlow|tensorflow|Tensorflow|PyTorch|pyTorch|pytorch|torch|caffe|opencv|openCV|OpenCV|Open-CV|mxnet|keras|Keras|scikit-learn|Django|django|cntk|CNTK',
        job_info, re.S))
    extraction['major'] = set(re.findall('计算机|软件工程|计算机科学|计算机技术|计算机视觉|图像处理|自然语言处理|模式识别|自动化|数学|光学', job_info, re.S))
    data['extration'] = extraction

    return render(request, 'detail.html', {'data':data})
