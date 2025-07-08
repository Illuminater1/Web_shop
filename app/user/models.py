from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), default='user')
    orders = db.relationship('Order', backref="user")

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
    status = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False, index=True)
    product = db.relationship('Product', back_populates='orders')

    def __repr__(self):
        return f"<Оrder {self.id} - amount: {self.amount}>"