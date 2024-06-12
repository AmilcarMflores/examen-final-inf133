
        
from database import db

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    description = db.Column(String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self,name,address,city,phone,description,rating):
        self.name=name
        self.address=address
        self.city=city
        self.phone=phone
        self.description=description
        self.rating=rating


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return db.session.query.all()

    @staticmethod
    def get_by_id(id):
        return db.session.query.get(id)


    def update(self,name=name,address=address,city=city,phone=phone,description=description,rating=rating):
        if name is not None:
            self.name=name
        if address is not None:
            self.address=address
        if city is not None:
            self.city=city
        if phone is not None:
            self.phone=phone
        if description is not None:
            self.description=description
        if rating is not None:
            self.rating=rating
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        