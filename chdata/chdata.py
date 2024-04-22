import time

import requests
import json
import subprocess
import datetime

credential = "eyJzdWJqZWN0IjoiMDE0NTQyMjEiLCJwYXNzd29yZCI6ImQybHVaRzkzYzBBeE1nPT0iLCJ0eXBlIjoxfQ%3D%3D"
iam_token_url = "https://iama.haier.net/api/oauth/authorize?client_id=cb3b02710dd7ebd0b10762405121d418&credential=" + credential + "&loginType=2&redirect_uri=https%3A%2F%2Frrsoa.rrswl.com%2Fuuc.html%3F%24%24query%24%24eyJyZWRpcmVjdCI6ImluZGV4In0%40%40%24%24end%24%24"

iam_token_payload = {}
iam_token_headers = {
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'languageEnv': 'cn',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Content-Type': 'application/json;charset=utf-8',
    'Accept': 'application/json, text/plain, */*',
    'Application-Key': 'cb3b02710dd7ebd0b10762405121d418',
    'sec-ch-ua-platform': '"Windows"',
    'host': 'iama.haier.net'
}

iam_token_get = requests.get(iam_token_url, headers=iam_token_headers, data=iam_token_payload)

iam_token = json.loads(iam_token_get.text)

iam_token = iam_token.get('data').get('access_token')

token_url = "https://rrsoa.rrswl.com/uniedp-web/open/api/authLogin/authToken"

token_payload = json.dumps({
    "accessToken": iam_token
})

token_headers = {
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"'
}

task_token = requests.request("POST", token_url, headers=token_headers, data=token_payload)

task_token = json.loads(task_token.text)

task_token = task_token.get('data').get('token')

headers = {
    'Host': 'rrsoa.rrswl.com',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Connection': 'keep-alive',
    'Content-Type': "application/json",
    'Referer': 'https://rrsoa.rrswl.com',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    'Token': task_token,
}

url = 'https://rrsoa.rrswl.com/uniedp-web/oa/flowable/processInst/page?order=&orderField=&sumFields=&page=1&limit=1000&source=todo-1&formCode=&formName=&procTitle=&procName=&beginDateStr=&endDateStr=&status=&startBy='

todo_list_url = requests.get(url=url, headers=headers)

todo_list = json.loads(todo_list_url.text)

