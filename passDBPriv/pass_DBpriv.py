import requests
import json
import re
import datetime
import time
import subprocess
import sys
sys.path.insert(0, sys.path[0]+"/../credential")
from credential import credential

# credential = "eyJzdWJqZWN0IjoiMDE0NTQyMjEiLCJwYXNzd29yZCI6ImQybHVaRzkzYzBBeE1nPT0iLCJ0eXBlIjoxfQ%3D%3D"
token_url = "https://iama.haier.net/api/oauth/authorize?client_id=4dc643c5890060f8191edbf6e746db88&credential=" + credential + "&response_type=code&loginType=2&redirect_uri=https%3A%2F%2Ftechless.haier.net%2Fbpmsportal"

token_payload = {}
token_headers = {
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'languageEnv': 'cn',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Content-Type': 'application/json;charset=utf-8',
    'Accept': 'application/json, text/plain, */*',
    'Application-Key': '4dc643c5890060f8191edbf6e746db88',
    'sec-ch-ua-platform': '"Windows"',
    'host': 'iama.haier.net'
}

iam_token_get = requests.request("GET", token_url, headers=token_headers, data=token_payload)

# print(response.text)

iam_token = json.loads(iam_token_get.text)

iam_token = iam_token.get('data').get('access_token')

url = "https://bpms-portal.haier.net/flowportal/flow/list"

payload = "{\"cn\":\"01454221\",\"typeCode\":\"YLYURCAUTH3451QHD8T\",\"type\":\"runtime\",\"size\":100,\"current\":1}"
headers = {
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'Access-Token': iam_token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'host': 'bpms-portal.haier.net'
}

def is_8_digit_number(s):
    return bool(re.match(r'\d{8}', s))

def is_A7_digit_number(s):
    return bool(re.match(r'A\d{7}', s))
def agree_fuc():
    agree_url = "https://aqzxlc.haier.net/S03269/process/complete"

    agree_payload = {"instanceId": "" + instId + "", "plat": "runtime", "taskId": "" + taskId + "",
                     "actionName": "pass", "opinion": "同意"}

    agree_payload = json.dumps(agree_payload)
    agree_headers = {
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'Access-Token': iam_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'host': 'aqzxlc.haier.net'
    }
    agree = requests.request("POST", agree_url, headers=agree_headers, data=agree_payload)


def disagree_fuc():
    disagree_url = "https://aqzxlc.haier.net/S03269/process/complete"

    disagree_headers = {
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'Access-Token': iam_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'host': 'aqzxlc.haier.net'
    }

    disagree = requests.request("POST", disagree_url, headers=disagree_headers, data=disagree_payload)
    # print(t_apply_user + '：不同意')

to_do_list = requests.request("POST", url, headers=headers, data=payload)

