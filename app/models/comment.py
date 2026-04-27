from datetime import datetime
from app.models import db
import logging

class Comment(db.Model):
    """留言資料表"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, recipe_id, content):
        """新增一筆記錄"""
        try:
            comment = cls(user_id=user_id, recipe_id=recipe_id, content=content)
            db.session.add(comment)
            db.session.commit()
            return comment
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating comment: {e}")
            raise

    @classmethod
    def get_by_id(cls, comment_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(comment_id)
        except Exception as e:
            logging.error(f"Error fetching comment by id {comment_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error fetching all comments: {e}")
            return []

    def update(self, content):
        """更新記錄"""
        try:
            self.content = content
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating comment {self.id}: {e}")
            return False

    def delete(self):
        """刪除記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting comment {self.id}: {e}")
            return False
