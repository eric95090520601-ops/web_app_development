from datetime import datetime
from app.models import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade="all, delete-orphan")
    collected_by = db.relationship('Collection', backref='recipe', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, user_id, title, ingredients, steps, description=None):
        recipe = cls(user_id=user_id, title=title, ingredients=ingredients, steps=steps, description=description)
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.get(recipe_id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
