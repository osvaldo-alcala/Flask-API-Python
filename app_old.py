import pip
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from security import authenticate, identity

try:
    from flask_jwt import JWT, jwt_required
except:
    pip.main(['install', 'flask_jwt'])

app = Flask(__name__)
app.secret_key = 'osvaldo'  ## got to be somehitng really difficult to guess
api = Api(app)
jwt = JWT(app, authenticate, identity)  # auto generate endpooint (/auth) create a tocken
items = []  # dict for each item lils
'''
@app.route('/')
def home():
    return 'hello World'
'''


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    data = parser.parse_args()


    @jwt_required()  # decorator to have auth user before we can use this method
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):  # /item/<name>
        # iterate over our items list to see if the item exis
        for item in items:
            if item['name'] == name:
                return {'message': "Bad request, item already exist!"}, 400
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = {'name': name,
                'price': data['price']
                }
        items.append(item)
        return item, 201  # created
        # return {'item': None}, 404

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:  # if item does not exist them create the item
            item = {'name': name,
                    'price': data['price']
                    }
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.0:5000/item/pencil
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)
