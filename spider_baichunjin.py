#! /usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import os
import sys
import re
import time

'''
项目:爬虫程序
研发人员: 白春瑾
需求:
    1、爬取 "www.hao123.com"下的资源(只限该站的资源)
    2、设置爬取资源的上限，比如，设置1个参数max_size=1000，爬到1000个时候就终止爬虫
    3、可以print屏幕输出爬取的资源链接
    4、命令行方式运行: 例如: python spider_baichunjin.py --site http://www.hao123.com/ --max_size 1000
    5、运行过程中在本地保存日志文件，记录抓取的资源url链接
'''

#帮助函数
def Usage():
    print '################################'
    print '1、 --site 参数用来指定抓取的url地址'
    print '2、 --max_size 参数用来指定抓取资源的上限'
    print '3、运行格式为: python spider_baichunjin.py --site http://www.hao123.com/ --max_size 1000'
    print '4、如果只想抓取链接,可以通过添加"--no_save"来取消内容保存'
    print '################################'

#文本存储url处理
def saveResource(url, saveName):
    try:
        f = urllib2.urlopen(url)
    except:
        print '获取页面失败,请检查网络情况.'
        return False
    dir_path = os.path.abspath('.') + '/' + 'spider_bcj/'
    if not os.path.exists(dir_path):
        os.system(r'mkdir spider_bcj')
    if '.js' in url:
        path = dir_path + saveName + '.js'
    elif '.css' in url:
        path = dir_path + saveName + '.css'
    else:
        path = dir_path + saveName
    p = open(path,'wb')
    s = f.read()
    p.write(s)
    f.close()
    p.close()
    return True
	
#正则处理html资源
def getURL(url):
    html_rtv = []
    try:
        f = urllib2.urlopen(url)
    except:
        print '获取url信息失败'
        return False
    pa = re.compile(r"href=[\"']?([^ >\"']+)")
    while True:
        s = f.read()
        if not s:
            break
        urls = pa.findall(s)
        for url in urls:
            if 'hao123.com' in url:
                html_rtv.append(url)
            elif '.css' in url:
                html_rtv.append(url)
            else:
                pass
    f.close()
    html_rtv = list(set(html_rtv))
    return html_rtv
    
#日志函数
def saveLog(n, url):
    log_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    file_name = log_date + '_catch_log.txt'
    f = open(file_name,'a+')
    msg = '第' + str(n) + '个url资源:' + url + '\r'
    f.write(msg)
    f.close()
    return n 
		
#爬取资源上限控制
def spiderControl(baseURL,max_size,rtv):
    url_list = []
    url_list.append(baseURL)
    n = 1
    while True:
        if n > int(max_size):
            print '达到指定数量，抓取停止.'
            return True
        if len(url_list) > 0:
            url = url_list.pop(0)
            if n == 1:
                print '基础URL资源: %r' %url
            else:
                print '第%r个资源: %r' %(n,url)
            saveLog(n, url)
            if rtv == 0:
                saveResource(url, str(n))
            n = n + 1
            if len(url_list) < max_size:
                urllist = getURL(url)
                for url in urllist:
                    if url_list.count(url) == 0:
                        url_list.append(url)
        else:
            print '全部资源抓取完成.'
            break
    return True

#命令行参数处理
def processCmdLine():
    if (len(sys.argv) >=2):
        if (sys.argv[1] == "--help"):
            Usage()
            sys.exit()
        else:
            if (sys.argv[1] == "--site"):
                url = sys.argv[2]
            else:
                print"错误的site参数"
                sys.exit()
            if (sys.argv[3] == "--max_size"):
                max_size = sys.argv[4]
            else:
                print"错误的max_size参数"
                sys.exit()
            if (sys.argv[5] == "--no_save"):
                n = 1
                print '不保存链接资源文件'
            else:
                n = 0
        spiderControl(url, max_size, n)				
    else:
        print "没有指定命令行参数,请重新运行程序,可以通过--help命令来获取帮助."
        sys.exit()

#主程序部分
if __name__ == '__main__':
    processCmdLine()
