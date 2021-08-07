from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def home():
    blog_url = "https://api.npoint.io/e42b353ee387383898c7"
    response = requests.get(blog_url)
    posts = response.json()
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:id>")
def get_post(id):
    blog_url = "https://api.npoint.io/e42b353ee387383898c7"
    response = requests.get(blog_url)
    post = response.json()[id-1]
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
