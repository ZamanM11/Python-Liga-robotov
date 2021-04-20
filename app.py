# encoding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from marshmallow import fields
 
from marshmallow_jsonapi.flask import Schema
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from datetime import datetime
 
app = Flask(__name__)
 
database_location = os.getcwd()+'\\app.db'
 
a = os.getcwd()
b = app.root_path
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'secret_key'
 
admin = Admin(app, name='Администратор', template_mode='bootstrap3')
# Add administrative views here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_location
 
 
db = SQLAlchemy(app)
 
 
class Games(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type_game = db.Column(db.String)
    downloads = db.Column(db.Integer)
    released_day = db.Column(db.Date)
 
 
class GamesSchema(Schema):
    class Meta:
        type_ = 'игры'
        self_view = 'game_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'game_list'
 
    id = fields.Integer(as_string=True)
    type_game = fields.Str(required = True)
    downloads = fields.Integer(as_string=True)
    released_day = fields.Date()
 
class GamesList(ResourceList):
    schema = GamesSchema
    data_layer = {'session': db.session,
                  'model': Games}
 
class GamesDetail(ResourceDetail):
    schema = GamesSchema
    data_layer = {'session': db.session,
                  'model': Games}
 
 
api = Api(app)
api.route(GamesList, 'games_list', '/games')
api.route(GamesDetail, 'games_detail', '/games/<int:id>')
 
admin.add_view(ModelView(Games, db.session))
 
 
 
 
if __name__ == '__main__':
    app.run(debug=True) #fefef