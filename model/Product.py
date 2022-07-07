from cmath import e

from config import app_active, app_config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from model.Category import Category
from model.User import User

config = app_config[app_active]
db = SQLAlchemy(config.APP)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    quantity = db.Column(db.Integer, nullable=True, default=0)
    image = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(),
                             nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(),
                            nullable=False)
    status = db.Column(db.Boolean(), default=1, nullable=True)
    user_created = db.Column(
        db.Integer, db.ForeignKey(User.id), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey(
        Category.id), nullable=False)
    user_relationship = relationship(User)
    category_relationship = relationship(Category)

    def get_all():
        try:
            res = db.session.query(Product).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        finally:
            db.session.close()

    def update(self, obj):
        try:
            db.session.query(Product).filter(
                Product.id == self.id).update(obj)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.roolback()
            return False
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.query(Product).filter(
                Product.id == self.id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.roolback()
            return False
        finally:
            db.session.close()
