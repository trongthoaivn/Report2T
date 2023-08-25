from flask import Flask, render_template


app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="static",
)


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
