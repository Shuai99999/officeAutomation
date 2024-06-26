import requests
import json
import re
import urllib3
import datetime
import sys
sys.path.insert(0, sys.path[0]+"/../credential")
from credential import credential

leader_list = (
    "00002388", "00020213", "00023081", "00023294", "00091916", "00575641", "00575684", "00575808", "00592395",
    "00593200",
    "00594074", "00620594", "00627401", "00930164", "01008707", "01022865", "01024414", "01024434", "01043503",
    "01046999",
    "01047165", "01056906", "01067077", "01075525", "01075732", "01148288", "01158932", "01175700", "01188381",
    "01222067",
    "01324959", "01356647", "01404762", "01409561", "01414905", "01414959", "01422515", "01428652", "01434645",
    "18003735",
    "22025586", "22035823", "23037292", "23039960", "23044496", "00091078", "00100130", "00960539", "00980548",
    "01035368",
    "01075381", "01239581", "01473388", "22036908", "00980949", "00091061", "22000341", "00100195", "00091048",
    "01075601",
    "00013254", "01046981", "01186807", "00575852", "00091087", "00032839", "00981041", "00002288", "00951176",
    "01000233",
    "00012262", "00621683", "01256209", "00620902", "00091006", "00013254", "00602350", "01435749", "00602350", "23050791")

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

def getTitle(employeeId):
    url = "https://ehr.haier.net/ehrportal-api/searchservices/search/searchEmployees?retrieval=" + employeeId + ""

    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=utf-8',
        'sec-ch-ua-mobile': '?0',
        'Access-Token': iam_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'host': 'ehr.haier.net'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    employeeInfo = response.text
    employeeInfo = json.loads(employeeInfo)
    # employeeInfo = employeeInfo.get('data').get('records')[1].get('xwName')
    employeeInfo = employeeInfo.get('data').get('records')
    for i in employeeInfo:
        if i.get('empCode') == employeeId:
            # print(i.get('empCode') + '\t' + i.get('empName') + '\t' + i.get('outTitle'))
            return i.get('outTitle')
def agree_fuc():
    agree_url = "https://aqzxlc.haier.net/S03269/process/complete"

    agree_payload = {"instanceId": "" + instId + "", "plat": "porcess-usb", "taskId": "" + taskId + "",
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

    # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # with open('微信审批记录.txt', "a") as code:
    # # with open('/root/python/pass_wx/approval_record.txt', "a") as code:
    #     code.write('审批日期: ' + current_time + '; instId: ' + instId + '; taskId: ' + taskId + '; 申请人: ' + t_apply_user + '; 所在小微: ' + applyCompany + '; 申请软件: ' + rjxz + '; 审批领导: ' + final_opin_leader + '; 申请原因:' + reason)
    #     code.write('\n')

    http = urllib3.PoolManager()
    response = http.request('GET', file_list_url)
    # with open('\\root\\python\\pass_wx\\audit_pass_pdf\\' + instId + '_' + final_opin_leader +'.pdf', 'wb') as audit_pdf: audit_pdf.write(response.data)

    # print(t_apply_user + '：同意')
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
    # initorName = i.get('initorName')
    if '终端安全防护例外流程' in tempTile:
        taskviewurl = taskviewurl[taskviewurl.find("?") + 1:].replace('i', 'I')
        instId = taskviewurl[taskviewurl.find("eId=") + 4:taskviewurl.find("&")]
        taskId = taskviewurl[taskviewurl.find("kId=") + 4:taskviewurl.find("&", taskviewurl.find("kId=") + 4)]
        # print(tempTile)

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

        reason = apply_input.get('data').get('input').get('reason')

        node_in_reason = re.findall("\d+", reason)

        rjxz = apply_input.get('data').get('input').get('rjxz')

        sqlx = apply_input.get('data').get('input').get('sqlx')

        applyCompany = apply_input.get('data').get('input').get('applyCompany')

        apply_list = apply_input.get('data').get('input').get('applyList')

        file_list = apply_input.get('data').get('input').get('fileList')

        node_url = "https://aqzxlc.haier.net/S03269/process/node_opinion?instId=" + instId + "&plat=porcess-usb"

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

        t_apply_user = nodes.get('data').get('opinions')[0].get('userId')

        if len(reason) < 15 and ('办公' in reason or '需要' in reason or '工作' in reason):
            disagree_payload = {"instanceId": "" + instId + "", "plat": "porcess-usb", "taskId": "" + taskId + "",
                                "actionName": "unPass",
                                "opinion": "不同意 请在备注里详细写明是做什么工作，在什么情况下要给谁用微信沟通什么信息，只写个工作需要的会被打回。"}

            disagree_payload = json.dumps(disagree_payload)

            disagree_fuc()
            print(tempTile + '申请理由太简单')

        elif len(file_list) <= 2:
            disagree_payload = {"instanceId": "" + instId + "", "plat": "porcess-usb", "taskId": "" + taskId + "",
                                "actionName": "unPass",
                                "opinion": "不同意 请上传小微主签字的附件。"}

            disagree_payload = json.dumps(disagree_payload)

            disagree_fuc()
            print('不同意 请上传小微主签字的附件。')
        else:
            file_list = json.loads(file_list)
            file_list = file_list[0]
            file_list = file_list['response']
            file_list_url = file_list['data']

            node_in_opin = nodes.get('data').get('opinions')

            opin_result = '0'

            reason_result = '0'

            # for i in node_in_opin:
            #     opin_leader = i.get('userId')
            #     if getTitle(opin_leader) and ('小微主' in getTitle(opin_leader) or opin_leader in leader_list):
            #         opin_result = '1'
            #         final_opin_leader = opin_leader
            #
            # for i in node_in_reason:
            #     if getTitle(i) and ('小微主' in getTitle(i) or opin_leader in leader_list):
            #         reason_result = '1'
            #         final_opin_leader = i

            if sqlx == 'dgyssq':
                t_apply_user = ''
                for dgyssq_applyUserCodes in apply_list:
                    dgyssq_applyUserCode = dgyssq_applyUserCodes.get('applyUserCode')
                    t_apply_user = t_apply_user + ', ' + dgyssq_applyUserCode


            # if opin_result == '1' or reason_result == '1':
            #     agree_fuc()
            # else:
            #     disagree_payload = {"instanceId": "" + instId + "", "plat": "porcess-usb",
            #                         "taskId": "" + taskId + "",
            #                         "actionName": "unPass",
            #                         "opinion": "不同意 注意最终审批人应该是小微主，您需要向上查找自己的领导，否则不能通过。线上审批人节点里没有小微主的，请在报备具体原因中注明签字小微主的姓名和工号，具体请参照线上说明文档的截图 https://ihaier.feishu.cn/docx/PFSWdlfgyo6uToxt5EScG5cgnUg ，否则签字看不清楚，或没有在原因中注明的不再询问直接驳回。"}
            #
            #     disagree_payload = json.dumps(disagree_payload)
            #     disagree_fuc()
            # 集团已调整为强制小微主审批，因此不需要上述判断了
            agree_fuc()
