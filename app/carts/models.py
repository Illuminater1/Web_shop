from app.db import db


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship("User", back_populates="cart")
    product = db.relationship("Product", back_populates="carts")

    def __repr__(self):
        return f"<Cart(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"
