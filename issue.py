from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.Issue import Issue
from github import Github
import logging
import asyncio
import sys

import run

logging.basicConfig(level=logging.INFO)

# 获取 GitHub token
ACCESS_TOKEN = sys.argv[1]

# 连接到 GitHub API
github = Github(ACCESS_TOKEN)

# 获取存储库
repo: Repository = github.get_repo('Misaka-OpenSource/XTU-OnlineJudge-Answer')

# 获取所有开放的问题
issues: PaginatedList = repo.get_issues(state='open')


# 处理Issue
for index, issue in enumerate(issues):
    issue: Issue = issue
    try:
        logging.info(f"{index+1}. {issue.title}\n{issue.body}")
        lines = issue.body.splitlines()
        assert (
            len(lines) >= 2
            and issue.title.strip() == lines[0].strip()
            and lines[0].isdigit()
            and lines[1].isdigit()
        ), "Issue格式错误"

        problem_id = int(lines[0])
        exam_id = int(lines[1])

    except Exception as e:
        logging.error(f"Error! {e}")
        issue.create_comment(f"Error! {e}\n已关闭Issue, 你可以修改后重新打开此Issue!")
    else:
        try:
            asyncio.run(run.main(exam_id, problem_id, 3))
        except Exception as e:
            issue.create_comment(f"Failed! 爬取AC代码时遇到错误{e} 重新打开Issue即可重试!")
            raise e
        else:
            issue.create_comment(
                "Success! 成功爬取到AC代码!\n"
                + f"URL: https://https://misaka-opensource.github.io/XTU-OnlineJudge-Answer/answer/{exam_id}/{problem_id} (被墙)")
            logging.info(f"Success!")
            issue.lock("resolved")
    finally:
        issue.edit(state="closed")
