from Report2T import Report2T
from StyleTrigger import StyleTrigger
from Config import OutputFormat, TriggerTarget
from bs4 import BeautifulSoup


def trigger_name_data(value: str, style: BeautifulSoup):
    text_prop = style.find("style:text-properties")
    if value == "male":
        text_prop["fo:color"] = "#c9211e"


input_path = "/Template/template.xlsx"
output_path = "/"
data = {
    "invoice_date": "aaa",
    "invoice_num": "aaa",
    "product_name": "Abc",
    "bank_num": "XXX-XXX-XXX",
    "bank_account_name": "ABC Company",
    "bank_name": "VCB",
    "customer_name": "ABC",
    "customer_address": "acb",
    "terms_conditions": "abc",
    "item": [
        {
            "name": "abc",
            "num": "abc",
            "price": "abc",
            "total": "abc",
        },
        {
            "name": "abc",
            "num": "abc",
            "price": "abc",
            "total": "abc",
        },
        {
            "name": "abc",
            "num": "abc",
            "price": "abc",
            "total": "abc",
        },
        {
            "name": "abc",
            "num": "abc",
            "price": "abc",
            "total": "abc",
        },
        {
            "name": "abc",
            "num": "abc",
            "price": "abc",
            "total": "abc",
        },
    ],
    "sub_total": "abc",
    "tax": "abc",
    "total": "ac",
}

report_instance = Report2T(input_path, output_path, OutputFormat.PDF, data)

# report_instance.add_style(StyleTrigger("font_size", "text:span", TriggerTarget.SELF, trigger_name_data))
# report_instance.add_image("Image1","./Vi.jpg")
report_instance.exec_convert()
