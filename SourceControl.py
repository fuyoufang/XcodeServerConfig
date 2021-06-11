#!/usr/bin/env python3
from git import Repo
import re
import DingTalk
import sys
import os

def getLastCommit(path):
    if not os.path.exists(path):
        return

    with open(path, 'r') as f:
        content =f.read()
        #re.match(r'^DVTSourceControlLocationRevisionKey$', content)
        result = re.findall(r"DVTSourceControlLocationRevisionKey = (.+?);", content)
        if (len(result) < 1):
            print('没有找到')

        return result[0]

def getGitLog(project_path, lastCommit):
    print("getGitLog:"+project_path)
    repo = Repo(project_path)
    head = repo.head
    master = head.reference
    # log = master.log()
    # log2 = head.log()
    
    newCommits = []
    for i in repo.iter_commits():
        if i.hexsha == lastCommit:
            break

        newCommits.append(i)
    return newCommits
    
# 获取 git 日志
def getCommits(log_path, project_path): 
    lastCommit = getLastCommit(log_path)
    if lastCommit is None:
        print('未或得上次 commit')
        return 
    print('上次提交的 commit')
    print(lastCommit)
    print('开始搜索最近的 commit')
    return getGitLog(project_path, lastCommit)


if __name__ == "__main__":
    print(DingTalk.getDingTalkRbootUrl()) 
