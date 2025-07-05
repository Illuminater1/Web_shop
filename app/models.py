from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    products = db.relationship('Product', backref='category', lazy='select')

    def __repr__(self):
        return f"<Category id: {self.id}>"


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


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    description = db.Column(db.Text)
    stocks = db.Column(db.Integer)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    images = db.relationship('Product_image', backref='product', lazy='select')
    orders = db.relationship('Order', back_populates='product')

    def __repr__(self):
        return f"<Product id: {self.id} - name: {self.name}>"


class Product_image(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), index=True)
    path_to_image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Product images in {self.path_to_image}>"


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    product = db.relationship('Product', back_populates='orders')


    def __repr__(self):
        return f"<Оrder {self.id} - amount: {self.amount}>"
