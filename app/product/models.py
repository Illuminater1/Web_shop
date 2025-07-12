from app.models import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    stocks = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    category = db.relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product id: {self.id}, name: {self.name}>"