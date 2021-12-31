# -*- coding: utf-8 -*-
import json
import os
import os.path as path
import re

import pandas as pd

from Keys import *
from entity import *

COLON = ":"

root = "/Users/xqk/Downloads/02.陶加国内"


def file_filter(root_dir="."):
    ret_map = {}
    for root_path, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                # if "page" in file:
                #     tokens = file.split("_")
                #     name = tokens[0]
                #     index = int(tokens[-1].split(".")[0])
                # else:
                #     name = file.split(".")[0]
                #     index = 1
                key = path.join(root_path, file)
                if key not in ret_map:
                    ret_map[key] = {}
                ret_map[key] = path.join(root_path, file)
    return ret_map


title_key_set = ["合同", "协议", "订货单", "订单"]


def _contains_any(seq, aset):
    return True if any(seq.find(word) >= 0 for word in aset) else False


def extract_contract(pages={}, filename=""):
    """
    遍历合同每一页的内容，提取合同关键信息
    :param pages: 每一个合同包含的所有页面
    :return: 合同
    """
    page_num = len(pages.keys())
    contract_json = {}
    with open(pages[1]) as file:
        doc = json.load(file)
        table_list = doc["pages"][0]["table"]
        title = table_list[0]["lines"][0]['text']
        if not _contains_any(title, title_key_set):
            return None
    src_text = ""
    form_data = []
    for i in range(1, page_num + 1, 1):
        with open(pages[i], "r") as file:
            data = json.load(file)
            table_list = data['pages'][0]['table']
            for table in table_list:
                is_form = table["type"]
                if is_form:
                    form_data += table["form_blocks"]
                else:
                    _parse_text(table["lines"], contract_json)
                    src_text += table["data"]
    form, extra_data = _parse_form(form_data)
    _contract = assemble_contract(contract_json, extra_data, src_text)
    _contract.form = form
    _contract.title = title
    if len(_contract.incentive_system) > 0:
        _contract.type = SINGLE_PRODUCT
    elif len(_contract.unit_price) > 0:
        _contract.type = WHOLE_LINE
    else:
        _contract.type = OTHERS
    return _contract


def _parse_form(form_data):
    """
    解析表格数据：求出每行包含单元格数目的众数m，从头两行中找出列数等于m的那一行作为表头，
    然后从剩下的列中每次取出m项（需检验该m项的(start_row, end_row),一致）。
    如果不一致，说明该页中包含多个表格，该列为新的表格开头。
    如果表格占据多页，那么需要将其拼接。
    (start_row, start_column) = (0,0)代表表格开头
    :param form_data: 表单原始数据
    :return:
    """
    form_pages = {}
    extra_data = {}
    index = -1
    for _cell in form_data:
        """
        按表格主体划分表单
        """
        cell = json.loads(json.dumps(_cell), object_hook=Cell)
        if cell.start_row == 0 and cell.start_column == 0:
            index += 1
        if index not in form_pages.keys():
            form_pages[index] = []
        form_pages[index].append(cell)
    ret = {}
    form_id = 0
    for cell_list in form_pages.values():
        col_num, row_num = calc_form_info(cell_list)
        if row_num == 1:
            # 单行表格，提取表格内关键字
            for _cell in cell_list:
                for line in _cell.lines:
                    txt = line.text
                    if COLON in txt:
                        pair = txt.split(COLON)
                        extra_data[pair[0]] = pair[1]
        elif row_num > 1:
            title = form_id
            start_row = 0
            # valid_cell_num = 0
            form_id += 1
            valid_cell_num = 0
            # 解析表格重的标题行
            # tmp = None
            # for j in range(col_num):
            #     _cell = cell_list[start_row * col_num + j]
            #     if len(_cell.data.strip()) > 0:
            #         valid_cell_num += 1
            #         if tmp is None:
            #             tmp = _cell.data.strip()
            # if title is None or len(title) > 10:
            #     title = form_id
            ret[title] = []
            for i in range(start_row, row_num):
                row_items = []
                for j in range(col_num):
                    row_items.append(cell_list[i * col_num + j].data)
                ret[title].append(row_items)

    return ret, extra_data


def calc_form_info(cell_list):
    col_num = 0
    for _cell in cell_list:
        if _cell.start_row == 0:
            col_num += 1
    return col_num, int(len(cell_list) / col_num)


