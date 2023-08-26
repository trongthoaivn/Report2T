from flask import Flask, render_template, request
from Report2T import Report2T
from Config import OutputFormat
import os


app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="static",
)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/export", methods=["POST"])
def export_invoice():
    data = request.json

    current_path = os.getcwd()
    input_path = os.path.join(current_path, "Template", "template.xlsx")
    output_path = os.path.join(current_path, "Template")
    report_instance = Report2T(input_path, output_path, OutputFormat.PDF, data)
    report_instance.exec_convert()

    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
