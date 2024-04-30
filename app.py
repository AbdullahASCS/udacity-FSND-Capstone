import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie,actors_movies, add_actor_to_movie
from auth.auth import requires_auth, AuthError
# trigger
def create_app(database_path= None):
  # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    if database_path:
        setup_db(app,database_path)
    else:
        setup_db(app)

    CORS(app)

    @app.route('/actors/<int:id>', methods = ["GET"]) 
    @requires_auth('get:actor')
    def get_actor(jwt,id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        movies = [movie.format() for movie in actor.movies]
        return jsonify({
            "success": True,
            "actor": actor.format(),
            'associated_movies': movies
        })
    @app.route('/movies/<int:id>', methods = ["GET"])
    @requires_auth('get:movie')
    def get_movie(jwt,id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        actors = [actor.format() for actor in movie.actors]
        return jsonify({
            "success": True,
            "movie": movie.format(),
            'associated_actors': actors
        })
    @app.route('/movies', methods = ["POST"])
    @requires_auth('post:movie')
    def post_movie(jwt):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        actors_id = body.get('actors_id') 
        movie = Movie(title, release_date)
        if actors_id is not None:
            for actorID in actors_id:
                actor = Actor.query.filter(Actor.id == actorID).one_or_none()
                if actor is None:
                    abort(404)
                movie.actors.append(actor)
            
        movie.insert()
        return jsonify({
            "success": True,
            "movie": movie.format()
        })
    @app.route('/movies/<int:id>', methods = ["PATCH"])
    @requires_auth('patch:movie')
    def patch_movie(jwt, id):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        actors_id = body.get('actors_id')
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        associations = actors_movies.query.filter_by(movie_id=id).all()
        for association in associations:
            association.delete()
        if actors_id is not None:
            for actorID in actors_id:
                actor = Actor.query.filter(Actor.id == actorID).one_or_none()
                if actor is None:
                    abort(404)
                if actor not in movie.actors:
                    add_actor_to_movie(movie, actor)
                    
        return jsonify({
            "success": True,
            "movie": movie.format(),
            "associated_actors": [actor.format() for actor in movie.actors]
        }) 
    @app.route('/movies/<int:id>', methods = ["DELETE"])
    @requires_auth('delete:movie')
    def delete_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            "success": True,
            "deleted": id
        })
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    
    
    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator each error handler should return (with approprate messages):
                 jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404
    
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'errorCode': '404',
            'message': 'The requested resource was not found'
        }), 404
    
    
    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'status': 'error',
            'errorCode': '400',
            'message': 'Bad request'
        }), 400
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': 'error',
            'errorCode': '500',
            'message': 'Internal server error'
        }), 500
    
    
    
    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app
   
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
