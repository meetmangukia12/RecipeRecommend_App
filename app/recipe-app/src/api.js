// src/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000", 
});

// Function to fetch recipes based on ingredients
export const fetchByIngredients = async (ingredients) => {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/recommend_by_ingredients`, {
      ingredients: ingredients  // Send ingredients as an array
    }, {
      headers: {
        'Content-Type': 'application/json', // Ensure proper request type
      },
    });
    return response.data;  // Return recipes from the response
  } catch (error) {
    console.error("Error fetching recipes based on ingredients:", error);
    throw error;  // Propagate error to be handled in the frontend
  }
};

  export const fetchByNutrition = async (nutrition) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/recommend_by_nutrition`, nutrition, {
        headers: {
          'Content-Type': 'application/json', // Ensure this header is set to application/json
        }
      });
      return response.data; // Return the recipes from Flask backend
    } catch (error) {
      console.error("Error fetching nutrition recipes:", error);
      throw error; // Propagate the error for frontend handling
    }
  };

  export const getAiRecipe = async (ingredients) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/ai_recipe_suggestion`, 
        {
          ingredients: ingredients,  // Send the ingredients as JSON in the request body
        },
        {
          headers: {
            "Content-Type": "application/json",  // Ensure the content type is set to JSON
          },
        }
      );
      return response;  // Return the response
    } catch (error) {
      console.error("Error fetching AI recipe:", error);
      throw error;
    }
  };
