from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from . import main
from .forms import UpdateProfile, BlogPostForm,EditPostForm,CommentForm
from flask_login import login_required, current_user
from ..requests import get_quotes
from .. import db,photos
from ..models import User,Role,BlogPost,Comments

@main.route('/', methods = ['GET','POST'],defaults={"page": 1})
@main.route('/<int:page>', methods=['GET'])
def index(page):
    page = page
    per_page = 4
    posts = BlogPost.query.order_by(BlogPost.posted.des()).paginate(page,per_page,error_out=False)
    quote = get_quotes()
    subscribe

    title = 'Home - Welcome to The Pitch of Your Life'

    return render_template('index.html', title=title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogposts = BlogPost.query.filter_by(user_id=user.id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, blogposts=blogposts)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blogpost/new', methods=['GET', 'POST'])
@login_required
def new_blogpost():
    form = BlogPostForm()


    if form.validate_on_submit():

        blog_title = form.title.data
        blog_subtitle = form.subtitle.data
        author = form.author.data
        content = form.content.data

        new_blogpost = BlogPost(title = blog_title, subtitle=blog_subtitle, author=author, content=content, user_id=current_user.id)
        new_blogpost.save_blogpost()
        return redirect(url_for('.index'))

    title = 'New Blogpost'    
    return render_template('newpost.html' ,blog_form=form, title=title)

@main.route('/posts',methods=['GET', 'POST'] )
@login_required
def get_blogposts():
    blogposts = BlogPost.query.all()

    return render_template('allposts.html',blogposts=blogposts)

@main.route('/blogpost/view/<blogpost_id>',methods=['GET','POST'])
def view_blogpost(blogpost_id):

    blogpost = BlogPost.query.filter_by(id=blogpost_id).first()
    comments = Comments.get_comments(blogpost_id)
    comment_form = CommentForm()
    if current_user.is_authenticated:
        
        if comment_form.validate_on_submit():
            comments = comment_form.description.data

            new_comment = Comments(comment=comments, user_id=current_user.id, blogpost_id=blogpost_id)
            new_comment.save_comment()
        
        comments = Comments.get_comments(blogpost_id)

    return render_template('blogpost.html', blogpost_id=blogpost_id, blogpost=blogpost, comments=comments, comment_form=comment_form)

@main.route('/editpost/<int:id>', methods = ['GET','POST'])
def edit_blogpost(blogpost_id):
    blogpost = BlogPost.query().filter(id==id).first()
    form = BlogPostForm()

    blogpost.blog_title = request.form.get['title']
    blogpost.blog_subtitle = request.form.get['subtitle']
    blogpost.author = request.form.get['author']
    blogpost.content = request.form.get['content']

    if form.validate_on_submit():
        db.session.commit()
        return redirect(url_for('.editpost'))

    return render_template('allposts.html', user_id=current_user.id, blogpost=blogpost)