import pip
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

try:
    from flask_jwt import JWT, jwt_required
except:
    pip.main(['install', 'flask_jwt'])

app = Flask(__name__)
app.secret_key = 'osvaldo'  ## got to be somehitng really difficult to guess
api = Api(app)

jwt = JWT(app, authenticate, identity)  # auto generate endpooint (/auth) create a tocken


'''
@app.route('/')
def home():
    return 'hello World'
'''


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.0:5000/item/pencil
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__=='__main__':
    app.run(port=5000, debug=True)
