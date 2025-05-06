import React, { useState } from "react";
import { useNavigate } from "react-router-dom";  // Import useNavigate for page navigation
import { fetchByNutrition } from "../api"; // ✅ Import the API function
import "./NutritionSearch.css";

const NutritionSearch = () => {
  const [loading, setLoading] = useState(false); // Loading state
  const [nutrition, setNutrition] = useState({
    minCalories: 100,
    maxCalories: 500,
    minProtein: 5,
    maxProtein: 50,
    minFat: 1,
    maxFat: 30,
    minCarbs: 5,
    maxCarbs: 100,
  });

  const navigate = useNavigate(); // Initialize useNavigate to navigate to another page

  // Function to handle form field updates
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNutrition(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSearch = async () => {
    setLoading(true); // Set loading state to true while fetching data
    try {
      const response = await fetchByNutrition(nutrition); // Send the POST request
      const recipes = response.recipes; // Get recipes from the response

      // Navigate to the NutritionResults page and pass the recipes as state
      navigate("/nutrition-results", { state: { recipes } });
    } catch (err) {
      console.error("Failed to fetch nutrition recipes", err);
    } finally {
      setLoading(false); // Set loading to false once data is fetched
    }
  };

  return (
    <div class="container">
      <div class="main-banner">
      <h1>Nutrition-Based Recommendations</h1>
      <p>Explore healthy recipes tailored to your needs</p>
      

      <section class="nutrition-inputs">
    <div class="input-container1">
      <h3>Set Your Nutritional Ranges</h3>
      <input type="number" placeholder="Min Calories" class="input-field" />
      <input type="number" placeholder="Max Calories" class="input-field" />
      <input type="number" placeholder="Min Protein" class="input-field" />
      <input type="number" placeholder="Max Protein" class="input-field" />
      <input type="number" placeholder="Min Fat" class="input-field" />
      <input type="number" placeholder="Max Fat" class="input-field" />
      <input type="number" placeholder="Min Carbs" class="input-field" />
      <input type="number" placeholder="Max Carbs" class="input-field" />
      <button onClick={handleSearch} className="cta-btn2">
            {loading ? "Searching..." : "Get Recommendations"}
      </button>
    </div>
  </section>  
      </div>

    
    
    
    </div>
  );
};

export default NutritionSearch;
