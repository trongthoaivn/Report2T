from Report2T import Report2T
from StyleTrigger import StyleTrigger
from Config import OutputFormat, TriggerTarget
from bs4 import BeautifulSoup 

def trigger_name_data(value : str, style : BeautifulSoup):
    text_prop = style.find("style:text-properties")
    if value == "male":
        text_prop["fo:color"]="#c9211e"


input_path = "./a.docx"
output_path = "./"
data = {"sex":"male"}

report_instance = Report2T(input_path, output_path, OutputFormat.PDF, data)

report_instance.add_style(StyleTrigger("test", "text:span", TriggerTarget.SELF, trigger_name_data))
report_instance.add_image("Image1","./2672292.jpg")
report_instance.exec_convert()
