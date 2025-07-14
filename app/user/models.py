from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app.db import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String())
    role = db.Column(db.String(10), default='user')

    cart = db.relationship("Cart", back_populates="user")
    orders = db.relationship("Order", back_populates="user")

    @property
    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User id: {self.id} - name: {self.email}>"


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(200))
    status = db.Column(db.String)

    user = db.relationship("User", back_populates="orders")
    ordered_products = db.relationship("OrderedProduct", back_populates="order")

    def __repr__(self):
        return f"<Оrder - {self.id}, user: {self.user_id}>"