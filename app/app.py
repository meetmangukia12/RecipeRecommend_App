import requests
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import process
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models (Recipe, Ingredient, RecipeIngredient, Nutrition)
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    spoonacular_url = db.Column(db.String(255))
    nutrition = db.relationship('Nutrition', backref='recipe', uselist=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

class Nutrition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Fetch recipes based on ingredients from Spoonacular API
def fetch_recipes_based_on_user_input(ingredients, dietary_preferences, max_calories, batch_size=10):
    params = {
        "apiKey": "07b08237eccf4fb389abd8ccae6f24dc",  # API key 
        "number": batch_size,
        "ingredients": ','.join(ingredients),
        "diet": dietary_preferences,
        "maxCalories": max_calories,
    }
    
    response = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=params)
    if response.status_code == 200:
        recipes = response.json()
        detailed_recipes = []

        for recipe in recipes:
            recipe_id = recipe['id']
            detailed_recipe = get_recipe_information(recipe_id)
            detailed_recipes.append(detailed_recipe)
        return detailed_recipes
    else:
        return []

# Fetch detailed recipe info including sourceUrl
def get_recipe_information(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": "07b08237eccf4fb389abd8ccae6f24dc"}  # Your API key here
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        recipe_info = response.json()
        return {
            'name': recipe_info['title'],
            'image_url': recipe_info['image'],
            'spoonacular_url': recipe_info.get('sourceUrl', '')  # Use sourceUrl
        }
    else:
        return {}

# Store fetched recipes in the database
def store_recipe_data(recipes):
    for recipe_data in recipes:
        print(f"Storing recipe: {recipe_data['name']}")  # Debugging
        recipe = Recipe.query.filter_by(name=recipe_data['name']).first()
        if not recipe:
            recipe = Recipe(
                name=recipe_data['name'],
                image_url=recipe_data.get('image_url', ''),
                spoonacular_url=recipe_data.get('spoonacular_url', '')  # Store sourceUrl
            )
            db.session.add(recipe)
            db.session.commit()

        # Store ingredients in the database
        for ingredient_data in recipe_data.get('extendedIngredients', []):
            ingredient_name = ingredient_data.get('name', '').lower().strip()
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_name)
                db.session.add(ingredient)
                db.session.commit()

            existing_link = RecipeIngredient.query.filter_by(recipe_id=recipe.id, ingredient_id=ingredient.id).first()
            if not existing_link:
                new_link = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient.id)
                db.session.add(new_link)
                db.session.commit()

# Get AI recipe suggestions using user ingredients
def get_ai_recipe_suggestions(ingredients):
    ingredient_list = ", ".join(ingredients)
    full_prompt = f"""
    Create a detailed recipe using the following ingredients: {ingredient_list}.
    
    Include:
    1. A creative name for the dish
    2. Full list of ingredients with measurements
    3. Step-by-step cooking instructions
    4. Approximate nutritional information (calories, protein, fat, carbs)
    5. Serving suggestions
    
    Be creative but make sure the recipe is practical and delicious.
    """
    
    try:
        # Send request to Ollama running locally
        response = requests.post("http://localhost:11434/api/generate", 
                                json={
                                    "model": "llama3.2:1b",
                                    "prompt": full_prompt,
                                    "stream": False
                                })
        
        if response.status_code == 200:
            result = response.json()
            recipe_text = result.get('response', '')
            return {
                "success": True,
                "recipe_text": recipe_text
            }
        else:
            return {
                "success": False,
                "message": f"Error from Ollama API: {response.status_code}",
                "details": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error communicating with Ollama: {str(e)}"
        }

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Fetch and store recipes based on user input (from ingredients)
@app.route('/fetch_and_store_recipes', methods=['POST'])
def fetch_and_store_recipes():
    ingredients = request.form.getlist('ingredients')
    dietary_preferences = request.form.get('diet', 'vegetarian')
    max_calories = int(request.form.get('max_calories', 500))

    recipes_batch = fetch_recipes_based_on_user_input(ingredients, dietary_preferences, max_calories)
    store_recipe_data(recipes_batch)

    return redirect(url_for('recommend_by_ingredients', ingredients=','.join(ingredients)))

