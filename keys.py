# -*- coding: utf-8 -*-
SIGN_ENTITY_KEY = "签订主体"
PRODUCT_NAME_KEY = "产品名称"
CONTRACT_NO_KEY = "合同编号"
CUSTOMER_NAME_KEY = "客户名称"
SIGN_PLACE_KEY = "签订地点"
PAYMENT_METHOD_KEY = "结算方式和结算周期"
DELIVERY_METHOD_KEY = "运输方式和有效验收"
DELIVERY_DATE_KEY = "交货日期"
SIGN_DATE_KEY = "签订日期"
TOTAL_VALUE_KEY = "合同金额"
EXPIRY_DATE_KEY = "有效期"
UNIT_PRICE_KEY = "约定单价"
INCENTIVE_SYSTEM_KEY = "销售奖励制度"

key_dictionary = {
    CUSTOMER_NAME_KEY: ["甲方", "购货方", "买方", "甲方(购货方)", "需方联系人", "甲方(需方)", "需方", "TO"],
    SIGN_ENTITY_KEY: ["供货方", "卖方", "乙方(供货方)", "供方联系人", "乙方(供方)", "销售单位", "乙方", "供方", "提供方", "FR"],
    PRODUCT_NAME_KEY: ["产品名称", "提供", "设备名称", "产品名称及使用范围"],
    CONTRACT_NO_KEY: ["合同编号", "编号", "订货单号"],
    UNIT_PRICE_KEY: ["产品单价", "单价", "约定单价"],
    SIGN_PLACE_KEY: ["签约地点", "履行地点"],
    PAYMENT_METHOD_KEY: ["结算方式", "货款的结算与支付", "产品的价格与贷款的结算", "产量统计、核对以及结算:"],
    DELIVERY_METHOD_KEY: ["交货地点及方式", "运输方式", "产品的交货时间、地点和方式:", "产品的包装、交付和验收"],
    DELIVERY_DATE_KEY: ["交货日期", "统计周期"],
    SIGN_DATE_KEY: ["签订日期", "订单日期", "日期"],
    TOTAL_VALUE_KEY: ["合计人民币", "总额为", "总计", "金额为"],
    EXPIRY_DATE_KEY: ["有效期限"],
    INCENTIVE_SYSTEM_KEY: ["年销售奖励制度"]
}

capital_2_number = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
                    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "十一": 11, "十二": 12}
number_2_capital = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八",
                    9: "九", 10: "十", 11: "十一", 12: "十二", }
