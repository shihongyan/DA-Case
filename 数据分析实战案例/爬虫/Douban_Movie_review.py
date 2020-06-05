import requests as rq
import os
import re
import time
import random
import jieba

#设置输入输出流的格式
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#生成Session对象，用于保存Cookie
s = rq.session()
# 影评数据保存文件
COMMENTS_FILE_PATH = 'douban_comments.txt'

def login_douban():
    '''
    模拟登录豆瓣
    :return:
    '''
    # 登录URL
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    # 请求头信息
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
               'Cookie':'bid=oOAy1RpbdLk; douban-fav-remind=1; __gads=ID=6a7796386471d576:T=1584073640:S=ALNI_MZjFWTvDwaUpVlBNYLiQ-iqEunJgQ; __utma=30149280.2043714682.1584073643.1591261973.1591266192.8; __utmz=30149280.1591261973.7.7.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login_popup; ll="118282"; viewed="27593848"; gr_user_id=b21f2b5d-64f3-4453-94cf-b1dabd759c04; _vwo_uuid_v2=D9BF31F9A32156E50EE89B9F616FAB46A|13912416bc021a9b6139f20ffa737a34; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14296; apiKey=; __utmc=30149280; login_start_time=1591266195003; last_login_way=account; ap_v=0,6.0; __utmb=30149280.1.10.1591266192; __utmt=1'}
    # 传递用户名和密码
    data = {
        'ck': '',
        'name':'15704446814',
        'password':'lxl12359',
        'remember':'false',
        'ticket': ''}
    try:
        r = s.post(url=login_url, headers=headers, data=data)
        r.raise_for_status()
    except:
        print("登录请求失败")
        return 0
    # 打印请求结果
    print(r.text)
    return 1

def spider_comment(page=0):
    '''
    爬取某页影评
    :param page: 起始位置，相当于分页参数
    :return:
    '''
    print('开始爬取第%d页' % int(page))
    start = int(page * 20)
    comment_url = 'https://movie.douban.com/subject/27010768/comments?start=%d&limit=20&sort=new_score&status=P' % start
    #请求头
    headers ={'user-agent':'Mozilla/5.0'}
    try:
        r = s.get(comment_url,headers=headers)
        r.raise_for_status()
    except:
        print('爬取请求失败' % page)
        return 0

    #使用正则提取影评内容
    comments = re.findall('<span class="short">(.*)</span>',r.text)
    if not comments:
        return 0
    #写入爬取内容
    with open(COMMENTS_FILE_PATH, 'a+',encoding=r.encoding) as file:
        file.writelines('\n'.join(comments))
    return 1

def batch_spider_comment():
    '''
    批量爬取豆瓣影评
    page:分页参数
    :return:
    '''
    #写入数据前先清空之前的数据
    if os.path.exists(COMMENTS_FILE_PATH):
        os.remove(COMMENTS_FILE_PATH)
    page = 0
    while spider_comment(page):
        page += 1
        #模拟用户浏览，设置一个爬虫问题，防止ip被封
        time.sleep(random.random() * 3)
    print("爬取完毕")

def cut_word():
    '''
    对数据分词
    :return: 分词后的数据
    '''
    with open(COMMENTS_FILE_PATH,encoding='UTF-8') as file:
        comment_text = file.read()
        wordlist = jieba.cut(comment_text,cut_all=True)
        wl = " ".join(wordlist)
        print(wl)
        return wl
if __name__ == '__main__':
    #if login_douban():
     #   batch_spider_comment()
    cut_word()