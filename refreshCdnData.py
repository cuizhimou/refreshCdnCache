#coding:utf-8
import time
import requests
import cdn
import json
import sys


def sendRefresh(version):
    objectPath = "www.guangmangapp.com/api/h5/" + version + "/"
    user_params = {
        "Action": "RefreshDcdnObjectCaches", "ObjectPath": objectPath, "ObjectType": "Directory"
    }
    url = cdn.make_request(user_params)
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        return data
    else:
        print "刷新请求失败", r.status_code, r.content
        return None


def refreshStatus(data):
    user_params = {
        "Action": "DescribeDcdnRefreshTasks", "TaskId": data["RefreshTaskId"]
    }
    while True:
        url = cdn.make_request(user_params)
        r = requests.get(url)
        if r.status_code == 200:
            refreshdata = json.loads(r.content)
            print "刷新对象：{},刷新进度：{}".format(refreshdata["Tasks"]["Task"][0]["ObjectPath"],
                                           refreshdata["Tasks"]["Task"][0]["Process"])
            if refreshdata["Tasks"]["Task"][0]["Status"] != "Complete":
                time.sleep(2)
            else:
                break
        else:
            print "查询状态失败: {}".format(data["RefreshTaskId"])
            break


if __name__ == '__main__':
    ver = sys.argv[1]
    cdn.setup_credentials()
    data = sendRefresh(ver)
    if data != None:
        refreshStatus(data)
