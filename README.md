# bilibili 用户数据爬虫

本平台适用于所有系统，使用VS Code开发，如果使用其他的开发平台亦可以运行。开发语言为Python，版本是Python 3.7.5，使用Python 3.x以上的版本都可以运行。

## 文件介绍：
agent_pool.txt：用户代理池

logs.txt:爬虫日志

mybilibili.py：爬虫文件

proxies/get_proxies.py：ip代理爬取文件

proxies/test_proxies.py：ip代理测试文件

proxies/my_proxies.txt：用户ip代理

proxies/https_proxy_pool.txt：爬取的ip代理

sql/mybilbili.sql：数据库文件

visualization/visualization.ipynb：数据可视化文件

## 使用说明：
创建用户数据库，配置数据库连接信息，使用mybilibili.py进行爬取，最后使visualization.ipynb进行用户数据可视化；

爬取日志保存在logs.txt中可以当前爬取进度以及用户条目爬取错误日志；

可以使用get_proxies.py爬取互联网上公开IP代理，加快用户爬虫速度，也可以在my_proxies.py中使用的自己的代理。
