# -*- coding: utf-8 -*-
import json
import os
import os.path as path

root = "/Users/xqk/Downloads/json_销售合同抽取-奔朗新材"


def dfs(curr_file=".", ret_list=list()):
    if not path.isdir(curr_file):
        if curr_file.endswith("json"):
            ret_list.append(curr_file)
        return
    files = os.listdir(curr_file)
    for file in files:
        dfs(curr_file + path.sep + file, ret_list)


def read_content(path=""):
    with open(path, "r") as file:
        content = json.load(file)
        print(content)


if __name__ == '__main__':
    json_files = []
    dfs(root, json_files)
    read_content(json_files[0])
