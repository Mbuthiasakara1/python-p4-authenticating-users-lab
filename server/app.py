#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class IndexArticle(Resource):
    
    def get(self):
        articles = [article.to_dict() for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):

    def get(self, id):
      session['page_views']=session.get('page_views',0)

      session['page_views'] +=0
      if session['page_views'] <= 3:

            article = Article.query.filter(Article.id == id).first()
            article_json = jsonify(article.to_dict())

            return make_response(article_json, 200)

      return {'message': 'Maximum pageview limit reached'}, 401
api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')  


@app.route('/check_session',methods=['GET'])
def check_session():#makes suee the user is not logged out incase they refersh the webapp
    user_id =session.get('user_id')

    if user_id :
        user=User.query.get(user_id)
        if user:
            return make_response(user.to_dict(),200)
        
    return make_response('',401)



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.json.get("username")
        user=User.query.filter_by(username=username).first()

        if not username:
            return make_response({
                'message':"Username is required"
            },400)

        if user:
            session["user_id"]=user.id
            return make_response(user.to_dict(),200)
        return make_response({
            'message':'User not found'
        },404)
@app.route('/logout',methods=['DELETE']) 
def logout():
    session.pop("user_id",None) 
    return make_response('',204)


    


        





if __name__ == '__main__':
    app.run(port=5555, debug=True)