def _parse_text(content, dataframe):
    for line in content:
        text = line['text'].strip()
        if COLON in text:
            tokens = text.split(COLON)
            if len(tokens) == 2:
                key, value = tokens
                if len(key.strip()) > 0 and len(value.strip()) != 0 and key not in dataframe.keys():
                    dataframe[key] = value
    pass


def parse_field(dataframe, field_key_list):
    key_set = dataframe.keys()
    for key in field_key_list:
        for target in key_set:
            if key in target or target in key:
                return dataframe[target]
    return None


def assemble_contract(dataframe, extra_data, src_text):
    _contract = Contract()
    _no = parse_field(dataframe, key_dictionary[CONTRACT_NO_KEY])
    _customer_name = parse_field(dataframe, key_dictionary[CUSTOMER_NAME_KEY])
    _sign_entity = parse_field(dataframe, key_dictionary[SIGN_ENTITY_KEY])
    _sign_date = parse_field(dataframe, key_dictionary[SIGN_DATE_KEY])
    _sign_place = parse_field(dataframe, key_dictionary[SIGN_PLACE_KEY])
    _delivery_date = parse_field(dataframe, key_dictionary[DELIVERY_DATE_KEY])
    _delivery_method = parse_field(dataframe, key_dictionary[DELIVERY_METHOD_KEY])
    _payment_method = parse_field(dataframe, key_dictionary[PAYMENT_METHOD_KEY])
    _expiry_date = parse_field(dataframe, key_dictionary[EXPIRY_DATE_KEY])
    _incentive_system = parse_field(dataframe, key_dictionary[INCENTIVE_SYSTEM_KEY])

    if _sign_date is None:
        match = re.compile("(?<=自).*?(?=开始)").search(src_text)
        start_date = None
        end_date = None
        if match is not None:
            start_date = match.group()
        match = re.compile("(?<=到).*?(?=止)").search(src_text)
        if match is not None:
            end_date = match.group()
        _sign_date = str(start_date) + "-" + str(end_date)

    _contract.set_sign_entity(_sign_entity)
    _contract.set_sign_date(_sign_date)
    _contract.set_sign_place(_sign_place)
    _contract.set_delivery_date(_delivery_date)
    _contract.set_delivery_method(_delivery_method)
    _contract.set_payment_method(_payment_method)
    _contract.set_expiry_date(_expiry_date)
    _contract.set_incentive_system(_incentive_system)

    return _contract


def write_excel(out_path, contract_list):
    if len(contract_list) == 0:
        return
    item = contract_list[0]
    keys, _ = item.serialize()
    data = list()
    data.append(keys)
    for _contract in contract_list:
        _, values = _contract.serialize()
        data.append(values)
    df = pd.DataFrame(data)
    df.to_excel(excel_writer=out_path, header=False, na_rep="", index=False, sheet_name="合同列表")
    for _contract in contract_list:
        _form = _contract.form
        order_path = _contract.title + ".xlsx"
        writer = pd.ExcelWriter(order_path)
        for order_name in _form.keys():
            df = pd.DataFrame(_form[order_name])
            # df.to_excel(excel_writer=order_path, header=False, na_rep="", index=False, sheet_name=str(order_name))
            df.to_excel(writer, header=False, na_rep="", index=False, sheet_name=str(order_name))
        writer.save()
        writer.close()
        print("%s:%d\n" % (order_path, len(_form.keys())))
    print("Write %s succeed" % out_path)


if __name__ == '__main__':
    json_files = file_filter(root)
    err_file = []
    contract_list = []
    for filename, pages in json_files.items():
        try:
            contract = extract_contract(pages, filename)
            if contract is not None:
                contract_list.append(contract)
        except Exception as e:
            err_file.append(filename)
    single_contract_list = [e for e in contract_list if e.type == SINGLE_PRODUCT]
    whole_line_contract_list = [e for e in contract_list if e.type == WHOLE_LINE]
    other_contract_list = [e for e in contract_list if e.type == OTHERS]
    write_excel("single.xlsx", single_contract_list)
    write_excel("whole_line.xlsx", whole_line_contract_list)
    write_excel("others.xlsx", other_contract_list)
