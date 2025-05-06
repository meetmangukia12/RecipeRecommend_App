import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchByIngredients } from "../api";  // Import the function to fetch recipes based on ingredients
import "./IngredientSearch.css";  // Import the CSS for styling

const IngredientSearch = () => {
  const [loading, setLoading] = useState(false);  // Loading state for the search
  const [ingredients, setIngredients] = useState("");  // State to store user input for ingredients
  const navigate = useNavigate();  // React Router's navigate function to redirect

  // Function to handle search and redirect
  const handleSearch = async () => {
    setLoading(true);  // Set loading state to true while fetching data
    try {
      // Sending the ingredients data to backend API via POST request
      const response = await fetchByIngredients(ingredients);
      const recipes = response.recipes;  // Get recipes from response

      if (recipes && recipes.length > 0) {
        // Redirect to the IngredientResults page and pass recipes via state
        navigate("/ingredient-results", { state: { recipes } });
      } else {
        // If no recipes, display an alert or message to the user
        alert("No recipes found based on the ingredients.");
      }
    } catch (err) {
      console.error("Failed to fetch ingredient-based recipes", err);
    } finally {
      setLoading(false);  // Set loading state to false after data is fetched
    }
  };

  return (
    <div className="background">
    <div className="ingredient-search-wrapper">
      <section className="hero">
        <div className="hero-content">
          <h1>Ingredient-Based Recipe Recommendation</h1>
          <p>Enter your ingredients and get personalized recipe suggestions from our AI.</p>
          
        </div>
      </section>

      <section className="search-section">
        <h2>Search Recipes by Ingredients</h2>
        <div className="search-box">
          <input
            type="text"
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}  // Update ingredients as user types
            placeholder="Enter ingredients separated by commas"
          />
          <button onClick={handleSearch} className="search-btn">
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </section>

      
    </div>
    </div>
  );
};

export default IngredientSearch;