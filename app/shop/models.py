from app.db import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)

    products = db.relationship('Product', backref='category')

    def __repr__(self):
        return f"<Category id: {self.id}, name: {self.name}>"


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    stocks = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    carts = db.relationship('Cart', back_populates='product')
    ordered_products = db.relationship('OrderedProduct', back_populates='product')

    def __repr__(self):
        return f"<Product id: {self.id}, name: {self.name}>"


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

