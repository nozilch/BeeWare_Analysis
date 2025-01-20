import requests
from datetime import datetime
import matplotlib.pyplot as plt

# GitHub仓库信息和个人访问令牌
repo_owner = "beeware"
repo_name = "beeware"
token = '个人令牌'

headers = {
    'Authorization': f'token {token}',
}


def fetch_issues():
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    params = {'state': 'all', 'per_page': 100, 'page': 1}
    issues = []

    while True:
        response = requests.get(url, headers=headers, params=params, verify=False)  # 忽略SSL验证
        if response.status_code != 200:
            print(f"Error fetching issues: {response.status_code}")
            break

        page_issues = response.json()
        if not page_issues:
            break

        issues.extend(page_issues)
        params['page'] += 1

    return issues


def analyze_issues(issues):
    bug_timestamps = []
    for issue in issues:
        # 检查是否标记为bug或者通过标题判断
        labels = [label['name'] for label in issue.get('labels', [])]
        if 'bug' in labels or ('title' in issue and 'bug' in issue['title'].lower()):
            created_at = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            bug_timestamps.append(created_at)

    return bug_timestamps


def plot_analysis(bug_timestamps):
    bugs_per_day = {}
    for timestamp in bug_timestamps:
        day = timestamp.date()
        if day not in bugs_per_day:
            bugs_per_day[day] = 0
        bugs_per_day[day] += 1

    days = sorted(bugs_per_day.keys())
    counts = [bugs_per_day[day] for day in days]

    plt.figure(figsize=(14, 7))
    plt.plot(days, counts, marker='o')
    plt.title('Bug Reports Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Bugs Reported')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    issues = fetch_issues()
    bug_timestamps = analyze_issues(issues)
    plot_analysis(bug_timestamps)