import time
import requests
import json
import subprocess
import datetime
import sys
# sys.path.append("../credential")
sys.path.insert(0, sys.path[0]+"/../credential")
from credential import credential_gaoshuai
from credential import credential_diaowentao
from credential import credential


# for credential in credential_gaoshuai, credential_diaowentao:
# for credential in credential_gaoshuai:
# credential = "eyJzdWJqZWN0IjoiMDE0NTQyMjEiLCJwYXNzd29yZCI6ImQybHVaRzkzYzBBeE1nPT0iLCJ0eXBlIjoxfQ%3D%3D"
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
    instId = i.get('id')
    procBizCode = i.get('procBizCode')
    procDefName = i.get('procDefName')

    if procDefName == '数据变更':

        task_url = 'https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/getFormData?taskId=' + taskId

        r_task_detail = requests.get(url=task_url, headers=headers)

        task_details = json.loads(r_task_detail.text)

        task_detail = json.loads(task_details.get('data').get('boData'))
        fileId = task_detail.get('fileId')
        sqlRemarks = task_detail.get('sqlRemarks')

        db_name = task_detail["databaseAddress"]

        db_type = 'mysql'

        if 'cdk' in db_name and 'mysql' not in db_name:
            db = 'cdk_pr'
            db_type = 'oracle'
        elif 'rckdb' in db_name:
            db = 'cdk_pr'
            db_type = 'oracle'
        elif 'sqm' in db_name:
            db = 'sqm_pr'
            db_type = 'oracle'
        elif 'iwmspf' in db_name:
            db = 'iwmspf_pr'
            db_type = 'oracle'
        elif 'i1wms' in db_name:
            db = 'i1wms_pr'
            db_type = 'oracle'
        elif 'i2wms' in db_name:
            db = 'i2wms_pr'
            db_type = 'oracle'
        elif 'i3wms' in db_name:
            db = 'i3wms_pr'
            db_type = 'oracle'
        elif 'rrslesdb' in db_name:
            db = 'i2wms_pr'
            db_type = 'oracle'
        elif 'rrswldb' in db_name:
            db = 'i1wms_pr'
            db_type = 'oracle'
        elif 'wloms2' in db_name:
            db = 'oms2_pr'
            db_type = 'oracle'
        elif 'wloms1' in db_name:
            db = 'oms1_pr'
            db_type = 'oracle'
        elif '10.133.28.7' in db_name:
            db = 'tms_pr'
            db_type = 'oracle'
        elif '10.135.17.94' in db_name:
            db = 'app_pr'
            db_type = 'oracle'
        elif 'iwmsa' in db_name:
            db = 'iwmsa_rac'
            db_type = 'oracle'
        elif 'huyi' in db_name:
            db = 'huyi'
            db_type = 'oracle'
        elif 'kuajing' in db_name:
            db = 'haierkuajing'
            db_type = 'oracle'
        elif 'hubwms' in db_name.lower():
            db = 'hubwms'
            db_type = 'oracle'
        elif 'rrswlhr' in db_name:
            db = 'rrswlhr'
            db_type = 'oracle'
        elif '10.246.82.104' in db_name:
            db = 'iwmsdb_master'
            db_type = 'mysql'
        elif 'qdr1ksfraub9id' in db_name:
            db = 'polardb_cdkread_exp'
            db_type = 'mysql'
        elif 'm5en7lf4nppm54ngm7o' in db_name:
            db = 'cdk_auth_nsp_srp_dba'
            db_type = 'mysql'
        elif 'v8z52br84u9zorvskoz4' in db_name:
            db = 'wccyr'
            db_type = 'mysql'
        elif '4897' in db_name:
            db = 'zlb'
            db_type = 'mysql'
        elif 'kxorder' in db_name:
            db = 'mecvwidedba'
            db_type = 'mysql'
        elif '1169-10.246.2.96' in db_name:
            db = 'xyc_mycat96'
            db_type = 'mysql'
        elif 'm5ev2c955pn291133' in db_name:
            db = 'wlhy'
            db_type = 'mysql'
        elif '1169-10.246.82.105-mysql-4302' in db_name:
            db = 'srm'
            db_type = 'mysql'
        elif 'haier12-kxapp.rwlb.rds.aliyuncs.com' in db_name:
            db = 'mecv_dba'
            db_type = 'mysql'
        elif 'crm_bas_db' in db_name:
            db = 'crm_bas_db'
            db_type = 'mysql'
        elif '1169-10.246.2.95-mycat-5066' in db_name:
            db = 'xyc_mycat95_exp'
            db_type = 'mysql'
        elif 'm5ei9xh1l69cg5331do' in db_name:
            db = 'daojia_rds'
            db_type = 'mysql'
        elif 'm5e1a60v8c3hfg6df' in db_name:
            db = 'tms_ddzx_aliyun'
            db_type = 'mysql'
        elif '10.246.82.140:4224' in db_name:
            db = 'diaoyunpt'
            db_type = 'mysql'
        elif 'haier12-prod.mysql.polardb.rds.aliyuncs.com' in db_name:
            db = 'mecv_finextend'
            db_type = 'mysql'
        elif '4802' in db_name:
            db = 'xyc_master3'
            db_type = 'mysql'
        elif '4148' in db_name:
            db = 'crm_receipt_db'
            db_type = 'mysql'
        else:
            db = ''

        if fileId:

            attach_url = 'https://rrsoa.rrswl.com/uniedp-web/obs/download?ossId=' + fileId + '&token=' + task_token + '&charset=UTF-8'

            attach = requests.get(attach_url)

            with open('/home/' + db_type + '/dba/prod/input', "wb") as code:
                code.write(attach.content)

        else:
            sql_text = task_detail["applyRemark"]
            sql_text = sql_text.encode()
            with open('/home/' + db_type + '/dba/prod/input', "wb") as code:
                code.write(sql_text)

        if db:
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
            # subprocess.Popen(['su', '-', 'oracle', '/home/oracle/dba/prod/chdata.sh', db], stdout=subprocess.PIPE)
            try:
                chdata_result = subprocess.check_output(
                    ['su', '-', db_type, '/home/' + db_type + '/dba/prod/chdata.sh', db]).decode('utf-8')
            except subprocess.CalledProcessError as e:
                chdata_result = 'ERROR 1064 (42000) at line 1: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax'

            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' 任务：' + procBizCode + '审批成功，结果：' + chdata_result)

        elif '10.246.4.51' in db_name:
            trans_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/doNotice"

            trans_payload = {"taskId": taskId, "instId": instId, "submitFlag": "noSubmit",
                             "noticeUserIds": "20114316", "opinion": "<p>转发归档任务</p>"}
            trans_payload = json.dumps(trans_payload)

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

        # elif db_name == '1169-10.246.82.104-mysql-4523':
        #     db = 'iwmsdb_master'
        #     subprocess.Popen(['su', '-', 'mysql', '/home/mysql/dba/prod/chdata.sh', db], stdout=subprocess.PIPE)
        #
        #     agree_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/agree"
        #     agree_headers = {
        #         'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        #         'sec-ch-ua-mobile': '?0',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        #         'Content-Type': 'application/json;charset=UTF-8',
        #         'Accept': 'application/json, text/plain, */*',
        #         'token': task_token,
        #         'sec-ch-ua-platform': '"Windows"',
        #         'host': 'rrsoa.rrswl.com'
        #     }
        #
        #     payload = {
        #         "opinion": "<p>同意</p>",
        #         "end": "true",
        #         "taskId": taskId}
        #
        #     agree_payload = json.dumps(payload)
        #
        #     response = requests.request("POST", agree_url, headers=agree_headers, data=agree_payload)
        #
        #     now = datetime.datetime.now()
        #
        #     print(now.strftime('%Y-%m-%d %H:%M:%S') + ' 任务：' + procBizCode + '审批成功')

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
        if sqlRemarks == '数据已导出，无需重复导。' or sqlRemarks == '已通过其他途径导出':
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