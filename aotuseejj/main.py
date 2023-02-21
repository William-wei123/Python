from selenium import webdriver
import os
import time
import logging
from selenium.common import exceptions as ex
from selenium.webdriver.common.by import By

import smtplib  # 负责发送邮件
from email.mime.text import MIMEText  # 构造文本
from email.mime.image import MIMEImage  # 构造图片
from email.mime.multipart import MIMEMultipart  # 将多个集合对象集合起来
from email.header import Header
import datetime

class Stock(object):    #借鉴别人代码
    def __init__(self,con):
        # 无浏览器界面化
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.brower = webdriver.Chrome(options=options)
        self.con = con

    def getAllStockUrl(self):
        if os.path.exists(self.con.url_path):
            return

        url = 'https://fund.eastmoney.com/'
        self.brower.get(url)

        data = self.brower.find_element_by_xpath('//*[@id="jjjz"]/div[4]/table/tfoot/tr/td/a')

        data_information = data.get_attribute('href')
        time.sleep(2)
        self.brower.get(data_information)

        table_data = {}
        fp = open(self.con.url_path, 'w')

        # find_element寻找第一个 find_elements寻找所有的
        for j in range(int(self.brower.find_element_by_xpath('//*[@id="pager"]/span[9]').text[1:-1])):
            try:
                tags = self.brower.find_elements_by_xpath('//*[@id="oTable"]/tbody/tr')
                for i in tags:
                    name = i.find_element_by_xpath('./td[5]/nobr/a[1]').text
                    num = i.find_element_by_xpath('./td[5]/nobr/a[1]').get_attribute('href')
                    num = num[:-5]
                    if name not in list(table_data.keys()):
                        fp.write(name + ',' + 'http://fundf10.eastmoney.com/jjjz_{}.html'.format(num[-6:]) + '\n')
                        table_data.setdefault(name, 'http://fundf10.eastmoney.com/jjjz_{}.html'.format(num[-6:]))
                        logging.info('{} --> {}'.format(name, table_data[name]))

                self.brower.find_element(by=By.XPATH, value='//*[@id="pager"]/span[8]').click()
                fp.flush()
                time.sleep(3)
            except ex.StaleElementReferenceException as e:
                self.brower.find_element_by_xpath('//*[@id="pager"]/span[8]').click()
                time.sleep(4)
                logging.warning(str(e))
        self.brower.close()
        fp.close()


    def getone(self, name):
        with open(self.con.url_path, 'r') as fp:
            csvLines = fp.read().split('\n')

        url = None
        stockName = None
        for csvLine in csvLines:
            if name in csvLine:
                csvCol = csvLine.split(',')
                stockName = csvCol[0]
                url = csvCol[1]
                break
        if url == None:
            
            print("网站暂未收录 %s"%name)
            url = 'http://fundf10.eastmoney.com/jjjz_%s.html'%name
            self.brower.get(url)
            stockName = self.brower.find_element(by=By.XPATH,value="//div[@class='col-left']/h4/a").text
            urlcvs = open('./data/url.csv', 'a+')
            urlcvs.write('{},{}\n'.format(stockName,url))
            urlcvs.close()

        logging.info(url)
        tempstock = self.brower.get(url)
        output = self.brower.find_element(by=By.XPATH,value="//span[@id='fund_gszf']").text
        print(output)
        # dataPath = self.con.data_path + stockName + '_{}.csv'.format(datetime.now().strftime('%Y%m%d'))
        # if os.path.exists(dataPath):
        #     return stockName


        # df, lists, numn, data, table_name = self._getdata(url)
        
        return stockName, output
class con(object):
    def __init__(self,file_name):
        self.url_path = file_name
        pass

class email2xx(object):
    def __init__(self,receiver='1766923xx@qq.com') -> None:
        self.Sender = 'WeipingChxxx6@163.com'
        self.SenderName = 'xx'
        self.SenderToken = 'WKEFSKxxxxxxxx'
        self.receiver = receiver
        self.mail_host = "smtp.163.com"
        pass

    def creatmail(self,  email_Subject, email_text, annex_file=None,annex_name=None):
        #生成一个空的带附件的邮件实例
        message = MIMEMultipart()
        #将正文以text的形式插入邮件中(参数1：正文内容，参数2：文本格式，参数3：编码方式)
        message.attach(MIMEText(email_text, 'plain', 'utf-8'))
        #生成发件人名称
        message['From'] = Header(self.SenderName, 'utf-8')
        #生成收件人名称
        message['To'] = Header(self.receiver, 'utf-8')
        #生成邮件主题
        message['Subject'] = Header(email_Subject, 'utf-8')
        if annex_file is None:
            pass
        else:
            #读取附件的内容
            att1 = MIMEText(open(annex_file, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            #生成附件的名称
            att1["Content-Disposition"] = 'attachment; filename=' + annex_name
            #将附件内容插入邮件中
            message.attach(att1)
        #返回邮件
        return message
        
    def send_email(self, msg):
    # 一个输入邮箱、密码、收件人、邮件内容发送邮件的函数
        try:
            #找到你的发送邮箱的服务器地址，已加密的形式发送
            server = smtplib.SMTP()  # 发件人邮箱中的SMTP服务器
            server.connect(self.mail_host, 25)
            server.ehlo()
            #登录你的账号
            server.login(self.Sender, self.SenderToken)  # 括号中对应的是发件人邮箱账号、邮箱密码
            #发送邮件
            server.sendmail(self.Sender, self.receiver, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号（是一个列表）、邮件内容
            print("邮件发送成功" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            txtlog = open('log.txt','a+')
            txtlog.write("邮件发送成功" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            txtlog.close()
            # 关闭SMTP对象
            server.quit()
        except Exception:
            print('邮件发送失败'+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            txtlog = open('log.txt','a+')
            txtlog.write("邮件发送失败" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            txtlog.close()

    def send2xx(self, title, content):
        messge = self.creatmail(title,content)
        self.send_email(messge)



if __name__ == "__main__":
    conn = con('./data/url.csv')
    

    test1 = Stock(conn)

    with open('./data/iwant1.csv', 'r', encoding='utf-8') as fp:
        allMy = fp.read().split('\n')
    Output = {}

    for one in allMy:
        if len(one) is 7:
            one = one[1:7]
        elif len(one) is 6:
            pass
        print(one)
        name, output = test1.getone(one)
        Output[name] = output
    # test1.getAllStockUrl()
    text = str(Output).replace("'", "")
    text = text.replace('{','')
    text = text.replace('}','')
    text = text.replace(',','\n')
    mail_test = email2xx()
    mail_test.send2xx('基金本日涨幅',text)
    print('暂时没错')
