# -*- coding: utf-8 -*-

SINGLE_PRODUCT = 0
WHOLE_LINE = 1
OTHERS = 2


class Contract:

    def __init__(self):
        self.root_dir = None
        self.filename = ""
        self._type = None
        self.text = None

        self.no = ""
        self._title = ""
        self.customer_name = ""
        self.sign_entity = ""
        self.product_name = ""
        self.total_value = ""
        self.sign_place = ""
        self.sign_date = ""
        self.delivery_method = ""
        self.delivery_date = ""
        self.payment_method = ""
        self.expiry_date = ""
        self.incentive_system = None
        self.unit_price = ""
        self._form = None

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, form):
        self._form = form

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir

    def set_filename(self, filename):
        self.filename = filename

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._type = _type

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, _title):
        self._title = _title

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
        pairs.pop("_type")
        pairs.pop("text")
        pairs.pop("_form")
        return list(pairs.keys()), list(pairs.values())
    pass

    def set_text(self, src_text):
        self.text = src_text


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
