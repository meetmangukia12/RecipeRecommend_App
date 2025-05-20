🥗 Recipe Recommendation Web App
❓ What is this?
This is a Flask-based web application that recommends recipes based on either:

Ingredients you have 🥕

Your desired nutritional profile (calories, protein, fat, carbs) 🥦

It uses the Spoonacular API to fetch recipe data and stores it in a local SQLite database. Users can interact through clean HTML forms and view recipes with images and links.

⚙️ How does it work?
🔍 Ingredient Mode: Enter ingredients → app hits Spoonacular API → matches recipes → displays results.

📊 Nutrition Mode: Enter nutrition ranges → app queries Spoonacular → gets recipes fitting those constraints.

🔗 Uses:

Flask for the web framework

Flask-SQLAlchemy for the database

Spoonacular API for real recipe data

HTML/CSS templates for the frontend (index.html, ingredientSearch.html, nutritionSearch.html)

📦 Stores recipes, ingredients, and their relationships in recipes.db.

🌟 Why did I build this?
To learn and demonstrate full-stack development using Python and Flask.

To make recipe discovery easier for people with dietary preferences or limited ingredients.

To practice using external APIs and relational databases in a real-world setting.
