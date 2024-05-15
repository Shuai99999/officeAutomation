import requests
import json
import sys
sys.path.insert(0, sys.path[0]+"/../credential")
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

# flwId = 'FLW20240218077453'
flwId = sys.argv[1]

getFlwidUrl = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/processReport/procMonitorReport?order=&orderField=&sumFields=&page=1&limit=10&procDefName=&creator=&procStatus=&bDate=&eDate=&bApproveDate=&eApproveDate=&deptIds=&deptName=&creatorName=&procBizCode=" + flwId + ""

payload = {}
headers = {
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'token': task_token,
    'sec-ch-ua-platform': '"Windows"',
    'host': 'rrsoa.rrswl.com'
}

getFlwidResponse = requests.request("GET", getFlwidUrl, headers=headers, data=payload)
getFlwidResponse = getFlwidResponse.text
getFlwidResponse = json.loads(getFlwidResponse)
instId = getFlwidResponse.get('data').get('list')[0].get('id')

url = "https://rrsoa.rrswl.com/uniedp-web/oa/flowable/processInst/instFormInfo?instId=" + instId + "&monitor=true&ccFlag=false"
getFlwidDetail = requests.request("GET", url, headers=headers, data=payload)
getFlwidDetail = getFlwidDetail.text
getFlwidDetail = json.loads(getFlwidDetail)
boData = getFlwidDetail.get('data').get('boData')
boData = json.loads(boData)
dbName = boData.get('databaseName')
fileId = boData.get('sqlFileId')

if fileId:
    fileIdArray = fileId.split(',')
    for fileIdArrayItem in fileIdArray:
        attach_url = 'https://rrsoa.rrswl.com/uniedp-web/obs/download?ossId=' + fileIdArrayItem + '&token=' + task_token + '&charset=UTF-8'

        attach = requests.get(attach_url)

        with open('/home/oracle/dba/bi/input', "wb") as code:
            # with open('input.txt', "wb") as code:
            code.write(attach.content)
        # os.system('read -n 1')

else:
    sql_text = boData["applyRemark"]
    sql_text = sql_text.encode()
    with open('/home/oracle/dba/bi/input', "wb") as code:
        code.write(sql_text)

if 'oracle' in dbName:
    # subprocess.Popen(['su', '-', 'oracle', '/home/oracle/dba/bi/exp.sh', dbName, "", "", flwId, " > /dev/null &"], stdout=subprocess.PIPE)
    print('su - oracle /home/oracle/dba/bi/exp.sh ' + dbName + ' "" "" ' + flwId + ' > /dev/null &')
    print('tail -1 /home/oracle/dba/bi/rpt')
elif 'mysql' in dbName or 'polardb' in dbName:
    # subprocess.Popen(['su', '-', 'mysql', '/home/oracle/dba/bi/exp.sh', dbName, "", "", flwId, " > /dev/null &"], stdout=subprocess.PIPE)
    print('su - mysql /home/mysql/dba/bi/exp.sh ' + dbName + ' "" "" ' + flwId + ' > /dev/null &')
    print('tail -1 /home/mysql/dba/bi/rpt')
