import requests
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import process

app = Flask(__name__)
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
        "apiKey": "29b63e9ae1f246b087b9cf5fc8c8b0ac",
        "number": batch_size,
        "ingredients": ','.join(ingredients),
        "diet": dietary_preferences,
        "maxCalories": max_calories,
    }
    
    response = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=params)
    return response.json() if response.status_code == 200 else []

# Extract numeric values from Spoonacular nutrition data (e.g., '5g' -> 5.0)
def extract_numeric(value):
    match = re.search(r"[\d.]+", str(value))
    return float(match.group()) if match else 0.0

# Store fetched recipes in the database
def store_recipe_data(recipes):
    for recipe_data in recipes:
        recipe = Recipe.query.filter_by(name=recipe_data['title']).first()
        if not recipe:
            recipe = Recipe(
                name=recipe_data['title'],
                image_url=recipe_data.get('image', ''),
                spoonacular_url=recipe_data.get('sourceUrl', '')
            )
            db.session.add(recipe)
            db.session.commit()

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

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Fetch and store recipes based on user input
@app.route('/fetch_and_store_recipes', methods=['POST'])
def fetch_and_store_recipes():
    ingredients = request.form.getlist('ingredients')
    dietary_preferences = request.form.get('diet', 'vegetarian')
    max_calories = int(request.form.get('max_calories', 500))

    recipes_batch = fetch_recipes_based_on_user_input(ingredients, dietary_preferences, max_calories)
    store_recipe_data(recipes_batch)

    return redirect(url_for('recommend_by_ingredients', ingredients=','.join(ingredients)))

# Recommend recipes by ingredients
@app.route('/recommend_by_ingredients', methods=['GET'])
def recommend_by_ingredients():
    user_ingredients = request.args.get('ingredients')
    if not user_ingredients:
        return render_template('ingredientSearch.html', recipes=None)

    user_ingredients = [i.lower().strip() for i in user_ingredients.split(',')]

    # Reset the database
    db.session.query(RecipeIngredient).delete()
    db.session.query(Ingredient).delete()
    db.session.query(Recipe).delete()
    db.session.commit()

    dietary_preferences = "vegetarian"
    max_calories = 500
    new_recipes = fetch_recipes_based_on_user_input(user_ingredients, dietary_preferences, max_calories)

    if not new_recipes:
        return render_template('ingredientSearch.html', recipes=[], message="No recipes found.")

    store_recipe_data(new_recipes)

    recipes = Recipe.query.all()
    results = [{"name": r.name, "image_url": r.image_url, "spoonacular_url": r.spoonacular_url} for r in recipes]

    return render_template('ingredientSearch.html', recipes=results, message=None)

# Fetch recipes based on nutrition from Spoonacular API
def fetch_recipes_by_nutrition(min_calories, max_calories, min_protein, max_protein, min_fat, max_fat, min_carbs, max_carbs):
    params = {
        "apiKey": "29b63e9ae1f246b087b9cf5fc8c8b0ac",
        "minCalories": min_calories,
        "maxCalories": max_calories,
        "minProtein": min_protein,
        "maxProtein": max_protein,
        "minFat": min_fat,
        "maxFat": max_fat,
        "minCarbs": min_carbs,
        "maxCarbs": max_carbs,
        "number": 5
    }

    response = requests.get("https://api.spoonacular.com/recipes/findByNutrients", params=params)
    return response.json() if response.status_code == 200 else []

# Recommend recipes by nutrition
@app.route('/recommend_by_nutrition', methods=['GET'])
def recommend_by_nutrition():
    min_calories = request.args.get('min_calories', type=int, default=100)
    max_calories = request.args.get('max_calories', type=int, default=500)
    min_protein = request.args.get('min_protein', type=int, default=5)
    max_protein = request.args.get('max_protein', type=int, default=50)
    min_fat = request.args.get('min_fat', type=int, default=1)
    max_fat = request.args.get('max_fat', type=int, default=30)
    min_carbs = request.args.get('min_carbs', type=int, default=5)
    max_carbs = request.args.get('max_carbs', type=int, default=100)

    # Reset the database
    db.session.query(RecipeIngredient).delete()
    db.session.query(Ingredient).delete()
    db.session.query(Nutrition).delete()
    db.session.query(Recipe).delete()
    db.session.commit()

    new_recipes = fetch_recipes_by_nutrition(min_calories, max_calories, min_protein, max_protein, min_fat, max_fat, min_carbs, max_carbs)

    if not new_recipes:
        return render_template('nutritionSearch.html', recipes=[], message="No recipes found.")

    store_recipe_data(new_recipes)

    recipes = Recipe.query.join(Nutrition).all()
    results = [{"name": r.name, "image_url": r.image_url, "spoonacular_url": r.spoonacular_url} for r in recipes]

    return render_template('nutritionSearch.html', recipes=results, message=None)

if __name__ == '__main__':
    app.run(debug=True)
