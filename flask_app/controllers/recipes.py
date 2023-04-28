from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.recipe import Recipe
from flask_app.models.ingredient import Ingredient
from pprint import pprint



#GET ALL
@app.route('/mycookbook')
def get_all_recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    recipes = Recipe.get_all_recipes(session['user_id'])
    return render_template('dashboard.html', recipes = recipes)

#SEARCH PAGE
@app.route('/search')
def load_search():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('search.html')

#Main test dashboard
@app.route('/testkitchen')
def test_board():
    if 'user_id' not in session:
        return redirect('/logout')
    recipes = Recipe.get_test_recipes(session['user_id'])
    return render_template('test_board.html', recipes = recipes)

######### NEW 4-28 ##############
#GET ALL VERSIONS OF ONE RECIPE 
@app.route('/testkitchen/<int:id>')
def test_versions(id):
    if 'user_id' not in session:
        return redirect('/logout')
    recipes = Recipe.get_test_versions(id)
    return render_template('version_board.html', recipes = recipes)
##################################

#NEW - render form
@app.route('/mycookbook/new-recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/mycookbook')
    return render_template('new.html')

#NEW - process the form and redirect
@app.route('/create', methods=['POST'])
def create_recipe():

    # if not Recipe.validate_recipe(request.form):
    #     return redirect('/mycookbook/new-recipe')
    pprint(request.form)
    recipe=Recipe.save(request.form)
    pprint(request.form.getlist('ingredients'))
    for ingredient in request.form.getlist('ingredients'):
        print(ingredient)
        if ingredient != '':
            Ingredient.save_ingredient(recipe_id=recipe,text=ingredient)
    return redirect('/mycookbook') #redirect to show page for this recipe

#NEW VERSION OF RECIPE- render form
@app.route('/testkitchen/new/<int:id>')
def new_version():
    if 'user_id' not in session:
        return redirect('/mycookbook')
    return render_template('new.html')

#NEW VERSION OF RECIPE- process the form and redirect
@app.route('/new/<int:id>', methods=['POST'])
def create_version():
    # if not Recipe.validate_recipe(request.form):
    #     return redirect('/mycookbook/new-recipe')
    pprint(request.form)
    recipe=Recipe.save(request.form)
    pprint(request.form.getlist('ingredients'))
    for ingredient in request.form.getlist('ingredients'):
        print(ingredient)
        Ingredient.save_ingredient(recipe_id=recipe,text=ingredient)
    return redirect('/mycookbook') #redirect to show page for this recipe

#SHOW ONE RECIPE
@app.route('/recipe/<int:id>')
def show_recipe(id):
    return render_template("show.html",recipe=Recipe.get_recipe(id))

#SHOW ONE RECIPE FROM MY COOKBOOK
@app.route('/mycookbook/recipe/<int:id>')
def show_my_recipe(id):
    return render_template("show_mine.html",recipe=Recipe.get_recipe(id))

#SEND RECIPE TO TEST KITCHEN
@app.route('/testkitchen/send/<int:id>')
def send_recipe(id):
    Recipe.send_to_test(id)
    return redirect(f'/testkitchen/recipe/{id}')

@app.route('/testkitchen/recipe/<int:id>')
def show_test_recipe(id):
    return render_template("show_test.html",recipe=Recipe.get_recipe(id))

#UPDATE - This route renders the form
@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/mycookbook')
    recipe = Recipe.get_recipe(id)
    if session['user_id'] != recipe.user_id:
        return redirect('/mycookbook')
    return render_template('edit.html', recipe=recipe)

#UPDATE - Processing
@app.route('/recipes/update/<int:id>',methods=['POST'])
def update(id):
    pprint(request.form)
    # if not Recipe.validate_recipe(request.form):
    #     return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.update(request.form)
    ids=request.form.getlist('ingredient-id')
    vals=request.form.getlist('ingredients')
    print(ids)
    print(vals)
    for i in range (len(ids)):
        data={'id':ids[i],'text':vals[i]}
        Ingredient.update_ingredients(data)
    return redirect(f"/mycookbook/recipe/{id}")

#DELETE
@app.route('/delete-recipe/<int:id>')
def delete(id):
    recipe = Recipe.get_recipe(id)
    if session['user_id'] != recipe.user_id:
        return redirect('/recipes')
    if 'user_id' not in session:
        return redirect('/logout')
    Recipe.delete(id)
    return redirect('/recipes')


# #A redirect with reference to an id gotten from the page
# @app.route("/recipes/<int:id>", methods=['POST'])
# def show_recipe(id):
#     Recipe.get_recipe(id)
#     return redirect(f"/somewhere/{'id'}")
