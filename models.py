import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = 'capstone'
database_path = 'postgresql://{}:{}@{}/{}'.format(os.getenv("database_user"),os.getenv("database_password"),os.getenv("DATABASE_URL"), database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
# helper function to add an actor to a movie and commit it to the database
def add_actor_to_movie(movie, actor):
    movie.actors.append(actor)
    db.session.add(movie)  # Add the modified movie object to the session
    db.session.commit()  # Commit the changes to the database

class actors_movies(db.Model):
    __tablename__ = 'actors_movies'

    id = Column(Integer, primary_key=True)
    actor_id = Column("actor_id",db.Integer, db.ForeignKey('Actor.id'))
    movie_id = Column("movie_id",db.Integer, db.ForeignKey('Movie.id'))

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = Column(db.DateTime)
    actors = db.relationship('Actor', secondary='actors_movies', lazy = True) 

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    gender = Column(db.String)
    movies = db.relationship('Movie', secondary='actors_movies', lazy = True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}
