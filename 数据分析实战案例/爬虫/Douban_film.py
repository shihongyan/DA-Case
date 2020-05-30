import requests as rq
from lxml import etree

url = 'https://movie.douban.com/subject/1292001/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
data = rq.get(url,headers=headers).text
s = etree.HTML(data)

#默认返回的是list列表格式
film = s.xpath('/html/body/div[3]/div[1]/h1/span[1]/text()')
director = s.xpath('/html/body/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[2]/a/text()')
Starring = s.xpath('/html/body/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[3]/span[2]/a/text()')
duration = s.xpath('/html/body/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[13]/text()')
print("影名：" , film[0])
print("director:",director[0])
print("Starring:",Starring[0])
print("duration:",duration[0])

