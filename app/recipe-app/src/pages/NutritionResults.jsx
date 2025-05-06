import React from "react";
import { useLocation } from "react-router-dom";
import "./NutritionResults.css";  // Import the updated styles

const NutritionResults = () => {
  const location = useLocation();
  const { recipes } = location.state || {};  // Retrieve recipes from state

  return (
    <div className="nutrition-results-wrapper">
      <h1 className="title">Recipe Suggestions</h1>
      <div className="recipe-results">
        {recipes && recipes.length > 0 ? (
          recipes.map((recipe, index) => (
            <a key={index} href={recipe.spoonacular_url} target="_blank" rel="noopener noreferrer" className="recipe-card-link">
              <div className="recipe-card">
                <img
                  src={recipe.image_url}  // Ensure this is the correct field for the image URL
                  alt={recipe.name}
                  className="recipe-image"
                />
                <div className="card-content">
                  <h3 className="recipe-name">{recipe.name}</h3>
                  <p className="recipe-calories">
                    {recipe.calories ? `Calories: ${recipe.calories}` : ""}
                  </p>
                </div>
              </div>
            </a>
          ))
        ) : (
          <p>No recipes found based on the selected criteria.</p>
        )}
      </div>
    </div>
  );
};

export default NutritionResults;
