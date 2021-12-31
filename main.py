# -*- coding: utf-8 -*-
import json
import os
import os.path as path
import re
import shutil
import pandas as pd
import argparse

from entity import *

SEP = os.sep
COLON = ":"


def file_filter(root_dir="."):
    ret_map = {}
    for root_path, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                if "page" in file:
                    tokens = file.split("_")
                    name = tokens[0]
                    index = int(tokens[-1].split(".")[0])
                else:
                    name = file.split(".")[0]
                    index = 1
                key = path.join(root_path, name)
                if key not in ret_map:
                    ret_map[key] = {}
                ret_map[key][index] = path.join(root_path, file)
    return ret_map


title_key_set = ["合同", "协议", "订货单", "订单"]


def _contains_any(seq, aset):
    return True if any(seq.find(word) >= 0 for word in aset) else False


def _parse_dir(root_dir, path):
    dir = None
    if not root_dir.endswith(SEP):
        dir = root_dir + SEP
    regex = "(?<=%s).*?(?=%s)" % (dir, SEP)
    first_dir = re.compile(regex).search(path).group()
    tokens = path.split(SEP)
    parent_dir = tokens[-2]
    filename = tokens[-1]
    return first_dir, parent_dir, filename


def extract_contract(root_dir, pages={}, filename=""):
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
    _form, extra_data = _parse_form(form_data)
    contract_json.update(extra_data)

    _contract = assemble_contract(contract_json, src_text)
    _first_dir, _parent_dir, _filename = _parse_dir(root_dir, filename)

    _contract.first_dir = _first_dir
    _contract.parent_dir = _parent_dir
    _contract.filename = _filename
    _contract.form = _form
    _contract.title = title
    _contract.text = src_text
    if "产品" in title:
        _contract.type = SINGLE_PRODUCT
    elif "整线" in title:
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
            form_id += 1
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
        if key in key_set:
            return dataframe[key]
    return None


def assemble_contract(dataframe, src_text):
    pairs = dict(re.findall('(?<=\s)(.+?):(.+?)(?=\s)', src_text))
    dataframe.update(pairs)

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
    _total_value = parse_field(dataframe, key_dictionary[TOTAL_VALUE_KEY])
    _unit_price = parse_field(dataframe, key_dictionary[UNIT_PRICE_KEY])

    if _expiry_date is None:
        match = re.compile("(?<=自).*?日(?=[始至到])").search(src_text)
        start_date = None
        end_date = None
        if match is not None:
            start_date = match.group()
        match = re.compile("(?<=[到至]).*?日(?=[。止\s])").search(src_text)
        if match is not None:
            end_date = match.group()
        if start_date is not None and end_date is not None:
            _expiry_date = str(start_date) + "-" + str(end_date)

    if _total_value is None:
        regex = ""
        for key in key_dictionary[TOTAL_VALUE_KEY]:
            regex += "((?<=%s)\d+\.?\d+(?=[元]))|" % key
        regex = regex.rstrip("|")
        match = re.compile(regex).search(src_text)
        if match is not None:
            _total_value = match.group()

    _contract.sign_entity = _sign_entity
    _contract.sign_date = _sign_date
    _contract.sign_place = _sign_place
    _contract.delivery_date = _delivery_date
    _contract.delivery_method = _delivery_method
    _contract.payment_method = _payment_method
    _contract.expiry_date = _expiry_date
    _contract.incentive_system = _incentive_system
    _contract.total_value = _total_value
    _contract.unit_price = _unit_price

    return _contract


def write_excel(out_path, type, contract_list):
    if len(contract_list) == 0:
        return
    item = contract_list[0]
    keys, _ = item.serialize()
    data = list()
    data.append(keys)

    for _contract in contract_list:
        _, values = _contract.serialize()
        data.append(values)

    excel_filename = path.join(out_path, type + "合同字段.xlsx")
    to_excel(data, excel_filename)

    for _contract in contract_list:
        form_name = _contract.filename +"_"+ _contract.title
        _form = _contract.form
        form_dir = path.join(out_path, type + "订单")
        if not path.exists(form_dir):
            os.mkdir(form_dir)
        order_path = path.join(form_dir, form_name + ".xlsx")
        if len(_form.keys()) > 0:
            writer = pd.ExcelWriter(order_path)
            for order_name in _form.keys():
                _data = _form[order_name]
                if len(_data) > 1:
                    df = pd.DataFrame(_data)
                    df.to_excel(writer, header=False, na_rep="", index=False, sheet_name=str(order_name))
            writer.close()


def to_excel(data, output_dir):
    df = pd.DataFrame(data)
    df.to_excel(excel_writer=output_dir,
                header=False, na_rep="", index=False)
    print("Write %s succeed" % output_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage="python main.py INPUT_DIR OUTPUT_DIR")
    parser.add_argument('input_dir', type=str, help='输入文件根目录')
    parser.add_argument('output_dir', type=str, help='输出目录')
    args = parser.parse_args()

    root_dir = args.input_dir
    out_dir = args.output_dir

    json_files = file_filter(root_dir)
    err_file = []
    contract_list = []
    for filename, pages in json_files.items():
        try:
            contract = extract_contract(root_dir, pages, filename)
            if contract is not None:
                contract_list.append(contract)
        except Exception as e:
            err_file.append(filename)
    single_contract_list = [e for e in contract_list if e.type == SINGLE_PRODUCT]
    whole_line_contract_list = [e for e in contract_list if e.type == WHOLE_LINE]
    other_contract_list = [e for e in contract_list if e.type == OTHERS]

    if path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    write_excel(out_dir, "单品", single_contract_list)
    write_excel(out_dir, "整线", whole_line_contract_list)
    write_excel(out_dir, "其他", other_contract_list)
