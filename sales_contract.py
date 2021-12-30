#!/usr/bin/python3
# encoding:utf-8

import os
import pandas as pd
from bs4 import BeautifulSoup
import json
import openpyxl

"""
合同分为：单品合同、整线合同以及其他 (根据是否存在“销售奖励制度”、“约定单价”字段来区分)
输入：json格式合同文件
输出：三个excel文件，分别为单品合同、整线合同、国外合同
"""

single_product_key = {"签订主体":[], "合同编号":[], "客户名称":[], "产品名称":[], "合同金额":[], "签订地点":[], "销售奖励制度":[],
                      "结算方式和结算周期":["结算方式及期限"],"运输方式和有效验收":[], "签订日期":[], "有效期":[]}
whole_line_key = {"签订主体":[], "合同编号":[], "客户名称":[], "产品名称":[], "约定单价":[],
                  "结算方式和结算周期":[], "签订日期":[], "有效期":[]}
foreign_key = {"签订主体":["seller"], "合同编号":["document number", "contract no.", "p.o.no."], "客户名称":["buyer"],
               "产品名称":["name of commodity", "desc."],
               "签订地点":["signed at:"],
               "付款方式":["terms of payment", "payment"],
               "运输方式":["terms of delivery", "shipment term"],
               "交货日期": ["delivery period", "delivery date"],
               "签订日期":["date"],
               "合同金额":["total value payable", "total exw value"]}
common_key = ["文件夹一级名称", "文件夹末级名称", "文件名称", "字段类型"]
contract_type = ["单品合同字段", "整线合同字段", "国外合同字段", "其他"]

foreign_output = './国外合同字段.xlsx'


