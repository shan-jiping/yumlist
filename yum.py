# coding:utf-8
'''
Created on 2015-8-16

@author: shan.jiping
'''
import urllib  
import HTMLParser
from datetime import datetime
import os
import socket
from time import sleep
import platform


genurl="http://repo.percona.com/release/6/"
#genurl="http://10.10.20.58/percona/"            #测试使用yum源  方便测试问题
urlindex=0
yumurl=[]
tmpmulu=[]
tmpfile=[]
yum={}
yum[genurl]=['']
yumurl.append(genurl)
lim=True
sysstr = platform.system()

def get_list(url):
    global tmpfile
    global tmpmulu
    page = urllib.urlopen(url)                                              # 打开URL  
    data = page.read()                                                      # 读取URL内容  
    parser = MyHTMLParser()                                                 # 生成实例对象  
    parser.feed(data)
    parser.close()
    page.close()
    for mulu in tmpmulu:
        yum[url+mulu]=[]
        yumurl.append(url+mulu)
    yum[url]=tmpfile
    del tmpmulu
    del tmpfile
    tmpmulu=[]
    tmpfile=[]


class MyHTMLParser(HTMLParser.HTMLParser):                                              # 创建HTML解析类  
        def __init__(self):
                HTMLParser.HTMLParser.__init__(self)  
        def handle_starttag(self, tags, attrs):
            if tags == 'a': 
                for name,value in attrs:                                        #name为标签的属性名，如href、name、id、onClick等等
                    if name == "href" and value!="../":
                        if len(value.split('/')) > 1:
                            tmpmulu.append(value)
                            #print "add urlpath " + value
                        else:
                            tmpfile.append(value)
                            #print "file" + value
                            
def downloadlist():
    global lim
    global urlindex
    while lim == True:
        #print len(yumurl) ,urlindex
        if len(yumurl)>0 and len(yumurl) < urlindex +1 :
            lim=False
            break
        get_list(yumurl[urlindex])
        urlindex=urlindex + 1 
    #print "yum" + str(yum)
    #print yum.keys()
    f=open('tmp/yum.txt','a')
    for i in yum.keys():
        f.write('url: ' + str(i) + '\n')
        for l in yum[i]:
            #print l
            f.write("    "+i + l + '\n')
    f.flush()
    f.close()
    
    for i in yum.keys():
        for l in yum[i]:
            downloadfile(i+l,l)
            sleep(1)
            
def filesize(filepath):
    return '%.3fM' %(os.path.getsize(filepath)/1024.0/1024.0)


def df(url,filepath,filename):
    if(sysstr =="Windows"):
        urllib.urlretrieve(url, filepath+filename,callback)   
    elif(sysstr == "Linux"):
        os.system('axel -n 5 -a --verbose ' + url + ' -o ' +filepath+filename)
    else:
        print ("Other System tasks")

def callback(a,b,c):
    '''
    @a:到目前位置传递的数据块数量
    @b:每个数据块的大小  单位byte
    @c:文件大小  单位byte
    '''
    down_progress=100.0*a*b/c
    
    if down_progress>100:
        down_progress =100
    print "%.2f%%\r" %down_progress,
    
    
def downloadfile(url,filename):
    filepath=url.replace(genurl,'').replace(filename,'')
    dl=open('tmp/downfile.txt','a')
    if os.path.exists(filepath):
        pass
    else:
        os.makedirs(filepath)
        dl.write( "Create PATH " + filepath +'\n')
        
    pagesize=urllib.urlopen(url).info()['Content-Length']

    if os.path.exists(filepath+filename):
        LocalFileSize=os.path.getsize(filepath+filename)
        if  int(LocalFileSize) == int(pagesize):
            LocalFileSize=LocalFileSize/1024.0/1024.0
            #dl.write("File:"+filepath+filename +" exists   filesize ="+ str("%.2f" % LocalFileSize) + "M  Pass Download" +'\n')
            print "File:"+filepath+filename +" exists   filesize ="+ str("%.2f" % LocalFileSize) + "M  Pass Download"
        else:
            os.remove(filepath+filename)
            starttime=datetime.now()
            try:
                socket.setdefaulttimeout(1200)
                print filename
                df(url,filepath,filename)
            except (urllib.ContentTooShortError, IOError),e:
                dl.write(e )
            #urllib.urlretrieve(url, filepath+filename,callback)      #单个文件可以显示下载进度
            endtime=datetime.now()
            timeElapse = (endtime-starttime).total_seconds()
            dl.write("File size does not match the source  remove old file  downloading " + url + " ==> "+filepath + filename +"  done  耗时：" + str(timeElapse)  + '  FileSize:' + filesize(filepath + filename)+ '\n' )
    else:
        starttime=datetime.now()
        try:
            print filename
            df(url,filepath,filename)
        except (urllib.ContentTooShortError, IOError),e:
            dl.write(e)
        endtime=datetime.now()
        timeElapse = (endtime-starttime).total_seconds()
        dl.write("downloading " + url + " ==> "+filepath + filename +"  done  耗时：" + str(timeElapse)  + '  FileSize:' + filesize(filepath + filename)+ '\n' )
    dl.flush()
    dl.close()
    
if __name__ == "__main__":
    downloadlist()
    #downloadfile('http://10.10.20.58/percona/RPMS/x86_64/Percona-Server-tokudb-56-5.6.22-rel71.0.el6.x86_64.rpm', 'Percona-Server-tokudb-56-5.6.22-rel71.0.el6.x86_64.rpm')
    f=open('tmp/yum.txt','a')
    f.write('==============================================================\n')
    f.write(' download done'+'\n')
    f.write('==============================================================\n')
    f.flush()
    f.close()
