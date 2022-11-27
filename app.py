from flask import Flask, render_template, request, escape, redirect, abort, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from database import Post, User, db, app
from sqlalchemy import func
import datetime
import hashlib

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/myposts')
def ranking():
    allposts = db.session.query(Post).filter(
            Post.username == current_user.username).order_by(Post.id.desc()).all()
    return render_template("myposts.html", posts=allposts)
  

@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = escape(request.form["username"])
        password = request.form["password"]
        if (len(username) >= 80):
            flash("ユーザー名が長すぎます。80文字までにしてください",
                  category='alert alert-danger')
            return redirect('/register')
        user = User.query.filter_by(username=username).scalar()

        if user is not None:
            print(user)
            flash("そのユーザー名はすでに使われています",
                  category='alert alert-danger')
            return redirect(url_for('register'))
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("登録しました！", category='alert alert-success')
        return redirect("/about")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html",)
    else:
        username = escape(request.form["username"])
        password = request.form["password"]
        user=None
        if (User.query.filter_by(username=username).first()!=None):
            user = User.query.filter_by(username=username).first()
        if not user.check_password(password):
            flash("ログインに失敗しました",
                  category='alert alert-danger')
            return redirect(url_for('login'))
        login_user(user)
        flash("ログインしました！", category='alert alert-success')
        return redirect("/about")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if current_user.is_authenticated == False:
        return render_template("submit.html")
    if request.method == 'POST':
        text =  request.form["file"]
        sub = Post()
        sub.username = current_user.username
        sub.text = text
        sub.text_hash=hashlib.md5(text.encode()).hexdigest()
        sub.postdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(sub)
        db.session.commit()
        flash("投稿しました。", category='alert alert-success')
        return redirect("/myposts")
    else:
        return render_template("submit.html")


if __name__ == '__main__':
    with app.app_context():
        app.secret_key = "my super secret string!!!"
        login_manager = LoginManager()
        login_manager.init_app(app)
        @login_manager.user_loader
        def load_user(username):
            return User.query.filter_by(username=username).first()
    
        db.create_all()
        app.run(debug=True)
