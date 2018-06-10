#!/usr/local/bin/python
# coding: latin-1
import os, sys
import sqlite3

from flask import Flask, jsonify, abort, make_response, request, redirect, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal, request
from werkzeug.utils import secure_filename
#from flask_httpauth import HTTPBasicAuth
#from mysql.connector import (connection)

app = Flask(__name__, static_url_path="")
api = Api(app)

UPLOAD_FOLDER = os.path.basename('uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False

conn = sqlite3.connect('banco.db', check_same_thread=False)

def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        parser.add_argument('voltage')
        parser.add_argument('power_in_use')
        parser.add_argument('power_in_standby')
        args = parser.parse_args()

        file = request.files['photo']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photoPath = app.config['UPLOAD_FOLDER']+'/'+filename
            file.save(f)
        else:
            return "Formato da foto incorreto ou arquivo inexistente",400

        cursor = conn.cursor()
        a_name = args['name']
        a_description = args['description']
        a_photo_url = photoPath
        a_voltage = args['voltage']
        a_power_in_use = int(args['power_in_use'])
        a_power_in_standby = int(args['power_in_standby'])
        cursor.execute("INSERT INTO appliances (name, description, photo_url, voltage, power_in_use, power_in_standby) VALUES (?,?,?,?,?,?)", (a_name, a_description, a_photo_url, a_voltage, a_power_in_use, a_power_in_standby))
        conn.commit()
        return args, 201


class Appliance(Resource):
    def get(self, id):
        query = conn.execute("select * FROM appliances WHERE id="+str(id)+";")
        if query != None:
            return 'Aparelho doméstico não encontrado', 404
        else:
            return jsonify({'appliance': query.fetchall()})
    
#função de verificação de login
class Users(Resource):
    def get(self,user,senha):
        
        query=conn.execute("select mail,password FROM users where mail='"+user+"' AND password ='"+senha+"';");
        #coloquei aspas simples na query antes dos valores, sqlite não le como string
        if query != None :
            
            return 'Usuário ou senha incorretos! Já possui cadastro no sistema?',404
        else:
            return jsonify({'messagem':'login informado correto','codigo':200})

api.add_resource(Appliances, "/api-dad/appliances")
api.add_resource(Appliance, "/api-dad/appliances/<int:id>")
api.add_resource(Users, "/api-dad/users/login/<user>/<senha>")

app.run(debug=True)
conn.close()