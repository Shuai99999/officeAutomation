import requests
import json
import sys
import subprocess

sys.path.insert(0, sys.path[0] + "/../credential")
from credential import credential

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
    if procDefName == '数据获取':
        task_url = 'https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/getFormData?taskId=' + taskId
        r_task_detail = requests.get(url=task_url, headers=headers)
        task_details = json.loads(r_task_detail.text)
        task_detail = json.loads(task_details.get('data').get('boData'))
        fileId = task_detail.get('sqlFileId')
        sqlRemarks = task_detail.get('sqlRemarks')
        db_url = task_detail["databaseUrl"]
        db_name = task_detail["databaseName"]

        if '10.246.2.160' in db_name:
            db = 'crm_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:omsexp 密码:7wS&$M7ffGfLdg93，查找文件：'
        elif '10.246.82.162-mysql-4897' in db_name:
            db = 'zlb_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif '10.246.4.51' in db_name:
            db = 'newoms_ods'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:omsexp 密码:7wS&$M7ffGfLdg93，查找文件：'
        elif 'oracle_arch_oms_exp' in db_name:
            db = 'oracle_arch_oms_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:omsexp 密码:7wS&$M7ffGfLdg93，查找文件：'
        elif 'imfs_exp' in db_name:
            db = 'imfs_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:omsexp 密码:7wS&$M7ffGfLdg93，查找文件：'
        elif '4302' in db_name:
            db = 'srm_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:omsexp 密码:7wS&$M7ffGfLdg93，查找文件：'
        elif 'cdkread' in db_name or 'qdr1ksfraub9id' in db_name:
            db = 'cdkread_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:cdkexp 密码:8UytK6Z*toY5，查找文件：'
        elif 'mysql_cdk_auch_exp' in db_name:
            db = 'cdkread_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:cdkexp 密码:8UytK6Z*toY5，查找文件：'
        elif 'mysql_erp_exp' in db_name:
            db = 'mysql_erp_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:cdkexp 密码:8UytK6Z*toY5，查找文件：'
        elif 'oracle_cdk_exp' in db_name:
            db = 'oracle_cdk_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:cdkexp 密码:8UytK6Z*toY5，查找文件：'
        elif 'oracle_cdkbi_exp' in db_name:
            db = 'oracle_cdkbi_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:cdkexp 密码:8UytK6Z*toY5，查找文件：'
        elif 'oracle_vom2_exp' in db_name or 'wloms2' in db_url:
            db = 'oracle_vom2_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:omsexp 密码:7wS&$M7ffGfLdg93，查找文件：'
        elif '10.246.2.96' in db_name:
            db = 'xyc_mycat96_order_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:tmsexp 密码:dSLLg6YLYbRBaFoU，查找文件：'
        elif 'oracle_tms_exp' in db_name:
            db = 'oracle_tms_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:tmsexp 密码:dSLLg6YLYbRBaFoU，查找文件：'
        elif 'i1wms' in db_name:
            db = 'i1wms_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'i2wms' in db_name:
            db = 'i2wms_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'i3wms' in db_name:
            db = 'i3wms_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'iwmsa' in db_name:
            db = 'oracle_iwmsa_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'oracle_i4wms_exp' in db_name:
            db = 'oracle_i4wms_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'oracle_wldtm_exp' in db_name:
            db = 'oracle_wldtm_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'oracle_app_exp' in db_name:
            db = 'oracle_app_exp'
            db_type = 'oracle'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:appexp 密码:fDHub0erCGenMpq*，查找文件：'
        elif 'iwmsdb_exp' in db_name or 'iwms_sysdb_exp' in db_name:
            db = 'iwmsdb_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:iwmsexp 密码:h$6m$LzBZESvwTcr，查找文件：'
        elif 'ldg' in db_name:
            db = 'mycat_bms8066_ldgdb_exp'
            db_type = 'mysql'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:bmsexp 密码:cvh$UhTqVk*eYfHr，查找文件：'
        elif 'sqm' in db_url:
            db = 'sqmprod'
            db_type = 'ob'
            fileInfo = '您的数据已导出，n请登录rrswl导数ftp，打开文件资源管理器（任意文件夹），输入地址 ftp://10.135.30.96/ 输入 用户名:sqmexp 密码:Ya8RNHSk7MO7NIai，查找文件：'
        else:
            db = ''
            db_type = ''
            fileInfo = ''

        if db:
            if fileId:
                fileIdArray = fileId.split(',')
                for fileIdArrayItem in fileIdArray:
                    attach_url = 'https://rrsoa.rrswl.com/uniedp-web/obs/download?ossId=' + fileIdArrayItem + '&token=' + task_token + '&charset=UTF-8'
                    attach = requests.get(attach_url)
                    with open('/home/' + db_type + '/dba/bi/inputs', "wb") as code:
                        # with open('input.txt', "wb") as code:
                        code.write(attach.content)
                    # os.system('read -n 1')

            else:
                sql_text = sqlRemarks
                sql_text = sql_text.encode()
                with open('/home/' + db_type + '/dba/bi/inputs', "wb") as code:
                    code.write(sql_text)

            subprocess.Popen(
                ['su', '-', db_type, '/home/' + db_type + '/dba/bi/multi_exp.sh', db, procBizCode, " > /dev/null &"],
                stdout=subprocess.PIPE)
            print('tail -1 /home/' + db_type + '/dba/bi/rpt')

            agree_url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/taskInst/agree"

            agree_payload = json.dumps({"taskId": taskId,
                                            "data": json.dumps({"applyType": "1", "isConfirm": "1",
                                                                "fileInfo": fileInfo + procBizCode,
                                                                "status": "1"}),
                                            "actionName": "agree", "opinion": "<p>同意</p>",
                                            "end": "true"})
            agree_headers = {
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json, text/plain, */*',
                'token': task_token,
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'host': 'rrsoa.rrswl.com'
            }

            response = requests.request("POST", agree_url, headers=agree_headers, data=agree_payload)

        elif 'impala' in db_url:
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