#Imports
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import getquotes
from app.forms import LoginForm
from flask_login import login_required, current_user
from ..models import User,Role
from .forms import BlogForm,UpdateProfile
from .. import db
import datetime
from ..email import mail_message
# import markdown2 


@main.route('/index', methods=['GET', 'POST'])
def home():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Pitch(body=form.blog.data, author=current_user,
                     category=form.category.data)
        db.session.add(blog)
        db.session.commit()
        flash('Your blog is now live!')
    
        return redirect(url_for('main.index'))

    return render_template("index.html", title='Home Page', form=form)

@main.route('/')
def index():
   
   title = 'The Random Quotes'

   myquote = getquotes()

   quote = myquote['quote']
   quote_author = myquote['author']


  

   return render_template('quotes.html', title=title,quote = quote, quote_author = quote_author)


@main.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('index')
    return render_template('auth/login.html', title='Sign In', form=form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    legend = 'Newest Blog'
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.text.data
        category = form.category.data

        new_blog = Blog(blog_title = title,blog_content = blog, category = category,user = current_user)
        new_blog.save_blog()

        subscriber = Subscriber.query.all()
        for email in subscriber:
            mail_message("New Blog Post from BumbleBee! ","email/postnotification",email.email,subscriber=subscriber)
        return redirect(url_for('main.index'))

        title = 'New Blog'
    return render_template('new_blog.html', legend = legend, title = title, blog_form = form)

@main.route('/blog/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_blog(id):
    blog = Blog.get_blog(id)
    db.session.delete(blog)
    db.session.commit()

    return render_template('blogs.html', id=id, blog = blog)


@main.route('/blog/comment/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    blog_id = comment.blog
    Comment.delete_comment(id)

    return redirect(url_for('main.blog',id=blog_id))

@main.route('/blog/<int:id>', methods = ["GET","POST"])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.text.data
        name = form.name.data

        new_comment = Comment(comment = comment, name = name, blog_id = blog)

        new_comment.save_comment()

    comments = Comment.get_comments(blog)

    return render_template('blog.html', blog = blog, comment_form = form,comments = comments, date = posted_date)

@main.route('/user/<uname>/blogs', methods = ['GET','POST'])
def user_blogs(uname):
     user = User.query.filter_by(username = uname).first()
     blogs = Blog.query.filter_by(user_id = user.id).all()

     return render_template('profile/blogs.html', user = user, blogs = blogs)

@main.route('/blogs/recent', methods = ['GET','POST'])
def blogs():
    blogs = Blog.query.order_by(Blog.id.desc()).limit(5)

    return render_template('blogs.html',blogs = blogs)


@main.route('/blog/<int:id>/update', methods = ['GET','POST'])
@login_required
def update_blog(id):
    legend = 'Update Blog'
    blog = Blog.get_blog(id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.blog_title = form.title.data
        blog.blog_content = form.text.data
        blog.category = form.category.data
        db.session.commit()
        return redirect(url_for('main.blog', id = id))
    elif request.method == 'GET':
        form.title.data = blog.blog_title
        form.text.data = blog.blog_content
    form.category.data = blog.category
    return render_template('new_blog.html', legend = legend, blog_form = form, id=id)
