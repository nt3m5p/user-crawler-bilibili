import requests
import random


def detect_proxy(proxy):
    #test_url = "https://api.bilibili.com/x/space/acc/info?mid=123&jsonp=jsonp"
    test_url = "http://www.baidu.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "Referer": "https://space.bilibili.com/123456?from=search&seid=41235155151"
    }
    try:
        response = requests.get(test_url,
                                proxies=proxy,
                                headers=headers,
                                timeout=8)
        if response.status_code in [200]:
            print('代理可用', proxy)
        else:
            print('代理不可用', proxy)
    except Exception as e:
        print(e)
        print('代理不可用', proxy)


def LoadUserProxies(upfile):
    ups = []
    with open(upfile, "r") as upf:
        for up in upf.readlines():
            if up:
                item = up.strip()
                ups.append({"https": item})
    ups.append({None:None})
    random.shuffle(ups)
    return ups


ups = LoadUserProxies("http_proxy_pool.txt")
print("Http proxy pool:")
for p in ups:
    detect_proxy(p)

# ups = LoadUserProxies("proxies/my_proxies.txt")
# print(ups)
# print("My proxies:")
# for p in ups:
#     detect_proxy(p)
