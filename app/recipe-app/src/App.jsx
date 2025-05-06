import { Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import IngredientSearch from "./pages/IngredientSearch";
import NutritionSearch from "./pages/NutritionSearch";
import AiSuggestion from "./pages/AiSuggestion";
import IngredientResults from "./pages/IngredientResults";  // Import the IngredientResults page
import NutritionResults from "./pages/NutritionResults";

function App() {
  const location = useLocation();
  const showNavbar = location.pathname !== "/ingredient-search";

  return (
    <>
      {/* Conditionally render the Navbar */}
      {showNavbar && <Navbar />}
      
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ingredient-search" element={<IngredientSearch />} />
          <Route path="/nutrition-search" element={<NutritionSearch />} />
          <Route path="/ai-suggestion" element={<AiSuggestion />} />
          <Route path="/nutrition-results" element={<NutritionResults />} />
          <Route path="/ingredient-results" element={<IngredientResults />} />  {/* Add route for IngredientResults */}
        </Routes>
      
    </>
  );
}

export default App;
