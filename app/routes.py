from app import app
from flask import request
import json

with open('app/data.json') as file:
    data = json.load(file)


@app.route('/recipes')
def get_recipes():
    recipeNames = [recipe["name"] for recipe in data["recipes"]]
    return {
        'recipeNames': recipeNames
    }


@app.route('/recipes/details/<string:recipeName>')
def get_recipe_details(recipeName):
    this_recipe = {}
    for recipe in data["recipes"]:
        if recipe["name"] == recipeName:
            this_recipe = recipe
    try:
        return {
            "details": {
                "ingredients": this_recipe["ingredients"],
                "numSteps": len(this_recipe["instructions"])
            }
        }
    except:
        return {}

@app.route('/recipes', methods=["POST"])
def add_new_recipe():
    exists = False
    new_recipe = request.get_json()
    for recipe in data["recipes"]:
        if recipe["name"] == new_recipe["name"]:
            exists = True
    if exists:
        return {'error': "Recipe already exists"}
    if not exists:
        print(new_recipe)
        data["recipes"].append(new_recipe)
    return '' 