todo_list = json.loads(to_do_list.text)
for i in todo_list.get('data').get('records'):
    tempTile = i.get('tempTile')
    taskviewurl = i.get('taskviewurl')
    initorName = i.get('initorName')
    if '特权数据库账号申请流程' in tempTile:
        taskviewurl = taskviewurl[taskviewurl.find("?") + 1:].replace('i', 'I')
        instId = taskviewurl[taskviewurl.find("eId=") + 4:taskviewurl.find("&")]
        taskId = taskviewurl[taskviewurl.find("kId=") + 4:]

        task_url = "https://aqzxlc.haier.net/S03269/process/form_data?process" + taskviewurl
        task_payload = {}
        task_headers = {
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=utf-8',
            'sec-ch-ua-mobile': '?0',
            'Access-Token': iam_token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'host': 'aqzxlc.haier.net'
        }
        apply_input = requests.request("GET", task_url, headers=task_headers, data=task_payload)

        apply_input = json.loads(apply_input.text)

        print(apply_input)

        applyReason = apply_input.get('data').get('input').get('applyReason')
        applyType = apply_input.get('data').get('input').get('applyType')
        applyInfoList = apply_input.get('data').get('input').get('applyInfoList')

        assetSet = set()
        accountSet = set()
        if applyReason == '1':
            node_url = "https://aqzxlc.haier.net/S03269/process/node_opinion?instId=" + instId + "&plat=runtime"

            node_payload = {}
            node_headers = {
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'Access-Token': iam_token,
                'sec-ch-ua-platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'host': 'aqzxlc.haier.net'
            }

            nodes = requests.request("GET", node_url, headers=node_headers, data=node_payload)

            nodes = json.loads(nodes.text)
            node_in_opin = nodes.get('data').get('opinions')
            opin_userList = []
            isGrant = False
            for i in node_in_opin:
                opin_userId = i.get('userId')
                if opin_userId == '01508330':
                    isGrant = True
            if applyType == '1':
                disagree_payload = {"instanceId": "" + instId + "",
                                    "taskId": "" + taskId + "",
                                    "actionName": "unPass",
                                    "opinion": "不同意 不要申请DBA权限。"}
                disagree_payload = json.dumps(disagree_payload)
                disagree_fuc()
            elif applyType == '0':
                for assetInfo in applyInfoList:
                    # print(assetInfo)
                    assetName = assetInfo.get('assetName')
                    accountName = assetInfo.get('accountName')
                    userAccount = assetInfo.get('userAccount')
                    if is_A7_digit_number(accountName) or is_A7_digit_number(userAccount):
                        disagree_payload = {"instanceId": "" + instId + "",
                                            "taskId": "" + taskId + "",
                                                    "actionName": "unPass",
                                                    "opinion": "不同意 供应商不能申请数据库账号。"}
                        disagree_payload = json.dumps(disagree_payload)
                        disagree_fuc()
                    if is_8_digit_number(accountName):
                        if accountName != userAccount:
                            disagree_payload = {"instanceId": "" + instId + "",
                                                "taskId": "" + taskId + "",
                                                "actionName": "unPass",
                                                "opinion": "不同意 申请账号和使用账号不一致。"}
                            disagree_payload = json.dumps(disagree_payload)
                            disagree_fuc()
                        elif isGrant == True:
                            agree_fuc()
                            time.sleep(10)
                            if 'oracle' in assetName:
                                subprocess.Popen(['su', '-', 'oracle', '/home/oracle/dba/pum.sh', assetName, accountName],
                                             stdout=subprocess.PIPE)
                                print('分配oracle权限: ' + assetName + ' ' + accountName)
                            elif 'mysql' in assetName:
                                subprocess.Popen(
                                    ['su', '-', 'mysql', '/home/mysql/dba/pum.sh', assetName, accountName],
                                    stdout=subprocess.PIPE)
                                print('分配MySQL权限: ' + assetName + ' ' + accountName)
                        else:
                            agree_fuc()
                    if '10.135.30.96' in assetInfo:
                        disagree_payload = {"instanceId": "" + instId + "",
                                            "taskId": "" + taskId + "",
                                            "actionName": "unPass",
                                            "opinion": "不同意 归档库直接申请arch_ro的使用权限就行，不要新建账号。"}
                        disagree_payload = json.dumps(disagree_payload)
                        disagree_fuc()

                    assetSet.add(assetName)
                    accountSet.add(accountName)
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('数据库权限审批记录.txt', "a") as code:
                    code.write(
                        '审批日期: ' + current_time + '; instId: ' + instId + '; taskId: ' + taskId + '; 申请人: ' + accountName + '; 申请数据库清单: ' + str(assetSet))
                    code.write('\n')
                # print(assetSet)
                # print(accountSet)

        if applyReason == '0':
            if applyType == '1':
                disagree_payload = {"instanceId": "" + instId + "",
                                    "taskId": "" + taskId + "",
                                    "actionName": "unPass",
                                    "opinion": "不同意 不要申请DBA权限。"}
                disagree_payload = json.dumps(disagree_payload)
                disagree_fuc()
            elif applyType == '0':
                isPass = True
                for assetInfo in applyInfoList:
                    # print(assetInfo)
                    accountName = assetInfo.get('accountName')
                    userAccount = assetInfo.get('userAccount')
                    if accountName != userAccount and accountName != 'arch_ro':
                        isPass = False
                if isPass:
                    agree_fuc()
                else:
                    disagree_payload = {"instanceId": "" + instId + "",
                                        "taskId": "" + taskId + "",
                                        "actionName": "unPass",
                                        "opinion": "不同意 账号名和使用人不一致。"}
                    disagree_payload = json.dumps(disagree_payload)
                    disagree_fuc()
