from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode
import sqlite3, csv
app=Flask(__name__)

conn = sqlite3.connect("posts.db")
c = conn.cursor()
q = "CREATE TABLE IF NOT EXISTS posts(postid integer primary key autoincrement, post text, title text, author text, forumname text)"
c.execute(q)
q = "CREATE TABLE IF NOT EXISTS comments(postid integer,commentid integer, comment text, author text)"
c.execute(q)
conn.commit()


@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def index():
    return render_template("main.html");

@app.route("/forums", methods=["GET","POST"])
def forums():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    q = "CREATE TABLE IF NOT EXISTS posts(postid integer primary key autoincrement, post text, title text, author text, forumname text)"
    c.execute(q)
    q = "CREATE TABLE IF NOT EXISTS comments(postid integer,commentid integer, comment text, author text)"
    c.execute(q)
    conn.commit()
    q = "select distinct posts.forumname from posts"
    tmp =c.execute(q)
    conn.commit()
    topics = []
    for r in tmp:
        topics.append(r)
    print topics
    return render_template("forums.html", topics = topics)

@app.route("/create", methods=["GET","POST"])
def create():
    if request.method=="POST":
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
    return render_template("create.html")

@app.route("/table", methods=["GET","POST"])
def table():
    return render_template("bbcode.html");

@app.route("/forum", methods=["GET","POST"])
def forum():
    
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    q = "select postid, post, title, author from posts where forumname='"+request.args["topic"]+"'"
    result = c.execute(q)
    conn.commit()
    print result
    posts = []
    for r in result:
        posts.append(r)
    print posts
    
    if request.method=="GET":
        forumTopic = request.args["topic"]
    if request.method=="POST":
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
    
    return render_template("forum.html",topic=forumTopic,posts=reversed(posts))

@app.route("/post", methods=["GET","POST"])
def post():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    comments = []
    print request.method +"!!!!!!!!!!!!!!!\n\n\n"
    if (request.method=="GET"):
        q = "select postid,commentid, comment, author from comments where postid='"+request.args["postID"]+"'"
        result = c.execute(q)
        conn.commit()      
        for r in result:
            comments.append(r)
    
        topic = request.args["topic"]
        postid = request.args["postID"]
    if ("comment" in request.form):
        q = "select postid,commentid, comment, author from comments where postid='"+request.form["postID"]+"'"
        result = c.execute(q)
        conn.commit()
        for r in result:
            comments.append(r)
    
        topic = request.form["topic"]
        postid = request.form["postID"]
        body = request.form["body"]
        author = request.form["username"]
        
        if (author!="" and body!=""):
            commentid=0
            conn = sqlite3.connect("posts.db")
            c = conn.cursor()
            q = "select Count(*) from comments where postid='"+request.form["postID"]+"'"
            commentid = c.execute(q)
            ##this just takes the first and only item.
            for i in commentid:
                commentid=i[0]
            q = '''insert into comments values("'''+postid+'''","'''+ str(commentid) +'''","'''+body+'''","'''+author+'''")'''
            c.execute(q)
            conn.commit()
    print comments
    return render_template("post.html",comments=comments,topic=topic,postid=postid)
     
if __name__=="__main__":
    app.debug=True
    app.run();
