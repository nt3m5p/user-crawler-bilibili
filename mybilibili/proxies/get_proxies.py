import requests
import argparse
import random
from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool as ThreadPool


http_proxy_pool = []
https_proxy_pool = []


def get_xicidaili_proxy(url="https://www.xicidaili.com/nn/", page=1):
    for i in range(1, page+1):
        print('正在解析西刺代理', i)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
        try:
            response = requests.get(url+str(i), headers=headers, timeout=8,)

            html = response.text
            doc = pq(html)
            ip_list = doc('#ip_list')('tr:gt(0)').items()
            for item in ip_list:
                ip = item.find('td:nth-child(2)').text()
                port = item.find('td:nth-child(3)').text()
                http_type = item.find('td:nth-child(6)').text()
                proxy_ip = http_type.lower() + "://" + ip + ":" + port
                if http_type == 'HTTP':
                    if proxy_ip not in http_proxy_pool:
                        http_proxy_pool.append(proxy_ip)
                elif http_type == 'HTTPS':
                    if proxy_ip not in https_proxy_pool:
                        https_proxy_pool.append(proxy_ip)
        except Exception as e:
            print(e)


def delete_proxy(http_type, proxy):
    try:
        if http_type == "http":
            http_proxy_pool.remove(proxy)
        else:
            https_proxy_pool.remove(proxy)
    except Exception as e:
        print(e)


def detect_proxy(proxy):

    http_type = proxy.split(":")[0]
    test_url = http_type + "://www.baidu.com/"
    proxies = {http_type: proxy}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}

    try:
        response = requests.get(test_url, proxies=proxies,
                                headers=headers, timeout=5)
        if response.status_code in [200]:
            print('代理可用', proxy)
        else:
            print('代理不可用', proxy)
            delete_proxy(http_type, proxy)
    except(requests.exceptions.ProxyError, requests.exceptions.RequestException):
        print('代理不可用', proxy)
        delete_proxy(http_type, proxy)


def write_proxies(http_type):
    file = open(http_type + '_proxy_pool.txt', 'w')
    if http_type == 'http':
        for p in http_proxy_pool:
            file.write(p)
            file.write('\n')
    else:
        for p in https_proxy_pool:
            file.write(p)
            file.write('\n')
    file.close()


def read_proxies(http_type):
    file = open(http_type + '_proxy_pool.txt', 'r')
    line = file.readline()
    while line:
        if http_type == 'http':
            http_proxy_pool.append(line.strip('\n'))
        else:
            https_proxy_pool.append(line.strip('\n'))
        line = file.readline()
    file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--http_type', default='http')
    parser.add_argument('-o', '--operate', default='update')
    parser.add_argument('-p', '--page', default='10', type=int)
    args = parser.parse_args()

    try:
        read_proxies(args.http_type)
    except:
        print('没有找到文件')

    if args.operate == 'append':
        get_xicidaili_proxy(page=args.page)
    elif args.operate == 'update':
        pass
    else:
        exit

    pool = ThreadPool(13)
    try:
        if args.http_type == 'http':
            pool.map(detect_proxy, http_proxy_pool)
        else:
            pool.map(detect_proxy, https_proxy_pool)
    except Exception as e:
        print(e)
    pool.close()
    pool.join()

    write_proxies(args.http_type)


if __name__ == '__main__':
    main()
