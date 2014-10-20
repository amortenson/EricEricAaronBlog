from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode
import sqlite3
app=Flask(__name__)
conn = sqlite3.connect("post.db")
conn2 = sqlite3.connect("comment.db")
c = conn.cursor()
c2= conn.cursor()
q = "CREATE TABLE IF NOT EXISTS forumstuff(forumid integer, forumname text, author text)"
result = c.execute(q)
##qc -> q for the comments .db file
qc = "CREATE TABLE IF NOT EXISTS poststuff(postid integer, post text)"
result = c2.execute(qc)
conn.commit();


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
    ##list all of the posts using the db
    ##request.args = get
    ##request.form = POST
    if "b" in request.args:
        if (request.args["username"]!="" and
            request.args["title"]!="" and
            request.args["body"]!=""):
            print "success"
        else:
            print "fail"
    
        
    forumTopic = request.args["topic"]
    return render_template("forum.html",topic=forumTopic)
@app.route("/post", methods=["GET","POST"])
def post():
    
    forumTopic = request.args["topic"]
    return render_template("post.html",topic=forumTopic)
     
if __name__=="__main__":
    app.debug=True
    app.run();
