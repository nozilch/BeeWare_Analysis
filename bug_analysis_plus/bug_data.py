import requests
import json

# 设置 GitHub API 地址
repo_owner = "beeware"
repo_name = "toga"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"

# 过滤出标记为 "bug" 的 issues
params = {
    "state": "all",  # 获取所有状态的 issue（包括已关闭和未关闭）
    "labels": "bug",  # 过滤出 bug 标签的 issue
    "per_page": 100  # 每页获取最多100个结果
}

response = requests.get(url, params=params, verify=False)
issues = response.json()

# 输出获取到的 bug 信息
for issue in issues:
    print(f"Issue Title: {issue['title']}")
    print(f"Created At: {issue['created_at']}")
    print(f"Closed At: {issue['closed_at']}")
    print(f"URL: {issue['html_url']}")
    print("-" * 60)


import matplotlib.pyplot as plt
from datetime import datetime

# 提取 bug 提交和关闭的时间
created_times = []
closed_times = []

# 将数据格式化为时间戳
for issue in issues:
    created_times.append(datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ"))
    if issue['closed_at']:
        closed_times.append(datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ"))

# 计算 bug 提交的月份
created_months = [time.month for time in created_times]
closed_months = [time.month for time in closed_times]

# 绘制 bug 提交月份分布图
plt.hist(created_months, bins=12, alpha=0.7, label="Bug Created")
plt.hist(closed_months, bins=12, alpha=0.7, label="Bug Closed")
plt.xlabel('Month')
plt.ylabel('Number of Bugs')
plt.title('Bug Submission and Closure by Month')
plt.legend(loc='upper right')
plt.show()
