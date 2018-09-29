# coding:utf8
import json
import re
import shutil
import time

import requests
from bs4 import BeautifulSoup
from flask import (Flask, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)

import config
from exts import drow, exts, sub_query
from matplot import chart
from models import Score, Student, Subject, db
from sendemail import sendemail, parsermail, wechatInfo
from spider import getScore, spiderLogin, timeTable

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    # db.drop_all()
    db.create_all()


# 上下文管理器，保存登陆用户
@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}


# 钩子函数，每次响应执行前运行
@app.before_request
def my_before_request():
    id = session.get('id')
    name = session.get('name')
    if id:
        g.user = name


@app.route('/')
def login():
    return render_template('login.html', user=1)


# 登出
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 学生用户登陆
@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'GET':
        return render_template('login.html', user=1)
    else:
        try:
            id = request.form.get('id')
            password = str(request.form.get('password'))
            username = getScore(id, password)
            session['id'] = id
            session['name'] = username
            session['user'] = 'student'
            return redirect(url_for('student'))
        except:
            flash('', 'error')
            return render_template('login.html', user=1)


# 学生主界面
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        id = session.get('id')
        credit_list, time_list = drow(id)
        credit = []
        for c in credit_list:
            credit.append(c[2])
        chart(credit, time_list)
        return render_template('student.html')
    else:
        return render_template('student.html')


# 成绩查询
@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'GET':
        id = session.get('id')
        stu = Score.query.filter(Score.stu_id == id).all()
        credit = exts(stu)
        credit.append('all')
        credit.append('all')
        return render_template("score.html", classes=stu, credit=credit)
    else:
        id = session.get('id')
        year = request.form.get('year')
        term = request.form.get('term')
        if year == 'all' and term == 'all':
            return redirect(url_for('score'))
        else:
            credit, cla = sub_query(id, year, term)
        credit.append(year)
        credit.append(term)
        return render_template("score.html", classes=cla, credit=credit)


# 课程查询
@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    if request.method == 'GET':
        return render_template('student.html')
    else:
        return render_template('student.html')


# 邮箱推送
@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'GET':
        return render_template('sendemail.html')
    else:
        receive = request.form.get('email')
        id = session.get('id')
        name = session.get('name')
        if sendemail(id, receive, name):
            flash('', 'OK')
            return render_template('sendemail.html')
        else:
            flash('', 'error')
            return render_template('sendemail.html')


def xml_parser(text):
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    return dic


# 获取QRcode，生成二维码
@app.route('/QRlogin', methods=['GET', 'POST'])
def QRlogin():
    if request.method == 'GET':
        ctime = str(int(time.time() * 1000))
        qcode_url = "https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}".format(
            ctime)

        ret = requests.get(qcode_url)
        qcode = re.findall('uuid = "(.*)";', ret.text)[0]
        session['qcode'] = qcode
        return render_template('QRlogin.html', qcode=qcode)
    else:
        pass


# 检测是否扫码登陆
@app.route('/check_login')
def check_login():
    """
    发送GET请求检测是否已经扫码、登录
    https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=QbeUOBatKw==&tip=0&r=-1036255891&_=1525749595604
    :return:
    """
    response = {'code': 408}
    qcode = session.get('qcode')
    ctime = str(int(time.time() * 1000))
    check_url = "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-1036255891&_={1}".format(
        qcode, ctime)
    ret = requests.get(check_url)
    if "code=201" in ret.text:
        # 扫码成功
        src = re.findall("userAvatar = '(.*)';", ret.text)[0]
        response['code'] = 201
        response['src'] = src
    elif 'code=200' in ret.text:
        # 确认登录
        print("code=200~~~~~~~", ret.text)
        redirect_uri = re.findall('redirect_uri="(.*)";', ret.text)[0]

        # 向redirect_uri地址发送请求，获取凭证相关信息
        redirect_uri = redirect_uri + "&fun=new&version=v2"
        ticket_ret = requests.get(redirect_uri)
        ticket_dict = xml_parser(ticket_ret.text)
        session['ticket_dict'] = ticket_dict
        response['code'] = 200
    return jsonify(response)


# 扫码后执行,获取好友列表
@app.route('/index')
def index():
    ticket_dict = session.get('ticket_dict')
    init_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1039465096&lang=zh_CN&pass_ticket={0}".format(
        ticket_dict.get('pass_ticket'))

    data_dict = {
        "BaseRequest": {
            "DeviceID": "e750865687999321",
            "Sid": ticket_dict.get('wxsid'),
            "Uin": ticket_dict.get('wxuin'),
            "Skey": ticket_dict.get('skey'),
        }
    }

    init_ret = requests.post(
        url=init_url,
        json=data_dict
    )
    init_ret.encoding = 'utf-8'
    user_dict = init_ret.json()
    session['user_info'] = user_dict['User']
    session['SyncKey'] = user_dict['SyncKey']

    return render_template('index.html',user_dict=user_dict['User'])


# 发送成绩信息给文件传输助手
@app.route('/send_msg',methods=['GET','POST'])
def send_msg():
    if request.method=='GET':
        user = session.get('user_info')
        return render_template('index.html', user_dict=user)
    else:
        try:
            data =request.form
            year = data.get('year')
            term = data.get('term')
            id = session.get('id')
            content = wechatInfo(id, year, term)
            user = session['user_info']['UserName']
            ticket_dict = session.get('ticket_dict')
            ctime= str(int(time.time()*1000))
            send_url ='https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket={0}'.format(ticket_dict.get('pass_ticket'))

            send_dict = {
                'BaseRequest':{
                    'DeviceID': "e750865687999321",
                    "Sid": ticket_dict.get('wxsid'),
                    "Uin": ticket_dict.get('wxuin'),
                    "Skey": ticket_dict.get('skey'),
                },
                'Msg':{'ClientMsgId':ctime,
                    'LocalID':ctime,
                    'FromUserName':user,
                    'ToUserName':'filehelper',
                        'Type':1,
                        'Content':content,
                },
                'Scene':0,}

            requests.post(
                url=send_url,
                data=json.dumps(send_dict,ensure_ascii=False).encode('utf-8'),
            )
            flash('', 'OK')
        except:
            flash('', 'error')
        return redirect(url_for('send_msg'))

if __name__ == "__main__":
    app.run()
