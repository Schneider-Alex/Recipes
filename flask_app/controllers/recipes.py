from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, recipe
from flask import flash


@app.route('/createrecipe',methods=['GET'])
def trasnfer_to_recipe_page():
    if session:
        return render_template('newrecipepage.html')
    else:
        return redirect('/')


@app.route('/recipes/new',methods=['POST'])
def newrecipe():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/createrecipe')
    else:
        data={
            'name':request.form['name'],
            'description':request.form['description'],
            'instructions':request.form['instructions'],
            'under_thirty':request.form['under_thirty'],
            'users_id':session['id'],
        }
        recipe.Recipe.save_new_recipe(data)
    
    
    return redirect('/dashboard')

@app.route('/recipe/delete/<recipeid>')
def deleterecipe(recipeid):
    data = {
        'id' : recipeid
    }
    recipe.Recipe.delete_recipe(data)
    return redirect ('/dashboard')

@app.route('/recipe/<int:recipeid>')
def show_recipe(recipeid):
    data = {
        'id':  recipeid
    }
    this_recipe=recipe.Recipe.get_one_recipe(data)
    log_in_data={
                'id' : session['id']
            }
    if this_recipe:
        creator_data={
            'id' : this_recipe.users_id
        }
        return render_template('recipe_page.html',this_recipe=this_recipe, creator=user.User.get_one(creator_data),user=user.User.get_one(log_in_data))
    else:
        return redirect('/dashboard')

@app.route('/recipe/edit/<int:recipeid>')
def edit_recipe_page(recipeid):
    data = {
        'id':  recipeid
    }
    this_recipe=recipe.Recipe.get_one_recipe(data)
    return render_template("edit_recipe_page.html", this_recipe=this_recipe)

@app.route('/editrecipe', methods=["POST"])
def edit_recipe():
    data= {
        'id' : request.form['id'],
        'name' : request.form['name'],
        'instructions' : request.form['instructions'],
        'description' : request.form['description'],
        'under_thirty' : request.form['under_thirty'],
    }
    recipe.Recipe.update_recipe(data)
    return redirect ('/dashboard')


