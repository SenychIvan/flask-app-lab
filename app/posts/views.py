from flask import render_template, redirect, url_for, flash, request
from app.posts import posts_bp
from app import db
from app.posts.models import Post
from app.posts.forms import PostForm
from datetime import datetime

# --------------------- CREATE ---------------------
@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            author="Anonymous"
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully!", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/add_post.html", form=form)

# --------------------- READ ALL ---------------------
@posts_bp.route("/", methods=["GET"])
def all_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts/all_posts.html", posts=posts)

# --------------------- READ ONE ---------------------
@posts_bp.route("/<int:id>", methods=["GET"])
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("posts/detail_post.html", post=post)

# --------------------- UPDATE ---------------------
@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    # поле дати має різну назву → заповнюємо вручну
    form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Post updated successfully!", "info")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("posts/add_post.html", form=form, edit=True)

# --------------------- DELETE ---------------------
@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "warning")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/delete_confirm.html", post=post)
