from flask import Blueprint, render_template, redirect, url_for
from app.models.post import Post
import app.task.tasks as tasks
from app.models.tag import Tag
import random
from flask import current_app

bp_public = Blueprint('public', __name__)


@bp_public.route('/')
def page_welcome():
    randomnum = int(random.random() * current_app.config['PICTURENUM']) + 1
    return render_template('welcome.html', randomnum=randomnum)


@bp_public.route('/home')
def page_home():
    randomnum = []
    for x in range(1,6):
        randomnum.append(int(random.random() * current_app.config['PICTURENUM']) + 1)
    posts = Post.fivelatestpost()
    return render_template('post.html', posts=posts, randomnum=randomnum)


@bp_public.route('/archive')
def page_archive_default():
    return redirect(url_for('public.page_archive', page=1))


@bp_public.route('/archive/<int:page>')
def page_archive(page):
    posts = Post.query.filter_by(published=True).order_by(Post.time.desc()).paginate(page, per_page=2, error_out=False)
    return render_template('archive.html', posts=posts)


@bp_public.route('/post/<string:title>')
def page_read_more(title):
    return render_template('read_more.html', post=Post.getpostbytitle(title))


@bp_public.route('/tags')
def page_tags():
    tags = Tag.allpublishedtag()
    return render_template('tags.html', tags=tags)


@bp_public.route('/project')
def page_project():
    datas = tasks.getgithubinfo()
    return render_template('project.html', datas=datas)


@bp_public.route('/gallery')
def page_gallery():
    return 'Hello'