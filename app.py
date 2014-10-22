from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode
import sqlite3, csv
app=Flask(__name__)

conn = sqlite3.connect("posts.db")
c = conn.cursor()
q = "CREATE TABLE IF NOT EXISTS posts(postid integer primary key autoincrement, post text, title text, author text, forumname text)"
c.execute(q)
q = "CREATE TABLE IF NOT EXISTS comments(postid integer, comment text, author text)"
c.execute(q)
conn.commit()


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
        author = request.form["author"]
        body = request.form["body"]
        if (blog!="" and title!="" and author!="" and body!="") :
            print "success"
            conn = sqlite3.connect("posts.db")
            c = conn.cursor()
            q = '''insert into posts values(NULL,"'''+body+'''","'''+title+'''","'''+author+'''","'''+blog+'''")'''
            c.execute(q)
            q = "select * from posts"
            result = c.execute(q)
            conn.commit()
            for r in result:
                print r
        return render_template("main.html")
@app.route("/forum", methods=["GET","POST"])
def forum():
    if request.method=="GET":
        forumTopic = request.args["topic"]
        
        return render_template("forum.html",topic=forumTopic)
    ##list all of the posts using the db
    ##request.args = get
    ##request.form = POST
    else:
        body = request.form["body"]
        title = request.form["title"]
        author = request.form["username"]
        blog = request.form["topic"]
        if (author!="" and title!="" and body!=""):
            conn = sqlite3.connect("posts.db")
            c = conn.cursor()
            q = '''insert into posts values(NULL,"'''+body+'''","'''+title+'''","'''+author+'''","'''+blog+'''")'''
            c.execute(q)
            q = "select * from posts"
            result = c.execute(q)
            conn.commit()
            for r in result:
                print r
            forumTopic = request.form["topic"]
        else:
            forumTopic = request.args["topic"]
        return render_template("forum.html",topic=forumTopic)

@app.route("/post", methods=["GET","POST"])
def post():
    ##get the current postid using sqlite
    ##get the post id of 
    postID = 1
    commentID = 1
    if "comment" in request.args:
        if (request.args["username"]!="" and
            request.args["body"]!=""):
            print "success"
        else:
            print "fail"
    
    forumTopic = request.args["topic"]
    return render_template("post.html",topic=forumTopic)
     
if __name__=="__main__":
    app.debug=True
    app.run();