# Recommend recipes by ingredients
@app.route('/recommend_by_ingredients', methods=['POST'])  # Change this to POST if you're using POST method
def recommend_by_ingredients():
    data = request.json  # Parse incoming JSON data (from frontend)
    ingredients = data.get('ingredients')  # Get the ingredients from the POST body
    
    if not ingredients:
        return jsonify({"recipes": [], "message": "No ingredients provided."})
    
    # Clean and split the ingredients into a list
    user_ingredients = [i.lower().strip() for i in ingredients.split(',')]

    # Reset the database to clear old data
    db.session.query(RecipeIngredient).delete()
    db.session.query(Ingredient).delete()
    db.session.query(Recipe).delete()
    db.session.commit()

    # Default values for dietary preferences and max_calories
    dietary_preferences = "vegetarian"
    max_calories = 10000

    # Fetch new recipes based on the provided ingredients and default dietary preferences
    new_recipes = fetch_recipes_based_on_user_input(user_ingredients, dietary_preferences, max_calories)

    if not new_recipes:
        return jsonify({"recipes": [], "message": "No recipes found."})

    # Store the new recipes in the database
    store_recipe_data(new_recipes)

    # Retrieve all recipes from the database
    recipes = Recipe.query.all()
    results = [{"name": r.name, "image_url": r.image_url, "spoonacular_url": r.spoonacular_url} for r in recipes]

    return jsonify({"recipes": results, "message": "Recipes fetched successfully"})

# Fetch recipes based on nutrition (from Spoonacular API)
def fetch_recipes_by_nutrition(min_calories, max_calories, min_protein, max_protein, min_fat, max_fat, min_carbs, max_carbs):
    params = {
        "apiKey": "07b08237eccf4fb389abd8ccae6f24dc",  # Your API key here
        "minCalories": min_calories,
        "maxCalories": max_calories,
        "minProtein": min_protein,
        "maxProtein": max_protein,
        "minFat": min_fat,
        "maxFat": max_fat,
        "minCarbs": min_carbs,
        "maxCarbs": max_carbs,
        "number": 5  # Limit the number of recipes for testing
    }

    response = requests.get("https://api.spoonacular.com/recipes/findByNutrients", params=params)

    if response.status_code == 200:
        recipes = response.json()
        detailed_recipes = []

        for recipe in recipes:
            recipe_id = recipe['id']
            detailed_recipe = get_recipe_information(recipe_id)
            detailed_recipes.append(detailed_recipe)

        return detailed_recipes
    else:
        return []

# Recommend recipes by nutrition
@app.route('/recommend_by_nutrition', methods=['POST'])
def recommend_by_nutrition():
    # Get the nutritional data from the POST request
    data = request.json  # This will automatically parse JSON from the request body
    
    # Extract nutritional values
    min_calories = data.get('min_calories', 100)
    max_calories = data.get('max_calories', 500)
    min_protein = data.get('min_protein', 5)
    max_protein = data.get('max_protein', 50)
    min_fat = data.get('min_fat', 1)
    max_fat = data.get('max_fat', 30)
    min_carbs = data.get('min_carbs', 5)
    max_carbs = data.get('max_carbs', 100)

    # Reset the database to clear out old recipes
    db.session.query(RecipeIngredient).delete()
    db.session.query(Ingredient).delete()
    db.session.query(Recipe).delete()
    db.session.commit()

    # Fetch new recipes based on the nutritional data
    new_recipes = fetch_recipes_by_nutrition(
        min_calories, max_calories, min_protein, max_protein,
        min_fat, max_fat, min_carbs, max_carbs
    )

    # If no recipes are found, return a message
    if not new_recipes:
        return jsonify({"recipes": [], "message": "No recipes found based on the selected nutritional criteria."})

    # Store the newly fetched recipes in the database
    store_recipe_data(new_recipes)

    # Retrieve all recipes from the database to return to the frontend
    recipes = Recipe.query.all()
    results = [{"name": r.name, "image_url": r.image_url, "spoonacular_url": r.spoonacular_url} for r in recipes]

    # Return the recipes in JSON format
    return jsonify({"recipes": results, "message": "Recipes fetched successfully"})


# AI Recipe suggestion route
@app.route('/ai_recipe_suggestion', methods=['GET'])
def ai_recipe_suggestion():
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400
        
        # Generate the recipe using AI function
        result = get_ai_recipe_suggestions(ingredients)
        
        if result["success"]:
            return jsonify({"recipe_text": result["recipe_text"]})
        else:
            return jsonify({"error": result["message"]}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
