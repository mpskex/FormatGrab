#coding:utf-8
import requests
from bs4 import BeautifulSoup
##刘方瑞：北京工业大学：15143103（不要吐槽我这个人文院的学号
##获取信息门户新通知的简单脚本实现
##可以拓展到检索所有信息门户的消息（院部处通知，讲座海报等等....

##认证信息dict对象
##Token1是用户名（学号）
##Token2是密码
##顺便吐槽一下信息门户居然还用明文传输密码...（鄙视
Auth = {'Login.Token1':'', 
        'Login.Token2':'', 
        'goto':'http://my.bjut.edu.cn/loginSuccess.portal', 
        'gotoOnFail':'http://my.bjut.edu.cn/loginFailure.portal'}
##通过认证传送门获取信息门户的认证cookies
ar = requests.get('https://my.bjut.edu.cn/userPasswordValidate.portal', Auth)
##利用获取的cookies来访问信息门户海报页面
r = requests.get('https://my.bjut.edu.cn/detach.portal?ignoreSessionInvalid=true&action=bulletinsMoreView&.ia=false&.pmn=view&.pen=pe438', cookies = ar.cookies)
print('HTTP Request: %d' %( ar.status_code ))
##使用beautifulsoup来解析获取的html
soup = BeautifulSoup(r.text, "lxml", from_encoding = 'utf-8')
tag = soup.find("ul", id = "blpe438")
a = 1
f = open('format.html','wb')
##标明网页使用GB18030来编码
header = '<!DOCTYPE html><head><meta charset="gb18030"><title>Lecture Posters</title></head>'
f.write(str(header) + '\n' + '<body>')
##开始对所有海报下面的子节点枚举
for n in tag.children:
    if (n!='\n'):
        ##删除带有img的a标签
        n.a.decompose()
        ##使用beautifulsoup来获取每个单独页面的网址
        url_tag = n.find('a', class_= "rss-title")
        ##print url_tag.encode('gb18030')
        url = 'http://my.bjut.edu.cn/' + str(url_tag['href']).encode('gb18030')
        url_name = (url_tag.string).encode('gb18030')
        print url_name
        print url
        ##使用之前会话的cookie对获得的网址来请求海报内容
        poster = requests.get(str(url), cookies = ar.cookies)
        poster_soup = BeautifulSoup(poster.text, "lxml", from_encoding = 'utf-8')
        poster_tag = poster_soup.find('div', style = "padding:20px;")
        print poster_tag.encode('gb18030')
        ##该死的信息门户使用的gb18030编码，妈的智障
        ##print n.encode('gb18030')
        print 
        url_tag['href'] = url
        f.write(str(a) + str(n.encode('gb18030')) + '\n' + poster_tag.encode('gb18030') + '\n')
        a = a + 1
f.write('</body></html>')
f.close()