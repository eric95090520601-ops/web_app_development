from datetime import datetime
from app.models import db
import logging

class Collection(db.Model):
    """收藏資料表"""
    __tablename__ = 'collections'
    __table_args__ = (db.UniqueConstraint('user_id', 'recipe_id', name='_user_recipe_uc'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, recipe_id):
        """新增一筆記錄（如已收藏則直接返回）"""
        try:
            existing = cls.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
            if existing:
                return existing
            collection = cls(user_id=user_id, recipe_id=recipe_id)
            db.session.add(collection)
            db.session.commit()
            return collection
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating collection: {e}")
            raise

    @classmethod
    def get_by_id(cls, collection_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(collection_id)
        except Exception as e:
            logging.error(f"Error fetching collection by id {collection_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error fetching all collections: {e}")
            return []

    def delete(self):
        """刪除記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting collection {self.id}: {e}")
            return False
