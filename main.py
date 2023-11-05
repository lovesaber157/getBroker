import httpx
import queue
import json
import csv
import re

# 发包函数封装
def send_Http(url,proxy=""):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
    }
    if proxy != "":
        with httpx.Client(proxies=proxy,http2=True,verify=False) as client:
            resText = client.get(url,headers=headers).text
            return resText
    else:
        resText = httpx.get(url,headers=headers,verify=False).text
        return resText

# 匹配
def match_Data(data):
    pattern = r".*Proxies at (\d*-\d*-\d*) \((\d+) proxies\)"
    match = re.findall(pattern,data)[0]
    print(f"当前时间:{match[0]},可爬取代理数据:{match[1]}")
    return match

# 控制台输出
def console_Log(mainurl,parameter,proxy=""):
    newSrc = None
    while True:
        choose = str.upper(input("是否进行爬取？(Y/N)"))
        try:
            # 输入数据去重
            choose = {}.fromkeys(choose)
            choose = "".join(list(choose.keys()))
            choose = ord(choose)
        except:
            pass
        if(choose == 89):
            print("正在进行爬取！")
            newSrc =f"{mainurl}api/archive/{parameter}"
            return newSrc
        elif(choose == 78):
            print("程序正常退出！")
            break
        else:
            print("抱歉，您输入的参数程序理解不了")
            continue
    return newSrc

# 爬取网站返回数据数组
def crawl_Web(url,proxy=""):
    data = ""
    text = send_Http(url, proxy)
    match = match_Data(text)
    parameter = match[0]
    newSrc = console_Log(url,parameter,proxy)
    if newSrc:
        data = json.loads(send_Http(newSrc,proxy))
        csvfile = write_File(parameter)
        csvWrite = csv.writer(csvfile)
        id = 0
        for item in data:
            addr = item['addr']
            type = item['type']
            id += 1
            # 对type进行转换
            if type == 4:
                type = 'SOCKS5'
            elif type == 1:
                type = 'HTTP'
            elif type == 2:
                type = 'HTTPS'
            csvWrite.writerow([id,addr,type])
        csvfile.close()
        print("爬取完成！")

# 写入csv文件
def write_File(filename):
    csvfile = open(f"./{filename}_proxyList.csv","a+",encoding="utf-8",newline="")
    name = ['id','ip:port','type']
    csvWrite = csv.writer(csvfile)
    csvWrite.writerow(name)
    return csvfile


if __name__ == "__main__":
    # 爬取的免费代理网站
    crawlWeb = 'https://checkerproxy.net/'
    # 设置httpx的代理
    proxy = {
        "https://":"http://localhost:1080",
        "http://": "http://localhost:1080",
    }
    # 创建队列
    q = queue.Queue()
    crawl_Web(crawlWeb,proxy)