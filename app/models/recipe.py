from datetime import datetime
from app.models import db
import logging

class Recipe(db.Model):
    """食譜資料表"""
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
        """新增一筆記錄"""
        try:
            recipe = cls(user_id=user_id, title=title, ingredients=ingredients, steps=steps, description=description)
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating recipe: {e}")
            raise

    @classmethod
    def get_by_id(cls, recipe_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            logging.error(f"Error fetching recipe by id {recipe_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            logging.error(f"Error fetching all recipes: {e}")
            return []

    def update(self, **kwargs):
        """更新記錄"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating recipe {self.id}: {e}")
            return False

    def delete(self):
        """刪除記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting recipe {self.id}: {e}")
            return False
