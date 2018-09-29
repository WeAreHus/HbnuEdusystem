# -*-coding:utf-8 -*-
import json
import sys
import time

import requests
from bs4 import BeautifulSoup

from crypto_rsa.base64 import Base64 as pB64
from crypto_rsa.RSAJS import RSAKey
from crypto_rsa.safeInput import safeInput
from models import Score, Student, Subject, db

reload(sys)
sys.setdefaultencoding("utf-8")

# 时间戳
ctime = int(time.time() * 1000)
post_url = 'http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?time={0}'.format(
    ctime)
s = requests.Session()
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '471',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'jwxt.hbnu.edu.cn',
    'Origin': 'http://jwxt.hbnu.edu.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t={0}'.format(ctime),
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

header1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'jwxt.hbnu.edu.cn',
    'Referer': 'http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t={0}'.format(ctime),
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


# 密码加密
def getEnPassword(string, exponent, modulus):
    b64 = pB64()
    exponent = b64.b64_to_hex(exponent)
    modulus = b64.b64_to_hex(modulus)
    rsa = RSAKey()
    rsa.setPublic(modulus, exponent)
    crypto_t = rsa.encrypt(string)
    return b64.hex_to_b64(crypto_t)


# 模拟登陆
def spiderLogin(yhm, passwd):
    r = s.get(post_url, headers=header1)
    r.encoding = 'utf-8'
    doc = r.text
    soup = BeautifulSoup(doc, 'html.parser')
    # 解析获取csrftoken值
    csrftoken = str(soup.find('input', id="csrftoken")['value'])
    publicKeyUrl = "http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time={}&_={}".format(
        ctime, ctime-10)
    modExp = s.get(publicKeyUrl).json()
    get_mm = getEnPassword(passwd, modExp["exponent"], modExp["modulus"])
    postdata = [
        ('csrftoken', csrftoken),
        ('yhm', yhm),
        ('mm', get_mm),
        ('mm', get_mm)
    ]
    s.post(post_url, data=postdata, headers=header)
    score_url = 'http://jwxt.hbnu.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={}'.format(
        yhm)
    r = s.get(score_url)
    r.encoding = 'utf8'
    doc = r.content
    soup = BeautifulSoup(doc, 'html.parser')
    info = soup.find_all('p', class_='form-control-static')
    # 存储学生信息
    lists = []
    for text in info:
        text = text.getText().strip()
        lists.append(text)
    # 查询是否已存在该用户, 若存在则更新数据，不存在则写入
    user = Student.query.filter(Student.id == yhm).first()
    if user:
        user.grade = lists[10]
        user.collage = lists[11]
        user.major = lists[12]
        user.class_ = lists[14]
        db.session.commit()
    else:
        stu = Student(lists[0], lists[1], lists[4], lists[7],
                      lists[10], lists[11], lists[12], lists[14])
        db.session.add(stu)
        db.session.commit()
    return lists[1]


# 将成绩存入数据库
def addScoreDB(key):
    if key.has_key('jd') == False:
        key['jd'] = None
    school_year = str(key['xnmmc'])
    school_term = int(key['xqmmc'])
    class_name = str(key['kcmc'])
    class_code = str(key['kch_id'])
    if len(class_code) > 30:
        class_code = ""
    credit = float(key['xf'])
    class_category = str(key['kcxzmc'])
    test_category = str(key['ksxz'])
    cjsfzf = str(key['cjsfzf'])
    score = float(key['cj'])
    GPA = float(key['jd'])
    class_mark = str(key['kcbj'])
    class_ownership = str(key['kkbmmc'])
    stu_id = float(key['xh_id'])
    #print school_year, school_term, class_name, class_code, credit, class_category, test_category, cjsfzf, score, GPA, class_mark, class_ownership, stu_id
    sco = Score.query.filter(Score.school_year == school_year).filter(Score.school_term == school_term).filter(
        Score.class_name == class_name).filter(Score.test_category == test_category).filter(Score.stu_id == stu_id).first()
    if sco:
        sco.credit = credit
        sco.class_category = class_category
        sco.test_category = test_category
        sco.cjsfzf = cjsfzf
        sco.score = score
        sco.GPA = GPA
        sco.class_mark = class_mark
        sco.class_ownership = class_ownership
        db.session.commit()
    else:
        sco = Score(school_year, school_term, class_name, class_code, credit, class_category,
                    test_category, cjsfzf, score, GPA, class_mark, class_ownership, stu_id)
        db.session.add(sco)
        db.session.commit()


# 获取成绩
def getScore(yhm, passwd):
    name = spiderLogin(yhm, passwd)
    formdata = {
        'xnm': '',
        'xqm': '',
        '_search': 'false',
        'nd': ctime,
        'queryModel.showCount': '100',
        'queryModel.currentPage': '1',
        'queryModel.sortName': '',
        'queryModel.sortOrder': 'asc',
        'time': '0',
    }
    score_url = 'http://jwxt.hbnu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
    r = s.post(score_url, data=formdata)
    r.encoding = 'utf8'
    doc = r.content
    # 将字符串转为字典
    doc = json.loads(doc)
    for key in doc['items']:
        addScoreDB(key)
    return name

# 将课程表添加进数据库
def addTimetableDB(key, yhm, xnm, xqm):
    class_name = key['kcmc']
    day = key['xqjmc']
    time = key['jc']
    week = key['zcd']
    classroom = key['cdmc']
    teacher = key['xm']
    department = key['xqmc']
    print key['kcmc'], key['xqjmc'], key['jc'], key['zcd'], key['cdmc'], key['xm'], key['xqmc']
    sub = Subject.query.filter(Subject.school_year == xnm).filter(Subject.school_term == xqm).filter(
        Subject.class_name == class_name).filter(Subject.stu_id == yhm).first()
    if sub:
        sub.day = day
        sub.time = time
        sub.week = week
        sub.classroom = classroom
        sub.teacher = teacher
        sub.department = department
        db.session.commit()
    else:
        sub = Subject(xnm, xqm, class_name, day, time, week,
                      classroom, teacher, department, yhm)
        db.session.add(sub)
        db.session.commit()


# 获取课程表
def timeTable(yhm, passwd, xnm, xqm):
    spiderLogin(yhm, passwd)
    if xqm == "1":
        xq = "3"
    elif xqm == "2":
        xq = "12"
    table_url = "http://jwxt.hbnu.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"
    formdata = {
        'xnm': xnm,
        'xqm': xq
    }
    tables = s.post(table_url, data=formdata)
    tables.encoding = 'utf8'
    doc = tables.content
    table = json.loads(doc)
    for key in table['kbList']:
        addTimetableDB(key, yhm, xnm, xqm)


if __name__ == "__main__":
    id = 2016115020429
    passwd = 'qwer1234'
    getScore(id, passwd)
    #timeTable(id, passwd, '2017', '2')