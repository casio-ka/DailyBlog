from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
    def __init__(self,id,author,quote):
        self.id = id
        self.author = author
        self.quote = quote

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

class HeaderImage(db.Model):
    __tablename__='header_image'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    blogpost_id = db.Column(db.Integer,db.ForeignKey("blogposts.id"))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    password_hash = db.Column(db.String(255))
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class BlogPost (db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    subtitle = db.Column(db.String(70))
    author = db.Column(db.String(70))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=user_id)
    dateposted = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comments', backref='blogposts', lazy='dynamic')
    header_img_path = db.Column(db.String())
    headerimage = db.relationship('HeaderImage',backref = 'blogposts',lazy = "dynamic")

    def save_blogpost(self):
        db.session.add(self)
        db.session.commit()

    @classmethod 
    def get_blogposts():
        blogposts = BlogPost.query.all()

        return blogposts

    @classmethod
    def get_blogpost(cls, blogpost_id):
        blogpost = BlogPost.query.filter_by(id=blogpost_id).one()

        return blogpost
    
    @classmethod
    def get_blogposts_by_user_id(cls, user_id):
        blogposts = BlogPost.query.filter_by(user_id=user_id).first()
        user = User.query.filter_by(user_id=user_id)

        return blogposts


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300))
    name = db.Column(db.String(255),index = True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", foreign_keys=user_id)
    blogpost_id = db.Column(db.Integer, db.ForeignKey("blogposts.id"))
    

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, blogpost):
        comments = Comments.query.filter_by(blogpost_id=blogpost).all()
        return comments

class Subscribers (db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique = True, index = True)


