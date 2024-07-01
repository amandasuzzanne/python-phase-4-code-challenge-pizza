from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    #  relationship of M:M: Restaurant to Pizza through RestaurantPizza
    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', backref='restaurante', lazy=True)

    # Serialization rules to prevent recursion
    serialize_rules = ('-pizzas.restaurants',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    #  relationship of M:M: Pizza to Restaurant through RestaurantPizza
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', backref='pizza', lazy=True)

    # Serialization rules to prevent recursion
    serialize_rules = ('-restaurants.pizzas',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    #  foreign keys
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id", ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id", ondelete='CASCADE'))

    #  relationships with cascading delete
    pizza = db.relationship("Pizza", backref="restaurant_pizzas", cascade="all, delete")
    restaurant = db.relationship("Restaurant", backref="restaurant_pizzas", cascade="all, delete")

    def __repr__(self):
        return