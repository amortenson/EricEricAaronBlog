from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode

app=Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("main.html")
    else:
        button = request.form["b"]
        blog = request.form["blog"]
        title = request.form["title"]
        body = request.form["body"]
        return render_template("main.html")

if __name__=="__main__":
    app.debug=True
    app.run();
