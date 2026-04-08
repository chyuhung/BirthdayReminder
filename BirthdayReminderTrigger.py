# 云函数：触发 BirthdayReminder 生日提醒 GitHub Action
# 作用：每天定时调用 GitHub API，自动运行生日提醒任务

# 使用Python内置库，无需安装依赖，云函数直接运行
import json
import urllib.request
import urllib.error

def run():
    # ========== 【必须修改这4个信息】 ==========
    GITHUB_TOKEN = "your_github_token"
    GITHUB_USER = "your_github_user"
    REPO_NAME = "your_repo_name"  # 你的Action项目名
    WORKFLOW_NAME = "your_workflow_name.yml"  # 你的Action文件名
    
    # 构造请求数据：触发 main 分支
    payload = json.dumps({"ref": "main"}).encode('utf-8')
    
    # 请求头：身份认证
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    # GitHub API 地址（自动拼接）
    url = f'https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/actions/workflows/{WORKFLOW_NAME}/dispatches'
    
    # 发送请求触发 Action
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
        with urllib.request.urlopen(req) as resp:
            print(f"触发成功！状态码：{resp.getcode()}")
            return "触发 BirthdayReminder 成功"
    except urllib.error.HTTPError as e:
        print(f"触发失败，错误码：{e.code}，返回信息：{e.read().decode()}")
        return "触发失败"
    except Exception as e:
        print(f"异常：{str(e)}")
        return "触发异常"

# 腾讯云函数入口（固定写法，不用改）
def main_handler(event, context):
    return run()
