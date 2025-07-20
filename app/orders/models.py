from datetime import datetime
from email.policy import default

from app.db import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        index=True,)
    created_time = db.Column(db.DateTime,
                           default=datetime.utcnow)

    phone_number = db.Column(db.Integer())

    delivery_method = db.Column(db.String(20),
                                default='delivery')

    payment = db.Column(db.String(20),
                        default='card')

    address = db.Column(db.String(200))

    status = db.Column(db.String,
                       default='В обработке')

    user = db.relationship("User",
                           back_populates="orders")

    ordered_products = db.relationship("OrderedProduct",
                                       back_populates="order")

    def __repr__(self):
        return f"<Оrder - {self.id}, user: {self.user_id}>"



class OrderedProduct(db.Model):

    __tablename__ = 'ordered_products'

    id = db.Column(db.Integer,
                   primary_key=True)

    order_id = db.Column(db.Integer,
                         db.ForeignKey('orders.id'),
                         nullable=False)

    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'),
                           nullable=False)

    name = db.Column(db.String(200))


    quantity = db.Column(db.Integer,
                         default=1)

    price = db.Column(db.Float())

    created_timestamp = db.Column(db.DateTime,
                           default=datetime.utcnow)

    order = db.relationship("Order",
                            back_populates="ordered_products")

    product = db.relationship("Product",
                              back_populates="ordered_products")

    def __repr__(self):
        return f"<OrderedProduct(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"