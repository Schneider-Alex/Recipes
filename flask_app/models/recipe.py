from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app)

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty= data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @staticmethod
    def validate_recipe(form):
        is_valid = True
        query = """SELECT * FROM recipes WHERE name =  %(name)s"""
        data= {
            'name':form['name']
        }
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if results:
            flash("recipe name exists!")
            is_valid = False
        if len(form['name']) < 3:
            flash("Recipe Name must be 3 Characters!")
            is_valid = False
        if len(form['instructions']) <  3:
            flash("Instructions must be 3 Characters!")
            is_valid = False
        if len(form['description']) <  3:
            flash("Description must be 3 Characters!")
            is_valid = False
        return is_valid
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        if len(results)<1:
            return recipes
        else:
            for recipe in results:
                recipes.append( cls(recipe)) 
            return recipes
        
    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes where id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])

    # @classmethod
    # def get_all_messages_from_creator(cls, data):
    #     # Get all tweets, and their one associated User that created it
    #     query = "SELECT * FROM users JOIN messages ON messages.user_id = users.id WHERE users.id = '%(id)s' ;"
    #     results = connectToMySQL('private_wall').query_db(query,data)
    #     # user = cls(results[0])
    #     all_messages_from_user = []
    #     for row in results:
    #         # Create a Tweet class instance from the information from each db row
    #         one_message = cls(row)
    #         # Prepare to make a User class instance, looking at the class in models/user.py
    #         one_messages_creator_info = {
    #             # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
    #             "id": row['id'], 
    #             "first_name": row['last_name'],
    #             "last_name": row['last_name'],
    #             "email": row['email'],
    #             "password": row['password'],
    #             "created_at": row['created_at'],
    #             "updated_at": row['updated_at']
    #         }
    #         # Create the User class instance that's in the user.py model file
    #         creator = user.User(one_messages_creator_info)
    #         # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
    #         one_message.creator = creator
    #         # Append the Tweet containing the associated User to your list of tweets
    #         all_messages_from_user.append(one_message)
    #     return all_messages_from_user
    @classmethod
    def delete_recipe(cls, data):
        query="""DELETE FROM recipes WHERE recipes.id = %(id)s"""
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def save_new_recipe(cls,data):
        query = """INSERT INTO recipes (name, description, instructions, under_thirty, created_at, updated_at, users_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, NOW(), NOW(), %(users_id)s);"""
        return connectToMySQL('recipes_schema').query_db( query, data )
    
    @classmethod
    def update_recipe(cls,data):
        query = """UPDATE recipes
SET name = %(name)s, description = %(description)s, instructions=%(instructions)s , under_thirty=%(under_thirty)s
WHERE id=%(id)s;"""
        return connectToMySQL('recipes_schema').query_db( query, data )
