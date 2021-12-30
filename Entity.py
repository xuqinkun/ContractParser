# -*- coding: utf-8 -*-
import json

SINGLE_PRODUCT = 0
WHOLE_LINE = 1
OTHERS = 2


class Contract:

    def __init__(self):
        self.root_dir = None
        self.filename = None
        self._type = None
        self.text = None

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

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir

    def set_filename(self, filename):
        self.filename = filename

    def set_type(self, _type):
        self._type = _type

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

    def set_text(self, src_text):
        self.text = src_text


if __name__ == '__main__':
    print(Contract().serialize())
