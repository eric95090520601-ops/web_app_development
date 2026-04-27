from datetime import datetime
from app.models import db

class Collection(db.Model):
    __tablename__ = 'collections'
    __table_args__ = (db.UniqueConstraint('user_id', 'recipe_id', name='_user_recipe_uc'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, recipe_id):
        # 檢查是否已收藏
        existing = cls.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        if existing:
            return existing
        collection = cls(user_id=user_id, recipe_id=recipe_id)
        db.session.add(collection)
        db.session.commit()
        return collection

    @classmethod
    def get_by_id(cls, collection_id):
        return cls.query.get(collection_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
