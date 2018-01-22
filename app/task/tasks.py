import requests
import json
import functools
from flask_login import current_user
from flask import redirect, url_for, request, flash, render_template
from app.models.post import Post
from app.models.tag import Tag
from app.extensions.db import db
import os




def getgithubinfo():
    url = 'https://api.github.com/users/LarryAndCode/repos'
    resp = requests.get(url).text
    datas = json.loads(resp)
    return datas

def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            return fn(*args, **kwargs)
        return redirect(url_for('auth.login', next=request.path))
    return inner


def createpost(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.form.get('title')
        post.content = request.form.get('content')

        tag = Tag()
        tag.content = request.form.get('tags')

        post.tags.append(tag)

        if request.form.get('published') == 'True':
            post.published = True
        else:
            post.published = False

        if not (post.title and post.content and post.tags):
            flash('Please complete the form.', 'danger')
            return redirect(request.url)
        else:
            post.save()
            return redirect('/admin/home')
    elif request.method == 'GET':
        return render_template('blog/create.html')


def updatepost(request, postid):

    title = request.form.get('title')
    content = request.form.get('content')

    if request.form.get('published') == 'True':
        published = True
    else:
        published = False

    if not (title and content):
        flash('Please complete the form.', 'danger')
        return redirect(request.url)

    Post.query.filter_by(post_id=postid).update({
        "title": title,
        "content": content,
        "published": published
    })

    tags = Tag.query.filter(Tag.posts.any(Post.post_id == postid)).all()

    if not tags:
        newtag = Tag(content=request.form.get('newtag'))
        post = Post.query.filter_by(post_id=postid).first()
        post.tags.append(newtag)
        newtag.save()
    else:
        for tag in tags:
            taglabel = 'tagid_' + str(tag.tag_id)
            tag_content = request.form.get(taglabel)
            Tag.query.filter_by(tag_id=tag.tag_id).update({"content":tag_content})

    db.session.commit()

    return redirect('/admin/home')


def randonpicture(path):
    length = len(os.listdir(path))
    return length