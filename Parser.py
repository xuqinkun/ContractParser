# -*- coding: utf-8 -*-
import json
import os
import os.path as path

import pandas as pd

from Keys import *
from Entity import *

root = "/Users/xqk/Downloads/02.陶加国内"


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


def _extract_form(doc):
    return doc["form_blocks"]


def _extract_text(doc):
    if "lines" in doc.keys():
        return doc["lines"]
    else:
        return ""


def read_content_per_contract(pages={}):
    page_num = len(pages.keys())
    orig_data = OriginData()
    with open(pages[1]) as file:
        doc = json.load(file)
        table_list = doc["pages"][0]["table"]
        title = table_list[0]["lines"][0]['text']
        if not _contains_any(title, title_key_set):
            return None
    index = 0
    for i in range(1, page_num + 1, 1):
        # path = pages[i]
        with open(pages[i], "r") as file:
            content = json.load(file)
            table_list = content['pages'][0]['table']
            for table in table_list:
                body = Body()
                is_form = table["type"]
                body.is_form = is_form
                if is_form:
                    content = _extract_form(table)
                else:
                    content = _extract_text(table)
                body.set_content(content)
                orig_data.add_body(index, body)
                index += 1
    return orig_data


def _parse_form(form, dataframe):
    table_names = [cell["data"] for cell in form if cell['start_row'] == 0]
    table_values = [cell["data"] for cell in form if cell['start_row'] > 0]
    col_num = len(table_names)
    row_num = int(len(table_values) / col_num)
    form_data = []
    for row_idx in range(row_num):
        row_data = {}
        for col_idx in range(col_num):
            row_data[table_names[col_idx]] = table_values[row_idx * col_num + col_idx]
        form_data.append(row_data)
    if "form" not in dataframe:
        dataframe["form"] = []
    dataframe["form"] += form_data
    return 1


def _parse_text(content, dataframe):
    for line in content:
        text = line['text'].strip()
        colon = ":"
        if colon in text:
            tokens = text.split(colon)
            if len(tokens) == 2:
                key, value = tokens
                if len(value.strip()) != 0 and key not in dataframe.keys():
                    dataframe[key] = value


def parse_field(dataframe, field_key_list):
    key_set = dataframe.keys()
    for key in field_key_list:
        for target in key_set:
            if key in target or target in key:
                return dataframe[target]
    return None


def assemble_contract(dataframe):
    contract = Contract()
    contract.set_no(parse_field(dataframe, key_dictionary[CONTRACT_NO_KEY]))
    contract.set_customer_name(parse_field(dataframe, key_dictionary[CUSTOMER_NAME_KEY]))
    contract.set_sign_entity(parse_field(dataframe, key_dictionary[SIGN_ENTITY_KEY]))
    contract.set_sign_date(parse_field(dataframe, key_dictionary[SIGN_DATE_KEY]))
    contract.set_sign_place(parse_field(dataframe, key_dictionary[SIGN_PLACE_KEY]))
    contract.set_delivery_date(parse_field(dataframe, key_dictionary[DELIVERY_DATE_KEY]))
    contract.set_delivery_method(parse_field(dataframe, key_dictionary[DELIVERY_METHOD_KEY]))
    contract.set_payment_method(parse_field(dataframe, key_dictionary[PAYMENT_METHOD_KEY]))
    contract.set_expiry_date(parse_field(dataframe, key_dictionary[EXPIRY_DATE_KEY]))
    contract.set_incentive_system(parse_field(dataframe, key_dictionary[INCENTIVE_SYSTEM_KEY]))

    return contract


def extract_contract(ori_data_list):
    contract_list = []
    for data in ori_data_list:
        bodies = data.get_bodymap()
        title = data.get_filename()
        n = len(bodies)
        i = 0
        contract_json = {}
        while i < n:
            body = bodies[i]
            if body.is_form:
                step = _parse_form(body.content, contract_json)
                i += step
            else:
                _parse_text(body.content, contract_json)
                i += 1
        print(title)
        contract = assemble_contract(contract_json)
        contract.title = title
        if contract.incentive_system is not None:
            contract.type = SINGLE_PRODUCT
        elif contract.unit_price is not None:
            contract.type = WHOLE_LINE
        else:
            contract.type = OTHERS
        contract_list.append(contract)
    return contract_list


def write_excel(out_path, contract_list):
    item = contract_list[0]
    keys, _ = item.serialize()
    data = list()
    data.append(keys)
    for contract in contract_list:
        _, values = contract.serialize()
        data.append(values)
    df = pd.DataFrame(data)
    df.to_excel(out_path, index=False)
    print("Write %s succeed" % out_path)


if __name__ == '__main__':
    json_files = file_filter(root)
    err_file = []
    orig_data_list = []
    for name, pages in json_files.items():
        try:
            orig_data = read_content_per_contract(pages)
            orig_data.file_name = name
            if orig_data is not None:
                orig_data_list.append(orig_data)
        except Exception as e:
            err_file.append(name)
    # print(err_file)
    contract_list = extract_contract(orig_data_list)
    single_contract_list = [e for e in contract_list if e.type == SINGLE_PRODUCT]
    whole_line_contract_list = [e for e in contract_list if e.type == WHOLE_LINE]
    other_contract_list = [e for e in contract_list if e.type == OTHERS]
    write_excel("others.xlsx", other_contract_list)
