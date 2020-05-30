import requests as rq

#登录豆瓣的函数
def login_douban():
    # 登录URL
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    # 请求头信息
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    # 传递用户名和密码
    data = {
        'name':'15704446814',
        'password':'lxl12359',
        'remember':'false'}

    try:
        r = rq.post(login_url,headers=headers,data=data)
        r.raise_for_status()
    except:
        print("爬取失败")

    #打印请求结果
    print(r.text)

if __name__ == '__main__':
    login_douban()