document.getElementById('ingredient-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const ingredients = document.getElementById('ingredients').value;
    const recipesDiv = document.getElementById('recipes');
    recipesDiv.innerHTML = "<p>Loading recipes...</p>";
  
    try {
      const response = await fetch(`http://127.0.0.1:5000/recipes?ingredients=${encodeURIComponent(ingredients)}`);
      const data = await response.json();
  
      recipesDiv.innerHTML = "";
      if (data.recipes.length === 0) {
        recipesDiv.innerHTML = "<p>No recipes found.</p>";
        return;
      }
  
      data.recipes.forEach(recipe => {
        const col = document.createElement('div');
        col.className = 'col-md-4';
  
        col.innerHTML = `
          <div class="card h-100">
            <img src="${recipe.image}" class="card-img-top" alt="${recipe.title}" />
            <div class="card-body">
              <h5 class="card-title">${recipe.title}</h5>
              <a href="${recipe.sourceUrl}" class="btn btn-primary" target="_blank">View Recipe</a>
            </div>
          </div>
        `;
        recipesDiv.appendChild(col);
      });
    } catch (error) {
      recipesDiv.innerHTML = `<p>Error fetching recipes.</p>`;
      console.error(error);
    }
  });
  