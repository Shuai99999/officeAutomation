import requests
import json
from datetime import datetime


class zentao_cli(object):
    session = None  # 用于实现单例类，避免多次申请sessionID
    sid = None

    def __init__(self, url, account, password, override=False):
        self.url = url
        self.account = account
        self.password = password
        self.session_override = override
        self.pages = {
            "sid": "/api-getSessionID.json",  # 获取sid的接口
            "login": "/user-login.json?zentaosid={0}",  # 登录的接口
            "get_product_list": "/product-index-no.json",
            "get_unclosed_task": "/execution-task-376-unclosed-0-id_desc.json",
            "post_new_task": "/task-create-376-0-0.json",
            "start_task": "/task-start-",
            "finish_task": "/task-finish-",
            "close_task": "/task-close-",
            # 以下为单独完成某个任务时使用的URL
            # "start_task": "/task-start-15228.json",
            # "finish_task": "/task-finish-15228.json",
            # "close_task": "/task-close-15228.json",
        }
        self.s = None
        self.sid = None

    def req_get(self, url):
        # 请求并返回结果
        web = requests.get(url)
        if web.status_code == 200:
            resp = json.loads(web.content)
            if resp.get("status") == "success":
                return True, resp
            else:
                return False, resp

    def req_post(self, url, body):
        # 请求并返回结果
        res = requests.post(url=url, data=body)
        if res.status_code == 200:
            resp = json.loads(res.content)
            if resp.get("status") == "success":
                return True, resp
            else:
                return False, resp

    def login(self):
        if self.s is None:
            if not self.session_override and zentao_cli.session is not None:
                self.s = zentao_cli.session
                self.sid = zentao_cli.sid
            else:
                # 新建会话
                self.s = requests.session()
                res, resp = self.req_get(self.url.rstrip("/") + self.pages["sid"])
                if res:
                    print("获取sessionID成功")
                    self.sid = json.loads(resp["data"])["sessionID"]
                    zentao_cli.sid = self.sid
                    body = {'account': self.account, 'password': self.password, 'keepLogin[]': 'on',
                            'referer': self.url.rstrip("/") + '/my/'}
                    login_res, login_resp = self.req_post(self.url.rstrip("/") + self.pages["login"].format(self.sid),
                                                          body)
                    if login_res:
                        print("登录成功")
                        zentao_cli.session = self.s

    def get_product_list(self):
        req_url = self.url.rstrip("/") + self.pages["get_product_list"]
        res, resp = self.req_get(req_url + "?zentaosid=" + self.sid)
        if res:
            data = resp['data']
            products = json.loads(data)['products']
            return products.keys(), products.values()

    def get_unclosed_task_list(self):
        req_url = self.url.rstrip("/") + self.pages["get_unclosed_task"]
        res, resp = self.req_get(req_url + "?zentaosid=" + self.sid)
        if res:
            data = resp['data']
            products = json.loads(data)['tasks']
            return products

    def create_new_task(self):
        req_url = self.url.rstrip("/") + self.pages["post_new_task"]

        now = datetime.now()

        taskDict = {

            1: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            2: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            3: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            4: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            5: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            6: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            7: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            8: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            9: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            10: [['数据库月度巡检', '6', '数据库月度巡检'],
                ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                 '处理数据变更、导出，数据库和例外软件权限审批']],

            11: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            12: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            13: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            14: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            15: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            16: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            17: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            18: [['数据库备份恢复演练', '4', '数据库备份恢复演练'],
                 ['准备压测数据库环境', '4',
                  '准备压测数据库环境']],

            19: [['数据库备份恢复演练', '4', '数据库备份恢复演练'],
                 ['准备压测数据库环境', '4',
                  '准备压测数据库环境']],

            20: [['数据库备份恢复演练', '6', '数据库备份恢复演练'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            21: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            22: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            23: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            24: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            25: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            26: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            27: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            28: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            29: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            30: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],

            31: [['整理项目预算和付款资料', '6', '整理项目预算和付款资料'],
                 ['处理数据变更、导出，数据库和例外软件权限审批', '2',
                  '处理数据变更、导出，数据库和例外软件权限审批']],
        }

        taskList = taskDict.get(now.day)
        today = str(datetime.now()).split(' ')[0]

        # 如果要补之前日期的，把日期填在括号里执行下面这句
        # taskList = taskDict.get(12)
        # today = '2024-04-12


        for taskListDaily in taskList:
            # print(taskListDaily)
            data = {
                "execution": "376",
                "type": "devel",
                "module": "427",
                "assignedTo[]": "01454221",
                "teamMember": "",
                "mode": "linear",
                "status": "wait",
                "story": "9256",
                "color": "",
                "name": taskListDaily[0],
                "storyEstimate": "10000000",
                "storyDesc": "DBA日常需求---高帅",
                "storyPri": "1",
                "pri": "3",
                "estimate": taskListDaily[1],
                "desc": taskListDaily[2],
                "estStarted": today,
                "deadline": today,
                "after": "toTaskList",
                "uid": "660b78fba5b9b",
            }
            # taskListData.append(data)
            resp = self.req_post(req_url + "?zentaosid=" + self.sid, data)
            # print(resp[1]['id'])
            # print(type(resp[1]['id']))
            taskId = resp[1]['id']

            # 录入工时并完成任务
            url = self.url.rstrip("/") + self.pages["start_task"] + taskId + '.json'
            data = {
                "assignedTo": ["01454221"],
                "realStarted": today + " 09:00:00",
                "consumed": taskListDaily[1],
                "left": 0,
                "comment": "开始任务"
            }
            resp = self.req_post(url + "?zentaosid=" + self.sid, data)
            print(resp)

            # 关闭任务
            url = self.url.rstrip("/") + self.pages["finish_task"] + taskId + '.json'
            data = {
                "currentConsumed": taskListDaily[1],
                "assignedTo": ["01454221"],
                "realStarted": today + " 9:00:00",
                "finishedDate": today + " 19:00:00",
                "status": "done",
                "comment": "完成任务"
            }
            resp = self.req_post(url + "?zentaosid=" + self.sid, data)
            print(resp)

    # start, finish, close都合并在create里了，以下代码仅供参考
    def start_task(self):
        url = self.url.rstrip("/") + self.pages["start_task"]
        data = {
            "assignedTo": ["01454221"],
            "realStarted": "2024-04-03 09:00:00",
            "consumed": 6,
            "left": 0,
            "comment": "开始任务"
        }
        resp = self.req_post(url + "?zentaosid=" + self.sid, data)
        print(resp)

    # finish没用了，start录入足够的工时就能完成了
    def finish_task(self):
        url = self.url.rstrip("/") + self.pages["finish_task"]
        data = {
            "currentConsumed": 6,
            "assignedTo": ["01454221"],
            "realStarted": "2024-04-03 9:00:00",
            "finishedDate": "2024-04-03 19:00:00",
            "status": "done",
            "comment": "完成任务"
        }
        resp = self.req_post(url + "?zentaosid=" + self.sid, data)
        print(resp)

    def close_task(self):
        url = self.url.rstrip("/") + self.pages["close_task"]
        data = {
            "status": "closed",
            "comment": "任务完成并关闭。"
        }
        resp = self.req_post(url + "?zentaosid=" + self.sid, data)
        print(resp)


if __name__ == "__main__":
    cli = zentao_cli("https://wlapi.rrswl.com/zentao", "01454221", "Haier,123456")
    cli.login()
    # print(cli.get_product_list())
    # print(cli.get_unclosed_task_list())
    cli.create_new_task()
    # start,finish,close都合并在create里了，代码仅供参考
    # cli.start_task()
    # finish没用了，start录入足够的工时就能完成了
    # cli.finish_task()
    # cli.close_task()
