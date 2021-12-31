# -*- coding: utf-8 -*-

from Keys import *

SINGLE_PRODUCT = 0
WHOLE_LINE = 1
OTHERS = 2


class Contract:

    def __init__(self):
        self._first_dir = None
        self._parent_dir = None
        self._filename = None
        self._type = None
        self._text = None

        self._no = ""
        self._title = ""
        self._customer_name = ""
        self._sign_entity = ""
        self._product_name = ""
        self._total_value = ""
        self._sign_place = ""
        self._sign_date = ""
        self._delivery_method = ""
        self._delivery_date = ""
        self._payment_method = ""
        self._expiry_date = ""
        self._incentive_system = None
        self._unit_price = ""
        self._form = None

    @property
    def first_dir(self):
        return self.first_dir

    @first_dir.setter
    def first_dir(self, value):
        if value is None:
            value = ""
        self._first_dir = value

    @property
    def parent_dir(self):
        return self._parent_dir

    @parent_dir.setter
    def parent_dir(self, value):
        if value is None:
            value = ""
        self._parent_dir = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value is None:
            value = ""
        self._filename = value

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value):
        if value is None:
            value = ""
        self._form = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value is None:
            value = ""
        self._type = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value is None:
            value = ""
        self._title = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value is None:
            value = ""
        self._type = value

    @property
    def customer_name(self):
        return self._customer_name

    @customer_name.setter
    def customer_name(self, value):
        if value is None:
            value = ""
        self._customer_name = value

    @property
    def sign_entity(self):
        return self._sign_entity

    @sign_entity.setter
    def sign_entity(self, value):
        if value is None:
            value = ""
        self._sign_entity = value

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        if value is None:
            value = ""
        self._product_name = value

    @property
    def delivery_date(self):
        return self._delivery_date

    @delivery_date.setter
    def delivery_date(self, value):
        if value is None:
            value = ""
        self._delivery_date = value

    @property
    def delivery_method(self):
        return self._delivery_method

    @delivery_method.setter
    def delivery_method(self, value):
        if value is None:
            value = ""
        self._delivery_method = value

    @property
    def expiry_date(self):
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        if value is None:
            value = ""
        self._expiry_date = value

    @property
    def incentive_system(self):
        return self._incentive_system

    @incentive_system.setter
    def incentive_system(self, value):
        if value is None:
            value = ""
        self._incentive_system = value

    @property
    def payment_method(self):
        return self._payment_method

    @payment_method.setter
    def payment_method(self, value):
        if value is None:
            value = ""
        self._payment_method = value

    @property
    def sign_date(self):
        return self._sign_date

    @sign_date.setter
    def sign_date(self, value):
        if value is None:
            value = ""
        self._sign_date = value

    def set_sign_date(self, sign_date):
        if sign_date is None:
            sign_date = ""
        self.sign_date = sign_date

    @property
    def sign_place(self):
        return self._sign_place

    @sign_place.setter
    def sign_place(self, value):
        if value is None:
            value = ""
        self._sign_place = value

    @property
    def total_value(self):
        return self._total_value

    @total_value.setter
    def total_value(self, value):
        if value is None:
            value = ""
        self._total_value = value

    @property
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value):
        if value is None:
            value = ""
        self._unit_price = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            value = ""
        self._text = value

    def serialize(self):
        pairs = self.__dict__.copy()
        key_set = pairs.keys()
        for key in list(key_set):
            if pairs[key] is None:
                pairs.pop(key)

        pairs.pop("_type")
        pairs.pop("_text")
        pairs.pop("_title")
        pairs.pop("_form")
        key_set = list(pairs.keys())
        key_set[key_set.index("_no")] = CONTRACT_NO_KEY
        key_set[key_set.index("_sign_date")] = SIGN_DATE_KEY
        key_set[key_set.index("_first_dir")] = "一级目录"
        key_set[key_set.index("_parent_dir")] = "末级目录"
        key_set[key_set.index("_filename")] = "文件名(pdf)"
        key_set[key_set.index("_sign_entity")] = SIGN_ENTITY_KEY
        key_set[key_set.index("_incentive_system")] = INCENTIVE_SYSTEM_KEY
        key_set[key_set.index("_unit_price")] = UNIT_PRICE_KEY
        key_set[key_set.index("_delivery_method")] = DELIVERY_METHOD_KEY
        key_set[key_set.index("_delivery_date")] = DELIVERY_DATE_KEY
        key_set[key_set.index("_customer_name")] = CUSTOMER_NAME_KEY
        key_set[key_set.index("_sign_place")] = SIGN_PLACE_KEY
        key_set[key_set.index("_product_name")] = PRODUCT_NAME_KEY
        key_set[key_set.index("_expiry_date")] = EXPIRY_DATE_KEY
        key_set[key_set.index("_payment_method")] = PAYMENT_METHOD_KEY
        key_set[key_set.index("_total_value")] = TOTAL_VALUE_KEY
        return list(key_set), list(pairs.values())

    pass


class Cell:

    def __init__(self, data=None):
        self.start_row = None
        self.end_row = None
        self.start_column = None
        self.end_column = None
        self.data = None
        self.position = None
        self.org_position = None
        self.char_position = None
        self.lines = None
        if data:
            self.__dict__ = data
