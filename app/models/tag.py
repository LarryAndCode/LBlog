from app.extensions.db import db
from app.models.post import posts_tags, Post
import datetime


class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.String(2014), nullable=True, unique=True)
    posts = db.relationship('Post', secondary=posts_tags)

    @classmethod
    def allpublishedtag(cls):
        return Tag.query.filter(Tag.posts.any(Post.published==True)).all()

    @classmethod
    def deletepost(cls,tagid):
        Tag.query.filter_by(tag_id=tagid).delete()
        db.session.commit()

    @classmethod
    def updatetag(cls, request, tagid):
        content = request.form.get('content')
        Tag.query.filter_by(tag_id=tagid).update({"content":content})
        db.session.commit()


    def save(self):
        db.session.add(self)
        db.session.commit()
