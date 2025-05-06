import React from "react";
import { useLocation } from "react-router-dom";
import "./IngredientResults.css";  

const IngredientResults = () => {
  const location = useLocation();  // Get state passed from IngredientSearch
  const { recipes } = location.state || {};  // Retrieve recipes from the state

  return (
    <div className="ingredient-results-wrapper">
      <h1>Recipe Suggestions Based on Ingredients</h1>
      <div className="recipe-results">
        {recipes && recipes.length > 0 ? (
          recipes.map((recipe, index) => (
            <a key={index} href={recipe.spoonacular_url} target="_blank" rel="noopener noreferrer" className="recipe-card-link">
              <div className="recipe-card">
                <img
                  src={recipe.image_url}  
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
          <p>No recipes found based on the selected ingredients.</p>
        )}
      </div>
    </div>
  );
};

export default IngredientResults;
