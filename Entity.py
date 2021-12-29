# -*- coding: utf-8 -*-
import json

SINGLE_PRODUCT = 0
WHOLE_LINE = 1
OTHERS = 2


class Body:

    def __init__(self):
        self.content = ""
        self.is_form = False

    def set_content(self, content):
        self.content = content

    def set_is_form(self, is_form):
        self.is_form = is_form


class OriginData:

    def __init__(self):
        self.file_name = ""
        self.body_map = {}

    def set_file_name(self, file_name):
        self.file_name = file_name

    def add_body(self, index, body):
        self.body_map[index] = body

    def get_filename(self):
        return self.file_name

    def get_bodymap(self):
        return self.body_map

    pass


class Contract:

    def __init__(self):
        self.type = None
        self.no = None
        self.title = None
        self.customer_name = None
        self.sign_entity = None
        self.product_name = None
        self.total_value = None
        self.sign_place = None
        self.sign_date = None
        self.delivery_method = None
        self.delivery_date = None
        self.payment_method = None
        self.expiry_date = None
        self.incentive_system = None
        self.unit_price = None

    def set_type(self, type):
        self.type = type

    def set_title(self, title):
        self.title = title

    def set_no(self, no):
        self.no = no

    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def set_sign_entity(self, sign_entity):
        self.sign_entity = sign_entity

    def set_product_name(self, product_name):
        self.product_name = product_name

    def set_total_value(self, total_value):
        self.total_value = total_value

    def set_delivery_date(self, delivery_date):
        self.delivery_date = delivery_date

    def set_delivery_method(self, delivery_method):
        self.delivery_method = delivery_method

    def set_unit_price(self, unit_price):
        self.unit_price = unit_price

    def set_incentive_system(self, incentive_system):
        self.incentive_system = incentive_system

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def set_expiry_date(self, expiry_date):
        self.expiry_date = expiry_date

    def set_sign_date(self, sign_date):
        self.sign_date = sign_date

    def set_sign_place(self, sign_place):
        self.sign_place = sign_place

    def serialize(self):
        pairs = self.__dict__.copy()
        key_set = pairs.keys()
        for key in list(key_set):
            if pairs[key] is None:
                pairs.pop(key)
        pairs.pop("type")
        return list(pairs.keys()), list(pairs.values())
    pass


if __name__ == '__main__':
    print(Contract().serialize())
