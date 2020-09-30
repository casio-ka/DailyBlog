from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from . import main
from .forms import UpdateProfile, BlogPostForm,SubscribeForm,WriterCommentForm,UserCommentForm
from flask_login import login_required, current_user
from ..requests import get_quotes
from .. import db,photos
from sqlalchemy import asc,desc
from ..models import User,Role,BlogPost,Comments, Subscribers
from ..email import mail_message

@main.route('/', methods = ['GET','POST'],defaults={"page": 1})
@main.route('/<int:page>', methods=['GET'])
def index(page):
    page = page
    per_page = 3
    latest = BlogPost.query.order_by(desc(BlogPost.dateposted)).limit(3).all()
    quote = get_quotes()
    subform= SubscribeForm()

    title = 'Home - Welcome to The Pitch of Your Life'
    
    if subform.validate_on_submit():

        if Subscribers.query.filter_by(email = subform.email.data).first():
            flash ('Email already in user', 'danger')
        else:
            sub = User(email = subform.email.data)
            db.session.add(sub)
            db.session.commit()

            mail_message("DailyBlog Subscriber" , "email/sub_user", sub.email)
            flash("Subscribed successfully","success")
            return redirect(request.referrer)

    return render_template('index.html', subform=subform, quote=quote, latest=latest)


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


@main.route('/blogposts', methods = ['GET','POST'],defaults={"page": 1})
@main.route('/blogposts<int:page>',methods=['GET'] )
def get_blogposts(page):
    page = page
    per_page = 3
    blogposts = BlogPost.query.order_by(BlogPost.dateposted.desc()).paginate(page,per_page,error_out=False)

    return render_template('allposts.html',blogposts=blogposts)
@main.route('/blogpost/view/<blogpost_id>', methods=['POST'])
def post_comment(blogpost_id):

    blogpost = BlogPost.query.filter_by(id=blogpost_id).first()
    comments = Comments.get_comments(blogpost_id)
    comment_form = WriterCommentForm()
    usercomment_form = UserCommentForm()

    if comment_form.validate_on_submit or usercomment_form.validate_on_submit():
        if current_user.is_authenticated:
            name = current_user.username
            comment = comment_form.description.data
        else:
            name = usercomment_form.name.data
            comment = usercomment_form.description.data
        
        new_comment = Comments(name=name, comment=comment, blogpost_id=blogpost_id)
        new_comment.save_comment()

        return redirect(request.referrer)

@main.route('/blogpost/view/<blogpost_id>',methods=['GET','POST'])
def view_blogpost(blogpost_id):

    blogpost = BlogPost.query.filter_by(id=blogpost_id).first()
    user = User.query.filter_by(id=blogpost.user_id)
    comments = Comments.get_comments(blogpost_id)
    comment_form = WriterCommentForm()
    usercomment_form = UserCommentForm()

    return render_template('blogpost.html', blogpost_id=blogpost_id, blogpost=blogpost, comments=comments, comment_form=comment_form, usercomment_form=usercomment_form, user=user)


@main.route('/blogpost/update/<int:blogpost_id>', methods = ['GET','POST'])
@login_required
def update_blogpost(blogpost_id):
    blogpost = BlogPost.query.filter_by(id=blogpost_id).first()
    form = BlogPostForm()

    if form.validate_on_submit():
        blogpost.title = form.title.data
        blogpost.subtitle = form.subtitle.data
        blogpost.author = form.author.data
        blogpost.content = form.content.data
        db.session.commit()

        return redirect(url_for('.index'))

    else:
        title = 'Edit Post'
        return render_template('newpost.html', title= title, blogpost=blogpost, blog_form=form, action="Edit" )

@main.route('/blogpost/edit/<blogpost_id>', methods=['GET'])
def edit_blogpost(blogpost_id):
    comment_form = WriterCommentForm()
    usercomment_form = UserCommentForm()
    blogpost = BlogPost.query.filter_by(id=blogpost_id).first()
    user = User.query.filter_by(id=blogpost.user_id)
    comments = Comments.get_comments(blogpost_id)
    return render_template('editpost.html', blogpost=blogpost, comments=comments, blogpost_id=blogpost.id, comment_form = comment_form, usercomment_form=usercomment_form, user =user)