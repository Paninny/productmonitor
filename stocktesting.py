#coding=utf8
from selenium import webdriver
from lxml import etree
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

driver = webdriver.Chrome()
driver.maximize_window()


def get_info(url):
    driver.get(url)
    driver.implicitly_wait(10)
    selector = etree.HTML(driver.page_source)
    infos = selector.xpath('//*[@id="store-prompt"]')

    status = ""
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y-%m-%d, %H:%M:%S")

    message, smtp = initMail(url)

    for info in infos:
        status = info.xpath('strong/text()')[0]
        print(date_time + ":  " + status)
    if status == '无货':
        time.sleep(300)
        OneMore(url)
    elif status == '可配货' or status == '有货':
        print("---下单了---")
        print(date_time + ":  " + status)
        print("---下单了---")

        smtp.sendmail(from_addr="heavenlj@126.com", to_addrs="paninny0728@gmail.com", msg=message.as_string())

        time.sleep(1200)
        OneMore(url)
    else:
        print("---状态异常---")
        print(date_time + ":  " + status)
        print("---状态异常---")
        smtp.sendmail(from_addr="heavenlj@126.com", to_addrs="paninny0728@gmail.com", msg=message.as_string())
        OneMore(url)


def initMail(url):
    smtp = smtplib.SMTP()
    smtp.connect("smtp.126.com", port=25)
    smtp.login(user="heavenlj@126.com", password="******")
    message = MIMEText('达菲格智能系统 \r\n 提醒您 \r\n 货已到 快交易!! \r\n 传送门: ' + url, 'plain', 'utf-8')
    message['From'] = Header('达菲格邮件系统', 'utf-8')
    message['To'] = Header('亲爱的用户', 'utf-8')
    message['Subject'] = Header('达菲格定制提醒服务', 'utf-8')
    return message, smtp


def OneMore(url):
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(10)
    driver.get(driver.current_url)
    driver.implicitly_wait(10)
    get_info(driver.current_url)


if __name__ == '__main__':
    # url = 'https://item.jd.com/100046206079.html'
    url = 'https://item.jd.com/100020537365.html'
    # 京东把爬虫屏蔽了
    driver.get(url)
    get_info(driver.current_url)



