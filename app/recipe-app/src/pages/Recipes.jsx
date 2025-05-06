import { useEffect, useState } from "react";
import axios from "axios";

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFromFlask = async () => {
      try {
        const response = await axios.get("http://localhost:5000/recommend_by_ingredients", {
          params: {
            ingredients: "tomato,cheese"
          }
        });

        console.log("Flask backend response:", response.data);
        setRecipes(response.data);
      } catch (err) {
        console.error("Flask API error:", err);
        setError("Failed to load recipes from Flask backend.");
      }
    };

    fetchFromFlask();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Recipes from Flask Backend</h2>
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {recipes.map((recipe, index) => (
          <div key={index} className="bg-white shadow rounded-lg overflow-hidden">
            <img
              src={recipe.image_url}
              alt={recipe.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h3 className="text-lg font-semibold">{recipe.name}</h3>
              <a
                href={recipe.spoonacular_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 text-sm hover:underline"
              >
                View Recipe
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recipes;
