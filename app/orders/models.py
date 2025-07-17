from datetime import datetime

from app.db import db


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



class OrderedProduct(db.Model):
    __tablename__ = 'ordered_products'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    order = db.relationship("Order", back_populates="ordered_products")
    product = db.relationship("Product", back_populates="ordered_products")

    def __repr__(self):
        return f"<OrderedProduct(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"