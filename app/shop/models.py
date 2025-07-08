from app.models import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    products = db.relationship('Product', backref='category', lazy='select')

    def __repr__(self):
        return f"<Category id: {self.id}>"


class Product(db.Model):
    __tablename__ = 'shop'

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
    product_id = db.Column(db.Integer, db.ForeignKey('shop.id'), index=True)
    path_to_image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Product images in {self.path_to_image}>"
