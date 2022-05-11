from app import app
from flask import request
import json


with open('app/data.json') as file:
    data = json.load(file)


def recipe_exists(recipe_name):
    for recipe in data["recipes"]:
        if recipe["name"] == recipe_name:
            return True
    return False


@app.route('/recipes')
def get_recipes():
    recipe_names = [recipe["name"] for recipe in data["recipes"]]
    return {'recipes': recipe_names}, 200


@app.route('/recipes/details/<string:recipe_name>')
def get_recipe_details(recipe_name):
    for recipe in data["recipes"]:
        if recipe["name"] == recipe_name:
            return {
                "details": {
                    "ingredients": recipe["ingredients"],
                    "numSteps": len(recipe["instructions"])
                }
            }, 200
    return {}, 200


@app.route('/recipes', methods=["POST"])
def add_new_recipe():
    input_recipe = request.get_json()

    if recipe_exists(input_recipe["name"]):
        return {'error': "Recipe already exists"}, 400
    else:
        data["recipes"].append(input_recipe)
        output_data = json.dumps(data, indent=4)
        with open('app/data.json', 'w') as outfile:
            outfile.write(output_data)
        return '', 201


@app.route('/recipes', methods=["PUT"])
def update_recipe():
    input_recipe = request.get_json()

    exists = recipe_exists(input_recipe["name"])

    if exists:
        for i in range(len(data["recipes"])):
            if data["recipes"][i]["name"] == input_recipe["name"]:
                data["recipes"][i] = input_recipe
        output_data = json.dumps(data, indent=4)
        with open('app/data.json', 'w') as outfile:
            outfile.write(output_data)
        return '', 204
    return {'error': "Recipe does not exist"}, 404
