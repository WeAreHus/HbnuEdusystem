# 项目名称：模拟教务系统(web)


### 开发人员
---

项目开发：[Xiang Jinhu](https://github.com/chirsxjh)，[Chen Wei](https://github.com/Cris0525)，[Fu Tongyong](https://github.com/CANYOUFINDIT)

项目指导：[Li Xipeng](https://github.com/hahaps)

### 需求概述
---
这个项目实现了湖北师范大学学生进行教务系统正方教务系统的一套API： 包括模拟登陆，个人信息查询，课表获取，成绩查询等等。随着API的不断完善于扩充，可以很方便的作为后台服务。 
用户只需个人学号密码即可获取个人成绩与课程信息，无须验证码登录，并且在系统首页能够以折线图的形式来展示学生个人的平均绩点走向，同时能够将个人成绩以微信推送与邮件发送给用户，大大增加了学生查询成绩信息的便利性。

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

验证码识别：[ZFCheckCode](https://github.com/sctpan/CheckCodeRecognition)

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
|   |-- RSAJS.pyc
|   |-- __init__.py
|   |-- __init__.pyc
|   |-- base64.py
|   |-- base64.pyc
|   |-- safeInput.py
|   `-- safeInput.pyc
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
|-- test.html
`-- view.py
```

### 项目功能描述
---
* 各学期平均成绩点折线图展示
>通过shutil将爬虫爬取存入数据库的平均绩点绘制成折线图展示
* 成绩查询
> 通过教务系统个人信息页面，抓取，个人信息，并持久化保存到数据库中，在前端界面做以展示。
* 课表查询
> 通过教务系统课表信息页面，抓取，课程信息，并持久化保存到数据库中，在前端界面做以展示。
* 成绩邮箱推送
> 根据smtp协议实现成绩邮箱推送。
* 成绩微信推送


### 项目数据库设计
---
 数据库ER图
![物理模型](https://camo.githubusercontent.com/f6dc506aea3b1f1ad15ceea1d53a1e29e2a90f91/687474703a2f2f61332e717069632e636e2f7073623f2f5631337552775a343237577a5a752f6c6431796f444a39566e37384f7674304342456277654266676a2a4d54716433393349744e675a386e6b6f212f622f64465942414141414141414126656b3d31266b703d312670743d3026626f3d34414d6b417541444a4149444544552126746c3d31267675696e3d3230313839383237363326746d3d31353335323737363030267363653d36302d342d332672663d7669657765725f333131)

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


项目启动：`python view.py`



### 更新链接
---
[github](https://github.com/WeAreHus/StudyRecord/tree/master/day-2018-08-26/new_system)





### 运行效果部分展示
---
![登陆](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/hJrCWjQVdkUoQv5K1f4uOytz9v2.xCL5dxnUujJh.fI!/b/dDYBAAAAAAAA&ek=1&kp=1&pt=0&bo=MAf4AjAH.AIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=50-1-1&rf=viewer_311)
![主页](http://a4.qpic.cn/psb?/V13uRwZ427WzZu/vl8wWVEKe6.07FzcwLJGH5pbYlP3xLU.MCyrKURuZ9s!/b/dDcBAAAAAAAA&ek=1&kp=1&pt=0&bo=HgfzAh4H8wIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=60-4-3&rf=viewer_311)
![成绩](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/p3f6KdfDqGBteLoyBnsmjWi6XAHwiNAWopTiqzsMu7M!/b/dFYAAAAAAAAA&ek=1&kp=1&pt=0&bo=Dgf8Ag4H*AIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=50-1-1&rf=viewer_311)
![课程](http://a1.qpic.cn/psb?/V13uRwZ427WzZu/Mymr7HYjbUpPEdMZGnNtcvc4fXqMMLsORw3N0Qd1bVs!/b/dDQBAAAAAAAA&ek=1&kp=1&pt=0&bo=FQf1AhUH9QIDEDU!&tl=1&vuin=2018982763&tm=1535857200&sce=50-1-1&rf=viewer_311)
