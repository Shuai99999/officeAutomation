import requests
import json
import re
import datetime
import time
import subprocess
import sys

sys.path.insert(0, sys.path[0] + "/../credential")
from credential import credential

databseDict = {'1169-10.246.82.135-mysql-4614': ['1169-10.246.80.5-mysql-4614'],
               '1169-10.246.82.124-mysql-4238': ['1169-10.246.80.13-mysql-4238'],
               '1169-10.246.82.196-mysql-4628': ['1169-10.246.80.22-mysql-4628'],
               '1169-10.246.82.201-mysql-4750': ['1169-10.246.80.5-mysql-4750'],
               '1169-10.246.82.218-mysql-4799': ['1169-10.246.80.21-mysql-4799'],
               '1169-10.246.82.186-mysql-4760': ['1169-10.246.80.20-mysql-4760', '1169-10.246.80.17-mysql-4760'],
               '1169-10.246.82.152-mysql-4291': ['1169-10.246.80.14-mysql-4291', '1169-10.246.80.22-mysql-4291'],
               '1169-10.246.82.179-mysql-4342': ['1169-10.246.80.13-mysql-4342', '1169-10.246.80.21-mysql-4342'],
               '1169-10.246.82.211-mysql-4657': ['1169-10.246.80.13-mysql-4657', '1169-10.246.80.19-mysql-4657'],
               '1169-10.246.82.241-mysql-4956': ['1169-10.246.80.14-mysql-4956', '1169-10.246.80.26-mysql-4956'],
               '1169-10.246.82.161-mysql-4782': ['1169-10.246.80.17-mysql-4782', '1169-10.246.80.18-mysql-4782'],
               '1169-10.246.82.191-mysql-4267': ['1169-10.246.80.17-mysql-4267', '1169-10.246.80.24-mysql-4267'],
               '1169-10.246.82.183-mysql-4961': ['1169-10.246.80.14-mysql-4961', '1169-10.246.80.27-mysql-4961'],
               '1169-10.246.82.184-mysql-4922': ['1169-10.246.80.4-mysql-4922'],
               '1169-10.246.82.230-mysql-4509': ['1169-10.246.80.3-mysql-4509'],
               '1169-10.246.82.234-mysql-4172': ['1169-10.246.80.18-mysql-4172'],
               '1169-10.246.82.111-mysql-4213': ['1169-10.246.80.38-mysql-4213'],
               '1169-10.246.82.113-mysql-4479': ['1169-10.246.80.10-mysql-4479'],
               '1169-10.246.82.108-mysql-4949': ['1169-10.246.80.19-mysql-4949'],
               '1169-10.246.82.109-mysql-4397': ['1169-10.246.80.4-mysql-4397'],
               '1169-10.246.82.112-mysql-4640': ['1169-10.246.80.1-mysql-4640'],
               '1169-10.246.82.110-mysql-4148': ['1169-10.246.80.21-mysql-4148'],
               '1169-10.246.82.199-mysql-4908': ['1169-10.246.80.18-mysql-4908'],
               '1169-10.246.82.127-mysql-4630': ['1169-10.246.80.15-mysql-4630'],
               '1169-10.246.82.153-mysql-4317': ['1169-10.246.80.16-mysql-4317'],
               '1169-10.246.82.168-mysql-4439': ['1169-10.246.80.18-mysql-4439'],
               '1169-10.246.82.226-mysql-4151': ['1169-10.246.80.18-mysql-4151'],
               '1169-10.246.82.169-mysql-4242': ['1169-10.246.80.40-mysql-4242'],
               '1169-10.246.82.188-mysql-4369': ['1169-10.246.80.23-mysql-4369'],
               '1169-10.246.82.104-mysql-4523': ['1169-10.246.80.9-mysql-4523'],
               '1169-10.246.82.248-mysql-4212': ['1169-10.246.80.15-mysql-4212'],
               '1169-10.246.82.208-mysql-4473': ['1169-10.246.80.6-mysql-4473'],
               '1169-10.246.82.120-mysql-4392': ['1169-10.246.80.8-mysql-4392'],
               '1169-10.246.82.177-mysql-4859': ['1169-10.246.80.3-mysql-4859'],
               '1169-10.246.82.238-mysql-4159': ['1169-10.246.80.4-mysql-4159'],
               '1169-10.246.82.139-mysql-4263': ['1169-10.246.80.23-mysql-4263'],
               '1169-10.246.82.203-mysql-4629': ['1169-10.246.80.41-mysql-4629'],
               '1169-10.246.82.225-mysql-4255': ['1169-10.246.80.13-mysql-4255'],
               '1169-10.246.82.133-mysql-4653': ['1169-10.246.80.6-mysql-4653'],
               '1169-10.246.82.220-mysql-4569': ['1169-10.246.80.48-mysql-4569', '1169-10.246.80.47-mysql-4569'],
               '1169-10.246.82.246-mysql-4171': ['1169-10.246.80.44-mysql-4171', '1169-10.246.80.43-mysql-4171'],
               '1169-10.246.82.137-mysql-4277': ['1169-10.246.80.46-mysql-4277', '1169-10.246.80.45-mysql-4277'],
               '1169-10.246.82.209-mysql-4593': ['1169-10.246.80.49-mysql-4593', '1169-10.246.80.50-mysql-4593'],
               '1169-10.246.82.157-mysql-4005': ['1169-10.246.80.3-mysql-4005'],
               '1169-10.246.82.205-mysql-4188': ['1169-10.246.80.50-mysql-4188', '1169-10.246.80.49-mysql-4188'],
               '1169-10.246.82.237-mysql-4077': ['1169-10.246.80.46-mysql-4077', '1169-10.246.80.45-mysql-4077'],
               '1169-10.246.82.125-mysql-4550': ['1169-10.246.80.43-mysql-4550', '1169-10.246.80.44-mysql-4550'],
               '1169-10.246.82.193-mysql-4515': ['1169-10.246.80.47-mysql-4515', '1169-10.246.80.48-mysql-4515'],
               '1169-10.246.82.118-mysql-4092': ['1169-10.246.80.11-mysql-4092'],
               '1169-10.246.82.239-mysql-4974': ['1169-10.246.80.3-mysql-4974'],
               '1169-10.246.82.105-mysql-4302': ['1169-10.246.80.9-mysql-4302'],
               '1169-10.246.82.228-mysql-4149': ['1169-10.246.80.23-mysql-4149'],
               '1169-10.246.82.158-mysql-4049': ['1169-10.246.80.6-mysql-4049'],
               '1169-10.246.82.231-mysql-4116': ['1169-10.246.80.7-mysql-4116'],
               '1169-10.246.82.131-mysql-4802': ['1169-10.246.80.9-mysql-4802'],
               '1169-10.246.82.154-mysql-4353': ['1169-10.246.80.35-mysql-4353'],
               '1169-10.246.82.190-mysql-4570': ['1169-10.246.80.20-mysql-4570'],
               '1169-10.246.82.162-mysql-4897': ['1169-10.246.80.3-mysql-4897'],
               '1169-10.246.82.114-mysql-4971': ['1169-10.246.80.8-mysql-4971', '1169-10.246.80.6-mysql-4971'],
               '1169-10.246.82.115-mysql-4913': ['1169-10.246.80.10-mysql-4913', '1169-10.246.80.5-mysql-4913'],
               '1169-10.246.82.175-mysql-4205': ['1169-10.246.80.9-mysql-4205'],
               '1169-10.246.82.163-mysql-4711': ['1169-10.246.80.9-mysql-4711'],
               '1169-10.246.82.223-mysql-4861': ['1169-10.246.80.39-mysql-4861'],
               '1169-10.246.82.251-mysql-4666': ['1169-10.246.80.40-mysql-4666'],
               '1169-10.246.82.178-mysql-4264': ['1169-10.246.80.28-mysql-4264'],
               '1169-10.246.82.204-mysql-4717': ['1169-10.246.80.7-mysql-4717']}

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
        # taskId = taskviewurl[taskviewurl.find("kId=") + 4:]
        tmp_taskId = taskviewurl[taskviewurl.find("kId=") + 4:]
        if '&' in tmp_taskId:
            taskId = tmp_taskId[0:tmp_taskId.find('&')]
        else:
            taskId = tmp_taskId

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
                                subprocess.Popen(
                                    ['su', '-', 'oracle', '/home/oracle/dba/pum.sh', assetName, accountName],
                                    stdout=subprocess.PIPE)
                                print('分配oracle权限: ' + assetName + ' ' + accountName)
                            elif 'mysql' in assetName:
                                if assetName in databseDict.keys():
                                    subprocess.Popen(
                                        ['su', '-', 'mysql', '/home/mysql/dba/pum.sh', assetName, accountName],
                                        stdout=subprocess.PIPE)
                                    for slaveAssetName in databseDict[assetName]:
                                        subprocess.Popen(
                                            ['su', '-', 'mysql', '/home/mysql/dba/pum_nodb.sh', slaveAssetName, accountName],
                                            stdout=subprocess.PIPE)
                                    print('分配MySQL权限: ' + assetName + ' ' + accountName)
                                else:
                                    subprocess.Popen(
                                        ['su', '-', 'mysql', '/home/mysql/dba/pum.sh', assetName, accountName],
                                        stdout=subprocess.PIPE)

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
                        '审批日期: ' + current_time + '; instId: ' + instId + '; taskId: ' + taskId + '; 申请人: ' + accountName + '; 申请数据库清单: ' + str(
                            assetSet))
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
