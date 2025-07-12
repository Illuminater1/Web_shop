from app.models import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)

    products = db.relationship('Product', back_populates='categories')

    def __repr__(self):
        return f"<Category id: {self.id}, name: {self.name}>"





class OrderedProduct(db.Model):
    __tablename__ = 'ordered_products'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    order = db.relationship("Order", back_populates="ordered_products")
    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderedProduct(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"