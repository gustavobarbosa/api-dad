#!/usr/local/bin/python
# coding: latin-1
import os, sys
import sqlite3

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal, request
#from flask_httpauth import HTTPBasicAuth
#from mysql.connector import (connection)


app = Flask(__name__, static_url_path="")
api = Api(app)

conn = sqlite3.connect('banco.db', check_same_thread=False)
'''
auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == 'lincoln':
        return 'python'
    return None

@auth.error_handler
def unathorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unathorized access'}), 403)




users = [
    {
        "id": 1,
        "name": "Lincoln",
        "cpf": "075.755.222-91",
        "mail": "lincoln@pucminas.br",
        "password": "dasdas",
        "address": "Rua Walter Ianni, 55, São Gabriel, Belo Horizonte",
        "birth_date": "2018-05-15"
    }
]
'''


class Appliances(Resource):
    def get(self):
        query = conn.execute("select * FROM appliances;")
        result = query.fetchall()
        query.close()
        return jsonify({'appliances': result})

    def post(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('description')
        parser.add_argument('photo_url')
        parser.add_argument('voltage')
        parser.add_argument('power_in_use')
        parser.add_argument('power_in_standby')
        args = parser.parse_args()

        cursor = conn.cursor()
        a_name = args['name']
        a_description = args['description']
        a_photo_url = args['photo_url']
        a_voltage = args['voltage']
        a_power_in_use = int(args['power_in_use'])
        a_power_in_standby = int(args['power_in_standby'])
        cursor.execute("INSERT INTO appliances (name, description, photo_url, voltage, power_in_use, power_in_standby) VALUES (?,?,?,?,?,?)", (a_name, a_description, a_photo_url, a_voltage, a_power_in_use, a_power_in_standby))
        conn.commit()
        return args, 201


class Appliance(Resource):
    def get(self, id):
        query = conn.execute("select * FROM appliances WHERE id="+str(id)+";")
        if query is None:
            return 'Aparelho doméstico não encontrado', 404
        else:
            return jsonify({'appliance': query.fetchall()})
    
    '''
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument(occupation)
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] =  args["occupation"]
                return user, 200 #ok
            
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }

        users.append(user)
        return user, 201 #Criado 

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
   '''

api.add_resource(Appliance, "/api-dad/appliances/<int:id>")
api.add_resource(Appliances, "/api-dad/appliances")

app.run(debug=True)
conn.close()