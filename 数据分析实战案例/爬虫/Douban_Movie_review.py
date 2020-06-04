import requests as rq

#登录豆瓣的函数
def login_douban():
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
        r = rq.post(url=login_url, headers=headers, data=data)
        r.raise_for_status()
    except:
        print("爬取失败")
    # 打印请求结果
    print(r.text)
if __name__ == '__main__':
    login_douban()