def convert_filejson_to_text2(jsondata):
    """
    将收到的json串根据坐标位置合成段落
    :param filejson: 收到的file json串
    :return: 文字文本、表格文本
    """
    # 先根据data中的'\n'来判断是否一行，先不考虑段落拼接的问题
    # 从json串中取出lines部分
    text_data = []
    table_data = []
    for filejson in jsondata:
        pages = filejson["pages"]

        for page in pages:
            tables = page["table"]
            for table in tables:
                type = table["type"]
                if type is False:  # 表示为文本
                    text = []
                    datas = table["data"].split('\n')
                    lines = table["lines"]
                    count = 0
                    for j in range(len(datas)):
                        data = datas[j]
                        start = 0
                        for i in range(count, len(lines)):
                            line = lines[i]
                            ind = data.find(line["text"], start, len(data))
                            start = ind +len(line["text"])
                            if ind != -1:
                                if len(text) < j+1:
                                    paras = _build_paras2(i, data, line["poly"][:-1], len(line["text"])+ind,
                                                          line["char_polygons"])
                                    text.append(paras)
                                else:
                                    # text[-1]["data"] += line["text"]
                                    # text[-1]["char_index"].append(text[-1]["char_index"][-1]+len(line["text"]))
                                    if text[-1]["char_index"][-1] == len(data):
                                        count = i
                                        break
                                    text[-1]["index"].append(i)
                                    text[-1]["char_index"].append(ind + len(line["text"]))
                                    text[-1]["position"].append(line["poly"][:-1])
                                    text[-1]["char_polygons"].append(line["char_polygons"])
                                    if text[-1]["data"][ind-1] == ' ':
                                        text[-1]["char_position"].append([])
                                    text[-1]["char_position"].extend(line["char_polygons"])
                                    # assert len(text[-1]["data"]) == len(text[-1]["char_position"])
                            else:
                                count = i
                                break
                    if len(text) != 0:
                        text_data.extend(text)

                    # for td in text_data:
                    #     if len(td["data"]) != len(td["char_position"]):
                    #         print(td["data"], len(td["data"]), len(td["char_position"]))
                    #         assert len(td["data"]) == len(td["char_position"])
                else:  # type = True 表示为表格
                    tdata = []
                    row = -1
                    for blocks in table["form_blocks"]:
                        if blocks['data'] == '':
                            continue
                        if row == -1 or row != blocks["start_row"]:
                            # 不同行
                            row_list = {
                                "data": "",
                                "position": [],
                                "char_index": [],
                                "char_polygons":[],
                                "char_position":[]
                            }
                            # row_list["data"].append(blocks["data"])
                            # num = blocks["data"].count('\n')
                            num = len(blocks["lines"])
                            if num > 1:
                                blocks["data"] = blocks["data"].replace('\n', '')
                                data_len = 0
                                for i in range(num):
                                    if data_len > 0 and blocks["data"][data_len] == ' ':
                                        row_list["char_position"].append([])
                                        data_len += 1
                                    data_len += len(blocks["lines"][i]["text"])
                                    row_list["char_polygons"].append(blocks["lines"][i]["char_polygons"])
                                    row_list["char_position"].extend(blocks["lines"][i]["char_polygons"])
                                # blocks["data"] = blocks["data"].replace('\n', '')
                            else:
                                row_list["char_polygons"].append(blocks["lines"][0]["char_polygons"])
                                row_list["char_position"].extend(blocks["lines"][0]["char_polygons"])
                            row_list["data"] = blocks["data"]
                            row_list["char_index"].append(len(row_list["data"]))
                            row_list["position"].append(blocks["org_position"])

                            # if len(row_list["data"]) != len(row_list["char_position"]):
                            #     print(row_list["data"], len(row_list["data"]), len(row_list["char_position"]))
                            #     assert len(row_list["data"]) == len(row_list["char_position"])
                            tdata.append(row_list)
                        elif row == blocks["start_row"]:
                            # 同一行
                            # tdata[-1]["data"].append(blocks["data"])
                            tdata[-1]["data"] += '\t'
                            tdata[-1]["char_position"].append([])
                            # num = blocks["data"].count('\n')
                            num = len(blocks["lines"])
                            if num > 1:
                                blocks["data"] = blocks["data"].replace('\n', '')
                                data_len = 0
                                for i in range(num):
                                    if data_len > 0 and blocks["data"][data_len] == ' ':
                                        tdata[-1]["char_position"].append([])
                                        data_len += 1
                                    data_len += len(blocks["lines"][i]["text"])
                                    tdata[-1]["char_polygons"].append(blocks["lines"][i]["char_polygons"])
                                    tdata[-1]["char_position"].extend(blocks["lines"][i]["char_polygons"])

                            else:
                                tdata[-1]["char_polygons"].append(blocks["lines"][0]["char_polygons"])
                                tdata[-1]["char_position"].extend(blocks["lines"][0]["char_polygons"])
                            tdata[-1]["data"] += blocks["data"]
                            tdata[-1]["char_index"].append(len(tdata[-1]["data"]))
                            tdata[-1]["position"].append(blocks["org_position"])

                            # if len(tdata[-1]["data"]) != len(tdata[-1]["char_position"]):
                            #     print(tdata[-1]["data"], len(tdata[-1]["data"]), len(tdata[-1]["char_position"]))
                            #     assert len(tdata[-1]["data"]) == len(tdata[-1]["char_position"])
                        row = blocks["start_row"]
                    table_data.append(tdata)
    return text_data, table_data


def _build_paras2(ind, data, position, char_index, char_polygons):
    paras = {
        "data": "",
        "char_index":[],
        "index": [],
        "position":[],
        "char_polygons":[],
        "char_position":[]
    }
    paras["data"] = data
    paras["index"].append(ind)
    paras["position"].append(position)
    paras["char_index"].append(char_index)
    paras["char_polygons"].append(char_polygons)
    paras["char_position"].extend(char_polygons)
    # assert len(paras["data"]) == len(paras["char_position"])
    return paras


