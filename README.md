# 项目名称：模拟教务系统(web)  
[![](https://travis-ci.org/Alamofire/Alamofire.svg?branch=master)](https://travis-ci.org/Alamofire/Alamofire)![](https://img.shields.io/badge/python-2.7-orange.svg)![](https://img.shields.io/badge/github-@Edusystem-blue.svg?colorA=abcdef)![](https://img.shields.io/badge/platform-flask-lightgrey.svg)![](https://img.shields.io/badge/HBNU-jwxt-red.svg)![](https://travis-ci.org/Alamofire/Alamofire.svg?branch=master)

### 开发人员

---

项目开发：[Xiang Jinhu](https://github.com/chirsxjh)，[Chen Wei](https://github.com/Cris0525)，[Fu Tongyong](https://github.com/CANYOUFINDIT)

项目指导：[Li Xipeng](https://github.com/hahaps)

### 需求概述
---
这个项目实现了湖北师范大学正方教务系统的一套API： 包括模拟登陆，个人信息查询，课表获取，成绩查询，成绩邮箱/微信推送等等。随着API的不断完善与扩充，可以很方便为本校学生作为后台服务。 
用户只需输入个人学号密码即可获取个人成绩与课程信息，并且在系统首页能够以折线图的形式来展示学生个人的平均绩点走向，同时能够将个人成绩以微信推送和邮件发送的方式提供给用户，大大增加了本校学生查询个人成绩相关信息的便利性。

### 项目运行环境及技术依赖
---
语言：`python2.7`

运行环境：`ubuntu16.04`

### 技术依赖 
---
Web 应用框架：`Flask`

数据库：`MySQL`

ORM框架：`flask-sqlalchemy`

数据库迁移：`flask-migrate`, `flask-script`

爬虫相关库：`request`, `BeautifulSoup`

前端JS：`pyecharts`, `bootstrap`

邮件发送：`smtplib`

微信发送：`itchat`


### 项目目录
---
```
|-- README.md
|-- __init__.py
|-- config.py
|-- crypto_rsa
|   |-- RSAJS.py
|   |-- __init__.py
|   |-- base64.py
|   `-- safeInput.py
|-- exts.py
|-- manage.py
|-- matplot.py
|-- migrations
|-- models.py
|-- requirements.txt
|-- sendemail.py
|-- spider.py
|-- static
|   |-- css
|   |   |-- admin.css
|   |   |-- amazeui.min.css
|   |   `-- app.css
|   |-- fonts
|   |   |-- FontAwesome.otf
|   |   |-- fontawesome-webfont.eot
|   |   |-- fontawesome-webfont.ttf
|   |   |-- fontawesome-webfont.woff
|   |   `-- fontawesome-webfont.woff2
|   |-- images
|   |   |-- app-icon72x72@2x.png
|   |   |-- favicon.png
|   |   `-- logo.png
|   `-- js
|       |-- amazeui.min.js
|       |-- app.js
|       |-- echarts.min.js
|       |-- iscroll.js
|       `-- jquery.min.js
|-- templates
|   |-- QRlogin.html
|   |-- base.html
|   |-- index.html
|   |-- login.html
|   |-- score.html
|   |-- sendchat.html
|   |-- sendemail.html
|   |-- student.html
|   `-- timetable.html
`-- view.py
```

### 项目功能描述
---
* 学生用户各学期的平均成绩点折线图直观展示
>通过shutil将爬虫爬取存入数据库的平均绩点绘制成折线图展示
* 支持学生用户进行各学期的成绩信息查询，并且将合格，不合格以不同颜色区分开来
> 通过教务系统个人信息页面，抓取，个人信息，并持久化保存到数据库中，在前端界面做以展示。
* 支持学生用户进行各学期的课程信息查询

> 通过教务系统课表信息页面，抓取，课程信息，并持久化保存到数据库中，在前端界面做以展示。
* 支持将学生的成绩信息通过填写的邮箱进行推送
> 根据smtp协议实现成绩邮箱推送。
* 支持将学生的成绩信息通过移动端微信扫描二维码实现微信推送

> 通过itchat实现微信推送


### 项目数据库设计
---
 数据库ER图
![](http://a1.qpic.cn/psb?/V13uRwZ41wvDRP/4BKeiFjdQkOUYkBlA6iIoxf3BQUW1ZzvSupBg0dS6u0!/c/dGwBAAAAAAAA&ek=1&kp=1&pt=0&bo=JQNGAgAAAAADF1A!&tl=1&vuin=2018982763&tm=1539486000&sce=60-2-2&rf=0-0)

### 注意事项
---
通过本命令安装有关依赖库：
`pip install -r requirements.txt`

使用前需要修改的内容：
- `config.py`中的数据库信息
- `matplot.py`第20，21，24，40行的路径
- `spider.py`第34，254行的路径
- `sendmail.py`中发件人信息

使用`flask-script`配合`flask-migrate`进行版本库迁移，第一次使用时在命令行中使用`python manage.py db init`进行初始化，建立数据库迁移相关的文件和文件夹，之后每次需要迁移依次使用`python manage.py db migrate`和`python manage.py db upgrade`即可

**项目启动：`python view.py`**



### 更新链接
---
[github](https://github.com/WeAreHus/StudyRecord/tree/master/day-2018-08-26/new_system)





### 运行效果部分展示
---
![登陆](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/hJrCWjQVdkUoQv5K1f4uOytz9v2.xCL5dxnUujJh.fI!/b/dDYBAAAAAAAA&ek=1&kp=1&pt=0&bo=MAf4AjAH.AIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=50-1-1&rf=viewer_311)
![主页](http://a4.qpic.cn/psb?/V13uRwZ427WzZu/vl8wWVEKe6.07FzcwLJGH5pbYlP3xLU.MCyrKURuZ9s!/b/dDcBAAAAAAAA&ek=1&kp=1&pt=0&bo=HgfzAh4H8wIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=60-4-3&rf=viewer_311)
![成绩](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/p3f6KdfDqGBteLoyBnsmjWi6XAHwiNAWopTiqzsMu7M!/b/dFYAAAAAAAAA&ek=1&kp=1&pt=0&bo=Dgf8Ag4H*AIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=50-1-1&rf=viewer_311)
![课程](http://a1.qpic.cn/psb?/V13uRwZ427WzZu/Mymr7HYjbUpPEdMZGnNtcvc4fXqMMLsORw3N0Qd1bVs!/b/dDQBAAAAAAAA&ek=1&kp=1&pt=0&bo=FQf1AhUH9QIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=50-1-1&rf=viewer_311)
