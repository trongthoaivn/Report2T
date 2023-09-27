from flask import Flask, render_template, request, Response
from Report2T import Report2T
from Config import OutputFormat, TriggerTarget
from StyleTrigger import StyleTrigger
from bs4 import BeautifulSoup
import os
import base64


app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="static",
)

def sale_style(value: str, style: BeautifulSoup):
    text_prop = style.find("style:text-properties")
    text_prop["style:text-line-through-type"] = "single"
    text_prop["fo:color"] = "#ffffff"
    text_prop["style:use-window-font-color"] = "false"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/export", methods=["POST"])
def export_invoice():
    data = request.json

    current_path = os.getcwd()
    input_file_path = os.path.join(current_path, "Template", "template.xlsx")
    output_dir_path = os.path.join(current_path, "Template")
    report_instance = Report2T(input_file_path, output_dir_path, OutputFormat.PDF, data)
    # add image
    if data["product_img"] != "":
        report_instance.add_image("product_image", os.path.join(current_path, "static", data["product_img"]))
        
    report_instance.add_style(StyleTrigger("sale", "text:p", TriggerTarget.PARENT, sale_style))
        
    report_instance.exec_convert()

    output_file_path = os.path.join(current_path, "Template", "template.pdf")

    if os.path.exists(output_file_path):
        with open(output_file_path, "rb") as pdf:
            res = base64.b64encode(pdf.read())
            return Response(response=res, status=200, mimetype="application/pdf")
    else:
        return Response(status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
