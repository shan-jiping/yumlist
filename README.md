同步yum源脚本
============================================


用于percona等不能通过sync方式同步yum源来实现    linux下最好使用axel下载
--------------------------------------------------
使用HTMLParser 将页面中所有a标签中的连接全部获取出来  并和访问的url  最终拼接成完整的url用于下载使用


输出日志
--------------------------------------------------
输出日志存放在相对路径的tmp下

downfile.txt 输出的是下载文件的信息  包括下载的url   下载文件的路径及名字   下载所用时长   以及下载文件的大小   程序会自动创建下载的目录

yum.txt   输出的是所有被抓到下来的url   
