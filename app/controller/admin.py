from flask import Blueprint, render_template, abort, request, redirect,flash,url_for
from flask_login import current_user
from app.models.post import Post
from app.models.tag import Tag
import app.task.tasks as tasks

bp_admin = Blueprint('admin', __name__, url_prefix='/admin')

@bp_admin.before_request
def login():
    if not current_user.is_authenticated:
        abort(403)

@bp_admin.route('/home', methods=['GET'])
def home():
    return render_template('blog/base.html')

@bp_admin.route('/tags', methods=['GET'])
def tags():
    tags = Tag.query.all()
    return render_template('blog/tags.html', tags=tags)

@bp_admin.route('/list', methods=['GET'])
def list():
    publishedtposts = Post.allpublishedtpost()
    return render_template('blog/list.html', publishedtposts=publishedtposts)


@bp_admin.route('/create', methods=['GET', 'POST'])
def create():
    return tasks.createpost(request)


@bp_admin.route('/draft', methods=['GET'])
def draft():
    unpublishedtposts = Post.unallpublishedtpost()
    return render_template('blog/draft.html', unpublishedtposts=unpublishedtposts)


@bp_admin.route('/logout', methods=['GET'])
def logout():
    return redirect('/logout')


@bp_admin.route('/deletepost/<int:postid>', methods=['GET'])
def deletepost(postid):
    Post.deletepost(postid)
    return redirect(url_for('admin.list'))


@bp_admin.route('/editpost/<int:postid>', methods=['GET'])
def editpost(postid):
    post = Post.editpost(postid)
    return render_template('blog/edit.html', post=post)


@bp_admin.route('/editpost/<int:postid>/update', methods=['POST'])
def updatepost(postid):
    return tasks.updatepost(request, postid=postid)


@bp_admin.route('/deletetag/<int:tagid>', methods=['GET'])
def deletetag(tagid):
    Tag.deletepost(tagid)
    return redirect(url_for('admin.tags'))

@bp_admin.route('/updatetag/<int:tagid>', methods=['GET','POST'])
def updatetag(tagid):
    if request.method == 'GET':
        tag = Tag.query.filter_by(tag_id=tagid).first()
        return render_template('blog/edittag.html',tag = tag)
    elif request.method == 'POST':
        Tag.updatetag(request, tagid)
        return redirect(url_for('admin.tags'))
    else:
        redirect('/')