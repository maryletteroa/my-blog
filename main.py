from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)
Bootstrap(app)

SMTP = os.environ.get("SMTP")
MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    return render_template("post.html", post=requested_post)

@app.route("/edit/<int:post_id>", methods=["GET","POST"])
def edit_post(post_id):
    page_title = "Edit Post"
    post = BlogPost.query.get(post_id)
    if post:
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
            )
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.subtitle = edit_form.subtitle.data
            post.body = edit_form.body.data
            post.author = edit_form.author.data
            post.img_url = edit_form.img_url.data
            db.session.commit()
            return redirect(url_for("show_post", index=post.id))
    return render_template("make-post.html", form=edit_form, page_title=page_title)

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

@app.route("/new-post", methods=["GET","POST"])
def new_post():
    form = CreatePostForm()
    page_title = "New Post"
    if form.validate_on_submit():
        post = BlogPost(title = form.title.data, 
            subtitle = form.title.data, 
            date = datetime.now().strftime("%B %d, %Y"),
            body = form.body.data,
            author = form.author.data,
            img_url = form.img_url.data,
            )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, page_title=page_title)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

if __name__ == "__main__":
    app.run()
