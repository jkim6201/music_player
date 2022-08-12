from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Music:
    db = "music_schema"
    def __init__(self,data):
        self.id = data['id']
        self.track = data['track']
        self.artist = data['artist']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM musics JOIN users ON musics.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        musics = []
        for row in results:
            music = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at'],
            }
            user = User(user_data)
            music.user = user
            musics.append(music)
        return musics


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM musics JOIN users ON musics.user_id=users.id WHERE musics.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False  
        row = results[0]
        music = cls(row)
        user_data = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        user = User(user_data)
        music.user = user
        return music
    

    # @classmethod
    # def create(cls, data):
    #     query = "INSERT INTO musics(track,artist,user_id) VALUES(%(track)s, %(artist)s,%(user_id)s);"
    #     return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def create(cls, data):
        query = "INSERT INTO musics(track,user_id) VALUES(%(track_id)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE musics SET track=%(track)s, artist=%(artist)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM musics WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_music_by_user(cls,data):
        query="SELECT * FROM musics WHERE user_id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        musics = []
        for row in results:
            music = cls(row)
            musics.append(music)
        return musics
