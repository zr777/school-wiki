import requests
from bs4 import BeautifulSoup
import re

# 登录
login_url = 'http://127.0.0.1:8000/admin/login/'
s = requests.session()
content = s.get(login_url).content.decode('utf-8')
bs = BeautifulSoup(content, "lxml")
csrf = bs.find('input', attrs={'type': "hidden"}).attrs['value']
redirect_url = '/'
data = {
	'csrfmiddlewaretoken': csrf,
	'next': redirect_url,
	'username': 'xxx',
	'password': '123',
}
content = s.post(login_url, data=data)


# 增加用户
add_user_url = 'http://127.0.0.1:8000/admin/users/add/'
content = s.get(add_user_url).content.decode('utf-8')
bs = BeautifulSoup(content, "lxml")
csrf = bs.find('input', attrs={'type': "hidden"}).attrs['value']
data = {
	'csrfmiddlewaretoken': csrf,
	'username': 'guest',
	'email': 'unknown@5izxy.cn',
	'first_name': 'apple',
	'last_name': 'guest',
	'password1': 'xiaodengshen',
	'password2': 'xiaodengshen',
	'groups': '2',
}
content = s.post(add_user_url, data=data)

# 先上传一张图片
# 增加首页
add_wikihome_url = 'http://127.0.0.1:8000/admin/pages/add/wiki/wikihome/2/'
content = s.get(add_wikihome_url).content.decode('utf-8')
bs = BeautifulSoup(content, "lxml")
csrf = bs.find('input', attrs={'type': "hidden"}).attrs['value']
data = {
	'csrfmiddlewaretoken': csrf,
	'next':'',
	'title':'华南理工大学校园---',
	'logoname':'SCUT-WiKi',
	'toplinks-TOTAL_FORMS':'3',
	'toplinks-INITIAL_FORMS':'0',
	'toplinks-MIN_NUM_FORMS':'0',
	'toplinks-MAX_NUM_FORMS':'1000',
	'toplinks-0-title':'首页',
	'toplinks-0-link_external':'',
	'toplinks-0-link_page':'2',
	'toplinks-0-link_document':'',
	'toplinks-0-id':'',
	'toplinks-0-ORDER':'1',
	'toplinks-0-DELETE':'',
	'toplinks-1-title':'标签',
	'toplinks-1-link_external':'http://treeinlake.github.io',
	'toplinks-1-link_page':'',
	'toplinks-1-link_document':'',
	'toplinks-1-id':'',
	'toplinks-1-ORDER':'2',
	'toplinks-1-DELETE':'',
	'toplinks-2-title':'关于',
	'toplinks-2-link_external':'http://aboutus.cn',
	'toplinks-2-link_page':'',
	'toplinks-2-link_document':'',
	'toplinks-2-id':'',
	'toplinks-2-ORDER':'3',
	'toplinks-2-DELETE':'',
	'image':'1',
	'intro':'华工小灯神团队带来的校园维基百科~',
	'little_intros-TOTAL_FORMS':'4',
	'little_intros-INITIAL_FORMS':'0',
	'little_intros-MIN_NUM_FORMS':'0',
	'little_intros-MAX_NUM_FORMS':'1000',
	'little_intros-0-fa_name':'fa-info',
	'little_intros-0-title':'丰富的资讯',
	'little_intros-0-caption':'这里涵盖了华工校园的各种资讯',
	'little_intros-0-id':'',
	'little_intros-0-ORDER':'1',
	'little_intros-0-DELETE':'',
	'little_intros-1-fa_name':'fa-lightbulb-o',
	'little_intros-1-title':'问题解决',
	'little_intros-1-caption':'这里有详实的校内问题解决办法',
	'little_intros-1-id':'',
	'little_intros-1-ORDER':'2',
	'little_intros-1-DELETE':'',
	'little_intros-2-fa_name':'fa-map-o',
	'little_intros-2-title':'导航',
	'little_intros-2-caption':'校园生活一站式导航',
	'little_intros-2-id':'',
	'little_intros-2-ORDER':'3',
	'little_intros-2-DELETE':'',
	'little_intros-3-fa_name':'fa-microchip',
	'little_intros-3-title':'学习资料',
	'little_intros-3-caption':'学习资料一网打进',
	'little_intros-3-id':'',
	'little_intros-3-ORDER':'4',
	'little_intros-3-DELETE':'',
	'slug':'华南理工大学校园aaa',
	'seo_title':'',
	'search_description':'',
	'go_live_at':'',
	'expire_at':'',
	'action-publish':'action-publish',
}
content = s.post(add_wikihome_url, data=data)




#----------------解析并导入文章
from lxml import etree#导入lxml库  
from datetime import datetime
tree = etree.parse(r'D:/谷歌下载/wordpress.2017-04-13.xml')#将xml解析为树结构  
root = tree.getroot()#获得该树的树根
ns = {'content':"http://purl.org/rss/1.0/modules/content/",
	  'dc':'http://purl.org/dc/elements/1.1/'}
posts = []
for i in root.find('channel').findall('item'):
	posts.append([
		i.find('title').text,
		str(
			datetime.strptime(
				i.find('pubDate').text, "%a, %d %b %Y %H:%M:%S %z"
			).date()
		),
		','.join([c.text for c in i.findall('category') if c.text != '未分类']),
		i.findall('dc:creator', ns)[0].text,
		i.findall('content:encoded', ns)[0].text,
	])
	
add_wiki_page = 'http://127.0.0.1:8000/admin/pages/add/wiki/wikipage/3/'
for title, date, tags, creator, body in posts:
	content = s.get(add_wikihome_url).content.decode('utf-8')
	bs = BeautifulSoup(content, "lxml")
	csrf = bs.find('input', attrs={'type': "hidden"}).attrs['value']
	data = {
		'csrfmiddlewaretoken': csrf,
		'next':'',
		'title':title,
		'date':date,
		'tags':tags,
		'author':creator,
		'subtitle':'',
		'body-count':1,
		'body-0-deleted':'',
		'body-0-order':0,
		'body-0-type':'raw_html',
		'body-0-value': body,
		'related_links-TOTAL_FORMS':'0',
		'related_links-INITIAL_FORMS':'0',
		'related_links-MIN_NUM_FORMS':'0',
		'related_links-MAX_NUM_FORMS':'1000',
		'slug':title,
		'seo_title':'',
		'search_description':'',
		'go_live_at':'',
		'expire_at':'',
		'action-publish':'action-publish',
	}
	content = s.post(add_wiki_page, data=data)

	
# 列出所有索引	
# curl 'localhost:9200/_cat/indices?v'
# curl -XDELETE 'localhost:9200/wikiscut?pretty'
# curl -XDELETE 'localhost:9200/wikiscut__wagtailcore_page?pretty'
