from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data ['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []
    
    @staticmethod
    def validate_account( form ):
        is_valid = True
        query = """SELECT * FROM users WHERE email =  %(email)s"""
        results = connectToMySQL('recipes_schema').query_db(query, form)
        if len(results) >= 1:
            flash("email address already in use!")
            is_valid = False
        elif not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(form['first_name']) < 3:
            flash("First Name must be 3 Characters!")
            is_valid = False
        if len(form['last_name']) <  3:
            flash("Last Name must be 3 Characters!")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user)) 
        return users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users where id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def save(cls, dict):
        data = {
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'email' : dict['email'],
                'password' : bcrypt.generate_password_hash(dict['password'])
            }
        query = """INSERT INTO users (first_name, last_name, email, password, updated_at ) 
        VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s,  NOW());"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes_schema').query_db( query, data )
    
    @classmethod
    def loginuser(cls, form):
        query = """SELECT * FROM users WHERE email =  %(email)s"""
        results = connectToMySQL('recipes_schema').query_db(query, form)
        if len(results)<1:
            flash('User does not exist with this email!')
        else:
            return cls(results[0])