from datetime import datetime
from app.models import db
import logging

class User(db.Model):
    """使用者資料表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    recipes = db.relationship('Recipe', backref='author', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete-orphan")
    collections = db.relationship('Collection', backref='user', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, username, email, password_hash):
        """新增一筆記錄"""
        try:
            user = cls(username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating user: {e}")
            raise

    @classmethod
    def get_by_id(cls, user_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            logging.error(f"Error fetching user by id {user_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error fetching all users: {e}")
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
            logging.error(f"Error updating user {self.id}: {e}")
            return False

    def delete(self):
        """刪除記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting user {self.id}: {e}")
            return False
