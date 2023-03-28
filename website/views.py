from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_text = request.form.get('text')

        if len(post_title) < 1:
            flash('Title is too short!', category='error')
        else:
            new_post = Post(title=post_title, text=post_text, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("new_post.html", user=current_user)

@views.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.text = request.form.get('text')

        db.session.commit()
        flash('Post updated!', category='success')
        return redirect(url_for('views.home'))

    return render_template("edit_post.html", user=current_user, post=post)

@views.route('/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')

    return redirect(url_for('views.home'))

@views.route('/posts/<username>')
@login_required
def user_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User does not exist.', category='error')
        return redirect(url_for('views.home'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post_detail.html', post=post, user=current_user)
