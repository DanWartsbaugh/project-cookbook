from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.recipe import Recipe
from flask_app.models.ingredient import Ingredient
from pprint import pprint
import requests



#GET ALL
@app.route('/mycookbook')
def get_all_recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    recipes = Recipe.get_all_recipes(session['user_id'])
    return render_template('dashboard.html', recipes = recipes)

#SEARCH PAGE
@app.route('/search/<letter>')
def load_search(letter):
    if 'user_id' not in session:
        return redirect('/logout')
    data = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}").json()
    pprint(data)
    return render_template('search.html', data=data)

@app.route('/search/<int:id>')
def load_id(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}").json()
    pprint(data)

        #create a variable array for ingredients for us to append to
    ingredients = []

    #this loops over our data dictionary 
    for meal in data['meals']:
        
        #this checks each ingredient, there are 20 possible slots so we need to check each one for an ingredient
        for i in range(1, 21):
            #embedded expression to evaluate dynamic number since i will be changing.
            ingredient_key = f'strIngredient{i}'
            measure_key = f'strMeasure{i}'

            #the loop is checking each key manually, starting at 1 by putting in a literal string
            if ingredient_key in meal:
                ingredient = meal[ingredient_key]
                measure = meal[measure_key]

                #I needed this because otherwise it displays empty numbers in my list
                if measure:
                    ingredient_str = f"{ingredient}: {measure}"
                    ingredients.append(ingredient_str)
                else:
                    ingredients.append(ingredient)
    return render_template('show_api.html', data=data, ingredients=ingredients)

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
    session['versions']=[]
    session['vers'] = 0
    for i in recipes:
        session['versions'].append({'version':session['vers']+1,'id':i.id})
        session['vers']+=1
        print(session['versions'])
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
    print('recipe=',recipe)
    pprint(request.form.getlist('ingredients'))
    for ingredient in request.form.getlist('ingredients'):
        print(ingredient)
        if ingredient != '':
            Ingredient.save_ingredient(recipe_id=recipe,text=ingredient)
    if session['test']==0:
        return redirect('/mycookbook/recipe/{recipe}') #redirect to show page for this recipe
    if session['test']==1:
        return redirect(f"/testkitchen/recipe/{recipe}")

@app.route('/random')
def load_random():
    if 'user_id' not in session:
        return redirect('/logout')
    
    #this is our api request
    data = requests.get("https://www.themealdb.com/api/json/v1/1/random.php").json()
    pprint(data)

    #create a variable array for ingredients for us to append to
    ingredients = []

    #this loops over our data dictionary 
    for meal in data['meals']:
        
        #this checks each ingredient, there are 20 possible slots so we need to check each one for an ingredient
        for i in range(1, 21):
            #embedded expression to evaluate dynamic number since i will be changing.
            ingredient_key = f'strIngredient{i}'
            measure_key = f'strMeasure{i}'

            #the loop is checking each key manually, starting at 1 by putting in a literal string
            if ingredient_key in meal:
                ingredient = meal[ingredient_key]
                measure = meal[measure_key]

                #I needed this because otherwise it displays empty numbers in my list
                if measure:
                    ingredient_str = f"{ingredient}: {measure}"
                    ingredients.append(ingredient_str)
                else:
                    ingredients.append(ingredient)

    return render_template('show_api.html', data=data, ingredients=ingredients)

#NEW VERSION OF RECIPE- render form
@app.route('/testkitchen/new/<int:id>')
def new_version(id):
    if 'user_id' not in session:
        return redirect('/mycookbook')
    recipe = Recipe.get_recipe(id)
    session['ing_ids']=[]
    session['test']=recipe.test
    print("session test =",session['test'])
    for ingredient in recipe.ingredients:
        session["ing_ids"].append(str(ingredient.id))
    # print(session["ing_ids"])
    if session['user_id'] != recipe.user_id:
        return redirect('/testkitchen')
    return render_template('new-version.html',recipe=recipe)

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
    recipe=Recipe.get_recipe(id)
    original = Recipe.get_recipe(recipe.original)
    session['original_id']=original.id
    session['original']=[]
    for ingredient in original.ingredients:
        session['original'].append(ingredient.text)
    return render_template("show_test.html",recipe=recipe)

#UPDATE - This route renders the form
@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/mycookbook')
    recipe = Recipe.get_recipe(id)
    session['ing_ids']=[]
    session['test']=recipe.test
    print("session test =",session['test'])
    for ingredient in recipe.ingredients:
        session["ing_ids"].append(str(ingredient.id))
    # print(session["ing_ids"])
    if session['user_id'] != recipe.user_id:
        return redirect('/mycookbook')
    return render_template('edit.html', recipe=recipe)

#UPDATE - Processing
@app.route('/recipes/update/<int:id>',methods=['POST'])
def update(id):
    # pprint(request.form)
    # if not Recipe.validate_recipe(request.form):
    #     return redirect(f"/recipes/edit/{request.form['id']}")
    recipe = Recipe.update(request.form)
    ids=request.form.getlist('ingredient-id')
    vals=request.form.getlist('ingredients')
    # print(ids)
    # print(vals)
    for i in session["ing_ids"]:
        if i not in ids:
            Ingredient.deleteIngredient(i)
    for i in range (len(vals)):
        data={'id':ids[i],'text':vals[i]}
        if ids[i]=='0':
            Ingredient.save_ingredient(recipe_id=id,text=vals[i])
        else:
            Ingredient.update_ingredients(data)
    if session['test']==0:
        return redirect(f"/mycookbook/recipe/{id}")
    if session['test']==1:
        return redirect(f"/testkitchen/recipe/{id}")

#DELETE
@app.route('/delete-recipe/<int:id>')
def delete(id):
    recipe = Recipe.get_recipe(id)
    if session['user_id'] != recipe.user_id:
        return redirect('/recipes')
    if 'user_id' not in session:
        return redirect('/logout')
    Ingredient.deletewithrecipe(id)
    Recipe.delete(id)
    return redirect('/mycookbook')


# #A redirect with reference to an id gotten from the page
# @app.route("/recipes/<int:id>", methods=['POST'])
# def show_recipe(id):
#     Recipe.get_recipe(id)
#     return redirect(f"/somewhere/{'id'}")