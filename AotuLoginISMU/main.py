#https://www.pythonheidong.com/blog/article/553834/1a821e87bbf00a9a3e71/  ubuntu环境下安装firefox 对应需要的驱动
##########定时执行脚本#############
# crontab -e    终端输入，编辑文件（首次选择编辑的工具），添加
# 1,16,30,45 * * * * /home/xinqiang_329/anaconda3/bin/python /home/xinqiang_329/桌面/cwp/autoSMU/main.py > /home/xinqiang_329/桌面/cwp/autoSMU/login_tem.log
# 具体参数看网页https://www.yisu.com/zixun/585879.html
# service cron restart  更新配置


import os
from selenium import webdriver
import time
def test_net():     #0表示ping通了，其他表示没通，0也表示无法识别主机？？
    print('测试网络')
    res = os.system('ping -c 2 www.baidu.com')
    return res


def Login():#1 成功   0 失败
    option = webdriver.FirefoxOptions()
    option.headless=True
    drive = webdriver.Firefox(options=option)
    url = 'https://hwifi.shmtu.edu.cn:19008/portalpage/cc15f524-83a4-4234-8585-60419a2fa308/20201112140517/pc/auth.html?apmac=6c16320d27aa&uaddress=10.66.132.25&umac=08beac2ace50&authType=1&lang=zh_CN&ssid=aVNNVQ==&pushPageId=37efd806-5224-4e7b-a186-43538139e997'
    url_second = 'https://hwifi.shmtu.edu.cn:19008/portalpage/cc15f524-83a4-4234-8585-60419a2fa308/20201112140517/pc/auth.html' #无法点击登录

    name = '20213051xxxx'       #学号
    password = 'xxxxxxxxx' #密码
    drive.get(url)
    drive.implicitly_wait(20)#隐性等待， 最长等待20秒
    drive.find_element_by_id('username').send_keys(name)
    time.sleep(1)
    drive.find_element_by_id('password').send_keys(password)
    time.sleep(1)
    drive.find_element_by_id('loginBtn').click()
    time.sleep(10)      #等待页面加载完成
    # print(drive.page_source)
    title = drive.title #页面的title，如果成功，会是登录成功，否则还是登录
    drive.quit()  #自动退出
    print(title)
    if title == '登录成功':
        return 1
    else:
        print('登陆失败')
        return 0


if __name__ == '__main__':
    print('开始')
    res = test_net()
    if res :
        print('网络不通，开始尝试登陆')
        flag = Login()
        if flag == 0:
            print('怎么办?，试着去选择wifi连接？')
    else:
        print('已连接')
        flag = Login()
        if flag == 0:
            print('怎么办')

