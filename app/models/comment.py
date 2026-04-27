from datetime import datetime
from app.models import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, recipe_id, content):
        comment = cls(user_id=user_id, recipe_id=recipe_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return comment

    @classmethod
    def get_by_id(cls, comment_id):
        return cls.query.get(comment_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, content):
        self.content = content
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
