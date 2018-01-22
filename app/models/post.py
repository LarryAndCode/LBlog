from app.extensions.db import db
import datetime

posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.post_id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id')),
                      )


class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=True, unique=True)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.String(2014), nullable=True)
    published = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=posts_tags)


    @classmethod
    def allpublishedtpost(cls):
        return Post.query.filter_by(published=True).order_by(Post.time.desc()).all()

    @classmethod
    def fivelatestpost(cls):
        return Post.query.filter_by(published=True).order_by(Post.time.desc()).limit(5)

    @classmethod
    def unallpublishedtpost(cls):
        return Post.query.filter_by(published=False).order_by(Post.time.desc()).all()

    @classmethod
    def getalltags(cls):
        return Post.query.get().all()

    @classmethod
    def getpostbytitle(cls, title):
        return Post.query.filter_by(title=title).first()

    @classmethod
    def deletepost(cls, id):
        Post.query.filter_by(post_id=id).delete()
        db.session.commit()

    @classmethod
    def editpost(cls, id):
        post = Post.query.filter_by(post_id=id).first()
        return post

    def save(self):
        db.session.add(self)
        db.session.commit()


