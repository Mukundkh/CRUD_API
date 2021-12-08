from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_restful import Api, Resource
#app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#set db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialization of database
db = SQLAlchemy(app)

#initialize marshmallow
marsh_mallow = Marshmallow(app)

#Creation of model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)


    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

#Schema of Item
class ItemSchema(marsh_mallow.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')

#initialize the schema
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

#create an item
@app.route('/item', methods=['POST'])
def add_item():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_item = Item(name, description, price, quantity)

    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item)
    

#get all item from db
@app.route('/item', methods=['GET'])
def get_items():
    all_items = Item.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result.data)


#get specific item 
@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    return item_schema.jsonify(item)

#Item updation
@app.route('/item/<id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get(id)
     
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    item.name = name
    item.description = description
    item.price = price
    item.quantity = quantity

    db.session.commit()

    return item_schema.jsonify(item)

#delete item
@app.route('/item/<id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


#run the server
if __name__ == '__main__':
    app.run(debug=True)
    