def batch_extraction():
    """
    批量处理整个文件夹中的json文件
    :return:
    """
    filepath_1 = '/Users/xqk/Downloads/json_销售合同抽取-奔朗新材'
    json_files = {}
    for roots, dirs, files in os.walk(filepath_1):
        for file in files:
            file = os.path.join(roots, file).replace("\\", '/')
            if file.endswith(".json"):
                # TODO:同一份合同的json文件要一起处理
                filename = file.split('/')[-1]
                name = filename.split('_')[0]
                if name not in json_files.keys():
                    json_files[name] = []
                    json_files[name].append(file)
                else:
                    json_files[name].append(file)

    print(len(json_files))

    data = {"签订主体":[], "合同编号":[], "客户名称":[],
               "产品名称":[],
               "签订地点":[],
               "付款方式":[],
               "运输方式":[],
               "交货日期": [],
               "签订日期":[],
               "合同金额":[],
               "文件夹一级名称":[],
               "文件夹末级名称":[],
               "文件名称":[]
    }

    for filename, file_list in json_files.items():
        f = file_list[0].split('/')
        data["文件夹一级名称"].append(f[2])
        data["文件夹末级名称"].append(f[len(f) - 2])
        data["文件名称"].append(filename)

        # 抽取国外合同
        result = extract_sales_contract(file_list)

        # TODO:抽取单品合同、整线合同

        for key in result.keys():
            data[key].append(result[key])

    # 写入excel文件
    df = pd.DataFrame(data)
    df.to_excel(foreign_output, index=False)


def extract_sales_contract(file_list):
    jsondata = []
    for file in file_list:
        with open(file, 'r', encoding='utf8') as fp:
            jsondata.append(json.load(fp))

    text_data, table_data = convert_filejson_to_text2(jsondata)

    result = {}
    for key in foreign_key.keys():
        find_flag = False
        content = None
        result_flag, matched_str = _match_key(key, text_data)
        if result_flag is True:
            find_flag, content = find_key_value(key, matched_str)

        if result_flag is False or find_flag is False:
            result_flag, matched_str = _match_key_from_table(key, table_data)
            if result_flag is True:
                find_flag, content = find_key_value(key, matched_str)

        if find_flag is False:
            print("Not find labelId: {}".format(key))

        result[key] = content

    return result


def _match_key(key, text_data):
    result_flag = False
    matched_str = None
    for i in range(len(text_data)):
        for name in foreign_key[key]:
            text = text_data[i]["data"]
            lower_text = text_data[i]["data"].lower()
            if name in lower_text:
                ind = lower_text.find(name)
                matched_str = lower_text[ind:]
                result_flag = True
                break

        if result_flag is True:
            break

    return result_flag, matched_str


def _match_key_from_table(key, table_data):
    matched_str = None
    result_flag = False
    for table in table_data:
        for i in range(len(table)):
            row_str = table[i]["data"]
            lower_row_str = table[i]["data"].lower()
            for name in foreign_key[key]:
                if name in lower_row_str:
                    ind = lower_row_str.find(name)
                    matched_str = row_str[ind:]
                    result_flag = True
                    break

            if result_flag is True:
                break

        if result_flag is True:
            break

    return result_flag, matched_str


def find_key_value(key, text):
    find_flag = False
    content = None
    text = text.replace("：", ":")
    ind = text.find(":")
    if ind != -1:
        content = text[ind + 1:]
        # content = content.strip().split(' ')[0]
        find_flag = True
    elif '\t' in text:
        content = text.split('\t')[1]
        find_flag = True
    elif ' ' in text:
        content = text.strip().split(' ')[1]
        find_flag = True

    return find_flag, content


def _extract_foreign_contract(text_data, foreign_key):
    result = {}
    for key in foreign_key.keys():
        for name in foreign_key[key]:
            result_flag = False
            matched_str = None
            for i in range(len(text_data)):
                text = text_data[i]["data"]
                if name in text:
                    ind = text.find(name)
                    matched_str = text[ind:]
                    result_flag = True
                    break

            if result_flag is True:
                break

        if result_flag is True:
            break
        result["key"]





    return result


if __name__ == '__main__':
    batch_extraction()
