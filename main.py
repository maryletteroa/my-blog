from flask import Flask, render_template, request
import requests
import smtplib, ssl
import os

SMTP = os.environ.get("SMTP")
MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        page_title = f"Successfully sent your message"
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        message = request.form["message"]
        email_body = f"Name: {name}\nEmai: {email}\nMessage: {message}"

        ## comment out when sending emails for real ##
        # with smtplib.SMTP_SSL(SMTP, 465, context=ssl.create_default_context()) as connection:
        #     connection.login(user=MY_EMAIL, password=PASSWORD)
        #     connection.sendmail(
        #         from_addr=MY_EMAIL, 
        #         to_addrs=TO_EMAIL, 
        #         msg=f"Subject:New Message\n\n{email_body}"
        #     )
        
        print(email_body)
    else:
        page_title = "Contact Me"
    return render_template("contact.html", page_title=page_title)

@app.route("/post/<int:id>")
def get_post(id):
    blog_url = "https://api.npoint.io/e42b353ee387383898c7"
    response = requests.get(blog_url)
    post = response.json()[id-1]
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run()
