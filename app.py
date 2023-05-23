from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, UserForm, PasswordForm, NamerForm, PostForm, SearchForm
from flask_ckeditor import CKEditor
import os

# to-do FUNCTIONAL
# user registration, (login, logout, password reset),
# recipe uploading, (recipe editing, recipe deleting), recipe browsing and interaction features
# search bar, recipe rating, recipe commenting, (recipe favoriting)
# (admin page)

# to-do NON-FUNCTIONAL
# responsive design, secure authentication, efficient database storage, scalability

# Create a Flask Instance
app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)
# Add Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:KH5!ajwQQ72uxrh@localhost/mydb'

app.config['SECRET_KEY'] = "mysecretkey"  # For CSRF Protection (Forms)

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Initialize Login Manager (flask_login)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:KH5!ajwQQ72uxrh@localhost/my_db'


# Pass Data to Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


#@app.route('/upload', methods=['GET', 'POST'])
#def upload():
#    form = UploadForm()
#
#    if form.validate_on_submit():
#        filename = secure_filename(form.file.data.filename)
#        form.file.data.save('uploads/' + filename)
#        return redirect(url_for('upload'))
#
#    return render_template('upload.html', form=form)


# Create an Admin Page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 23:
        return render_template('admin.html')
    else:
        flash('You do not have permission to access this page')
        return redirect(url_for('dashboard'))


# Create Search Function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = BlogPost.query
    if form.validate_on_submit():
        # Grab the search string from the form
        post.searched = form.searched.data
        # Query the database and filter by the search string
        posts = posts.filter(BlogPost.content.like("%" + post.searched + "%"))
        posts = posts.order_by(BlogPost.title.desc()).all()

        return render_template('search.html', searched=post.searched, form=form, posts=posts)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is not None:
            # Check Password Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Logged in successfully!')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect Password. Please try again.')
        else:
            flash('That user does not exist. Please try again or register.')
    return render_template('login.html', form=form)


# Create Logout Function
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('login'))


# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/posts')
def posts():
    # Grab a list of posts from database
    posts = BlogPost.query.order_by(BlogPost.date_posted)
    return render_template('posts.html', posts=posts)


@app.route('/posts/<int:id>')
def post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    form = PostForm()
    id = current_user.id
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        # Update the Database
        # db.session.update(post)
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated')
        return redirect(url_for('post', id=post.id))

    if id == post.poster_id or id == 23:
        form.title.data = post.title
        form.content.data = post.content
        form.slug.data = post.slug
        return render_template('edit_post.html', form=form)
    else:
        flash('You cannot edit this post')
        posts = BlogPost.query.order_by(BlogPost.date_posted)
        return render_template('posts.html', posts=posts)



# Delete Post
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = BlogPost.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster_id or id == 23:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Post has been deleted')
            posts = BlogPost.query.order_by(BlogPost.date_posted)
            return render_template('posts.html', posts=posts)
        except:
            flash('There was an error deleting the post')
            posts = BlogPost.query.order_by(BlogPost.date_posted)
            return render_template('posts.html', posts=posts)
    else:
        flash('You cannot delete this post')
        posts = BlogPost.query.order_by(BlogPost.date_posted)
        return render_template('posts.html', posts=posts)


# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        # Add Data to the Database
        poster = current_user.id
        post_pic = request.files['post_pic']
        pic_filename = secure_filename(post_pic.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save the picture
        post_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
        # Change it to a string to save to database
        post_pic = pic_name
        post = BlogPost(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data,
                        post_pic=post_pic)
        # Clear Form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        # Add to the Database
        db.session.add(post)
        db.session.commit()

        # Flash Message
        flash('Blog Post Added')
    return render_template('add_post.html', form=form)


# Create a function to add data to the database
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, method="sha256")
            # Add Data to the Database
            user = Users(name=form.name.data, username=form.username.data, email=form.email.data, favorite_color=form.favorite_color.data,
                         password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash('User Added Successfully!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


# Create a function to delete data from the database
# Cannot delete a user that has a post
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
        name = None
        form = UserForm()
        user_to_delete = Users.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("Data deleted successfully.")

            our_users = Users.query.order_by(Users.date_added)
            return render_template('add_user.html', form=form, name=name, our_users=our_users)
        except:
            flash("There was a problem deleting data.")
            our_users = Users.query.order_by(Users.date_added)
            return render_template('add_user.html', form=form, name=name, our_users=our_users)
    else:
        flash("You cannot delete another user's account")
        return redirect( url_for('dashboard'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            # return redirect('/users')
            flash("Data updated successfully.")
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
        except:
            flash("There was a problem updating data.")
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id=id)


# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # Lookup user by email address
        pw_to_check = Users.query.filter_by(email=email).first()
        # Check the password
        passed = check_password_hash(pw_to_check.password_hash, password)

        flash('Form Submitted Successfully!')
    return render_template('test_pw.html', email=email, password=password, pw_to_check=pw_to_check, passed=passed,
                           form=form)


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted Successfully!')
    return render_template('name.html', form=form, name=name)


@app.route('/blog')
def blog():
    posts = [{'title': 'Post 1', 'content': 'This is the content of post 1. Lorem ipsum dolor sit amet.'},
             {'title': 'Post 2', 'content': 'This is the content of post 2. Lorem ipsum dolor sit amet.'}
             ]
    return render_template('blog.html', sunny=True, author='Serdar', posts=posts)


if __name__ == '__main__':
    app.run()


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Create a Blog Post Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    post_pic = db.Column(db.String(255), nullable=True)
    # Create a foreign key to refer to primary key of a user
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer)


# Create a Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Add Password Hashing
    password_hash = db.Column(db.String(128))
    # Create a relationship between BlogPost and Users
    posts = db.relationship('BlogPost', backref='poster')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