for i in todo_list.get('data').get('list'):
    taskId = i.get('taskId')
    instId = i.get('procInstId')
    procBizCode = i.get('procBizCode')
    procDefName = i.get('procDefName')

    if procDefName == '数据变更':

        task_url = 'https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/getFormData?taskId=' + taskId

        r_task_detail = requests.get(url=task_url, headers=headers)

        task_details = json.loads(r_task_detail.text)

        task_detail = json.loads(task_details.get('data').get('boData'))
        fileId = task_detail.get('fileId')
        sqlRemarks = task_detail.get('sqlRemarks')

        if fileId:

            attach_url = 'https://rrsoa.rrswl.com/uniedp-web/obs/download?ossId=' + fileId + '&token=' + task_token + '&charset=UTF-8'

            attach = requests.get(attach_url)

            with open('/home/oracle/dba/prod/input', "wb") as code:
                code.write(attach.content)

        else:
            sql_text = task_detail["applyRemark"]
            sql_text = sql_text.encode()
            with open('/home/oracle/dba/prod/input', "wb") as code:
                code.write(sql_text)

        db_name = task_detail["databaseAddress"]

        if 'cdk' in db_name and 'mysql' not in db_name:
            db = 'cdk_pr'
        elif 'rckdb' in db_name:
            db = 'cdk_pr'
        elif 'sqm' in db_name:
            db = 'sqm_pr'
        elif 'iwmspf' in db_name:
            db = 'iwmspf_pr'
        elif 'i1wms' in db_name:
            db = 'i1wms_pr'
        elif 'i2wms' in db_name:
            db = 'i2wms_pr'
        elif 'i3wms' in db_name:
            db = 'i3wms_pr'
        elif 'rrslesdb' in db_name:
            db = 'i2wms_pr'
        elif 'rrswldb' in db_name:
            db = 'i1wms_pr'
        elif 'wloms2' in db_name:
            db = 'oms2_pr'
        elif 'wloms1' in db_name:
            db = 'oms1_pr'
        elif '10.133.28.7' in db_name:
            db = 'tms_pr'
        elif '10.135.17.94' in db_name:
            db = 'app_pr'
        elif 'iwmsa' in db_name:
            db = 'iwmsa_rac'
        elif 'huyi' in db_name:
            db = 'huyi'
        elif 'kuajing' in db_name:
            db = 'haierkuajing'
        elif 'hubwms' in db_name.lower():
            db = 'hubwms'
        elif 'rrswlhr' in db_name:
            db = 'rrswlhr'
        else:
            db = ''

        if db:
            subprocess.Popen(['su', '-', 'oracle', '/home/oracle/dba/prod/chdata.sh', db], stdout=subprocess.PIPE)

            agree_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/agree"
            agree_headers = {
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, */*',
                'token': task_token,
                'sec-ch-ua-platform': '"Windows"',
                'host': 'rrsoa.rrswl.com'
            }

            payload = {
                "opinion": "<p>同意</p>",
                "end": "true",
                "taskId": taskId}

            agree_payload = json.dumps(payload)

            response = requests.request("POST", agree_url, headers=agree_headers, data=agree_payload)

            now = datetime.datetime.now()

            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' 任务：' + procBizCode + '审批成功')

        elif '10.246.4.51' in db_name:
            trans_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/doNotice"

            trans_payload = {"taskId": taskId, "instId": instId, "submitFlag": "noSubmit",
                             "noticeUserIds": "20114316", "opinion": "<p>转发归档任务</p>"}
            trans_headers = {
                'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, */*',
                'token': task_token,
                'sec-ch-ua-platform': '"Windows"',
                'host': 'rrsoa.rrswl.com'
            }

            response_trans = requests.request("POST", trans_url, headers=trans_headers, data=trans_payload)

            time.sleep(5)

            agree_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/agree"
            agree_headers = {
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, */*',
                'token': task_token,
                'sec-ch-ua-platform': '"Windows"',
                'host': 'rrsoa.rrswl.com'
            }

            payload = {
                "opinion": "<p>同意</p>",
                "end": "true",
                "taskId": taskId}

            agree_payload = json.dumps(payload)

            response = requests.request("POST", agree_url, headers=agree_headers, data=agree_payload)

            now = datetime.datetime.now()

            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' 任务：' + procBizCode + '转发并审批成功')

        else:
            now = datetime.datetime.now()
            print(now.strftime(
                '%Y-%m-%d %H:%M:%S') + ' 任务：' + procBizCode + '未执行，原因：数据库地址' + db_name + '在清单中不存在，请添加')

    if procDefName == '数据获取':
        task_url = 'https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/getFormData?taskId=' + taskId

        r_task_detail = requests.get(url=task_url, headers=headers)

        task_details = json.loads(r_task_detail.text)

        task_detail = json.loads(task_details.get('data').get('boData'))
        fileId = task_detail.get('fileId')
        sqlRemarks = task_detail.get('sqlRemarks')
        if sqlRemarks == '数据已导出，无需重复导。':
            agree_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/agree"
            agree_headers = {
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, */*',
                'token': task_token,
                'sec-ch-ua-platform': '"Windows"',
                'host': 'rrsoa.rrswl.com'
            }

            payload = {
                "opinion": "<p>同意</p>",
                "end": "true",
                "taskId": taskId}

            agree_payload = json.dumps(payload)

            response = requests.request("POST", agree_url, headers=agree_headers, data=agree_payload)

            now = datetime.datetime.now()

            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' 任务：' + procBizCode + '审批成功')