import requests
import json
import random
import pymysql
import sys
import logging
import traceback
import time
from importlib import reload
from multiprocessing.dummy import Pool as ThreadPool

reload(sys)

logger = logging.getLogger(__name__)
handler = logging.FileHandler("logs.txt")
handler.setLevel(logging.CRITICAL)
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(handler)


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, "rb") as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


def LoadUserProxies(upfile):
    ups = []
    with open(upfile, "r") as upf:
        for up in upf.readlines():
            if up:
                item = up.strip()
                ups.append({"https": item})
    ups.append({None: None})
    random.shuffle(ups)
    return ups


def give_up_proxy(up):
    if error_ups.get(up):
        error_ups[up] += 1
    else:
        error_ups[up] = 1
    for ep in error_ups.keys():
        if error_ups.get(ep) >= 20:
            logger.critical("error ups:" + str(ep))
            logger.critical(error_ups)
            try:
                ups.remove({"https": ep})
            except:
                pass


def getsource(mid):
    ua = random.choice(uas)
    head = {"User-Agent": ua,
            "Referer": "https://space.bilibili.com/" + str(mid) + "?from=search&seid=" + 
            str(random.randint(100000000000, 500000000000))}

    for t in range(5):
        try:
            up = random.choice(ups)
            info = requests.session().get("https://api.bilibili.com/x/space/acc/info?mid=" +
                                          str(mid) + "&jsonp=jsonp", headers=head,  proxies=up,  timeout=8)
            if info.status_code in [200]:
                break
            give_up_proxy(up.get("https"))
        except Exception:
            traceback.print_exc()
            print("error proxy:", up)
            give_up_proxy(up.get("https"))
        if t == 4:
            print(mid, "blocked frequently, see error proxies in logs.txt")
            sys.exit()

    info = info.json()
    if info.get("data"):
        print(mid, "got date")
        try:
            info_data = info.get("data")
            mid = info_data.get("mid")
            name = info_data.get("name")
            sex = info_data.get("sex")
            face = info_data.get("face")
            sign = info_data.get("sign")
            urank = info_data.get("rank")
            level = info_data.get("level")
            birthday = info_data.get("birthday")
            fans_badge = info_data.get("fans_badge")
            official = info_data.get("official")
            official_role = official.get("role")
            official_title = official.get("title")
            official_desc = official.get("desc")
            official_type = official.get("type")
            vip = info_data.get("vip")
            vip_type = vip.get("type")
            vip_status = vip.get("status")

            try:
                tags = requests.get(
                    "https://api.bilibili.com/x/space/acc/tags?mid=" + str(mid) + "&jsonp=jsonp", headers=head, proxies=up, timeout=8).json()
                tags = tags["data"][0]["tags"]
            except Exception:
                tags = []

            try:
                stat = requests.get(
                    "https://api.bilibili.com/x/relation/stat?vmid=" + str(mid) + "&jsonp=jsonp", headers=head, proxies=up, timeout=8).json()
                following = stat["data"]["following"]
                fans = stat["data"]["follower"]
            except Exception:
                following = 0
                fans = 0

            try:
                upstat = requests.get(
                    "https://api.bilibili.com/x/space/upstat?mid=" + str(mid) + "&jsonp=jsonp&callback=__jp5", headers=head, proxies=up, timeout=8).text
                upstat = json.loads(upstat.replace("__jp5(", "")[:-1])
                archiveview = upstat["data"]["archive"]["view"]
                article = upstat["data"]["article"]["view"]
                likes = upstat["data"]["likes"]
            except Exception:
                archiveview = 0
                article = 0
                likes = 0

            try:
                navnum = requests.get(
                    "https://api.bilibili.com/x/space/navnum?mid=" + str(mid) + "&jsonp=jsonp", headers=head, proxies=up, timeout=8).json()
                video = navnum["data"]["video"]
            except Exception:
                video = 0
            try:
                conn = pymysql.connect(
                    host="localhost", user="root", passwd="password", db="mybilibili", charset="utf8")
                cur = conn.cursor()
                sql = "INSERT INTO bilibili_user_info(mid, name, sex, face, sign, urank, level, birthday, \
                    fans_badge, official_role, official_title, official_desc, official_type, \
                    vip_type, vip_status, tags, following, fans ,archiveview, article, likes, video) \
                    VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\
                        \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (
                    mid, name, sex, face, sign, urank, level, birthday, fans_badge, official_role, official_title, official_desc, 
                    official_type, vip_type, vip_status, tags, following, fans, archiveview, article, likes, video)
                cur.execute(sql)
                conn.commit()
            except Exception:
                pass

        except Exception:
            traceback.print_exc()

    else:
        print(mid, "no data")
        time.sleep(0.3)


uas = LoadUserAgents("agent_pool.txt")
#ups = LoadUserProxies("proxies/https_proxy_pool.txt")
ups = LoadUserProxies("proxies/my_proxies.txt")

error_ups = {}


if __name__ == "__main__":
    start = 354
    stride = 10000

    while start < 1000:
        logger.critical("%s-%s started" % (start*stride, (start+1)*stride))
        mids_list = list(range(start*stride, (start+1) * stride))
        error_ups = {}

        pool = ThreadPool(4)
        try:
            results = pool.map(getsource, mids_list)
        except Exception as e:
            traceback.print_exc()
        pool.close()
        pool.join()

        conn = pymysql.connect(
            host="localhost", user="root", passwd="password", db="mybilibili", charset="utf8")
        cur = conn.cursor()
        sql = "select count(*) from bilibili_user_info where  %s < mid and mid < %s " % (
            start*stride, (start+1) * stride)
        cur.execute(sql)
        results = cur.fetchall()[0][0]
        logger.critical("%s-%s finished, %s/%s updated" %
                        (start*stride, (start+1)*stride, results, stride))
        start += 1

