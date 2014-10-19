from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode
import sqlite3

app=Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("main.html")
    else:
        ##no idea if the form works. request.args does :^)
        button = request.form["b"]
        blog = request.form["blog"]
        title = request.form["title"]
        body = request.form["body"]
        return render_template("main.html")
@app.route("/forum", methods=["GET","POST"])
def forum():
    forumTopic = request.args["topic"]
    return render_template("forum.html",topic=forumTopic)
@app.route("/post", methods=["GET","POST"])
def post():
    forumTopic = request.args["topic"]
    return render_template("post.html",topic=forumTopic)



if __name__=="__main__":
    app.debug=True
    app.run();
