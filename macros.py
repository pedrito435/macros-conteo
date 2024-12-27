<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calorie and Macronutrient Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .container {
            max-width: 800px;
            margin: auto;
        }
        h1 {
            text-align: center;
        }
        nav {
            display: flex;
            justify-content: space-around;
            background-color: #f4f4f4;
            padding: 10px;
        }
        nav a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
            padding: 5px 10px;
            border-radius: 5px;
        }
        nav a:hover {
            background-color: #ddd;
        }
        section {
            display: none;
        }
        section.active {
            display: block;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .form-group {
            margin-bottom: 45px; /* Spacing equivalent to 3 lines */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calorie and Macronutrient Tracker</h1>
        <nav>
            <a href="#" onclick="showSection('food-and-calculator-section')">Lista de alimentos y consumo</a>
            <a href="#" onclick="showSection('recipes-section')">Recetas</a>
        </nav>

        <section id="food-and-calculator-section" class="active">
            <div class="grid">
                <div>
                    <h2>Food List</h2>
                    <div class="form-group">
                        <label for="food-name">Food Name</label>
                        <input type="text" id="food-name" placeholder="e.g., Chicken Breast">
                    </div>
                    <div class="form-group">
                        <label for="calories">Calories (per 100g)</label>
                        <input type="number" id="calories" placeholder="e.g., 165">
                    </div>
                    <button onclick="addFood()">Add Food</button>
                    <button onclick="confirmClearData()">Clear All Data</button>

                    <table id="food-table">
                        <thead>
                            <tr>
                                <th>Food</th>
                                <th>Calories</th>
                                <th>Remove</th>
                            </tr>
                        </thead>
                        <tbody>
                        </tbody>
                    </table>

                    <h2>Total Daily Intake</h2>
                    <p>Calories: <span id="total-calories">0</span></p>
                </div>

                <div>
                    <h2>Calorie Calculator</h2>
                    <div class="form-group">
                        <label for="weight">Weight (kg)</label>
                        <input type="number" id="weight" placeholder="e.g., 70">
                    </div>
                    <div class="form-group">
                        <label for="height">Height (cm)</label>
                        <input type="number" id="height" placeholder="e.g., 175">
                    </div>
                    <div class="form-group">
                        <label for="age">Age (years)</label>
                        <input type="number" id="age" placeholder="e.g., 25">
                    </div>
                    <div class="form-group">
                        <label for="activity-level">Activity Level</label>
                        <select id="activity-level">
                            <option value="1.2">Sedentary</option>
                            <option value="1.375">Lightly Active</option>
                            <option value="1.55">Moderately Active</option>
                            <option value="1.725">Very Active</option>
                            <option value="1.9">Extra Active</option>
                        </select>
                    </div>
                    <button onclick="calculateCalories()">Calculate Daily Calorie Needs</button>
                    <p>Your Daily Calorie Needs: <span id="daily-calories">0</span> kcal</p>
                </div>
            </div>
        </section>

        <section id="recipes-section">
            <h2>Recipes</h2>
            <div class="form-group">
                <label for="recipe-name">Recipe Name</label><input type="text" id="recipe-name">
            </div>
            <div class="form-group">
                <label for="recipe-ingredients">Ingredients</label>
                <textarea id="recipe-ingredients" placeholder="e.g., Chicken, Lettuce, Tomato, Olive Oil"></textarea>
            </div>
            <div class="form-group">
                <label for="recipe-instructions">Instructions</label>
                <textarea id="recipe-instructions" placeholder="e.g., Grill the chicken and mix with other ingredients."></textarea>
            </div>
            <button onclick="addRecipe()">Add Recipe</button>

            <h2>Recipe List</h2>
            <div id="recipe-list">
                <p>No recipes added yet.</p>
            </div>
        </section>
    </div>

    <script>
        const sections = document.querySelectorAll('section');

        function showSection(sectionId) {
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === sectionId) {
                    section.classList.add('active');
                }
            });
        }

        // Other JavaScript functions remain unchanged

        const foodTable = document.getElementById('food-table').querySelector('tbody');
        const totalCaloriesEl = document.getElementById('total-calories');
        const dailyCaloriesEl = document.getElementById('daily-calories');
        const recipeList = document.getElementById('recipe-list');

        let totalCalories = 0;

        // Load saved data
        window.onload = function() {
            const savedData = JSON.parse(localStorage.getItem('calorieTrackerData'));
            if (savedData) {
                totalCalories = savedData.totalCalories;
                totalCaloriesEl.textContent = totalCalories;
                dailyCaloriesEl.textContent = savedData.dailyCalories;
                savedData.foodList.forEach(food => {
                    addFoodToTable(food.name, food.calories);
                });
                if (savedData.recipes && savedData.recipes.length > 0) {
                    savedData.recipes.forEach(recipe => {
                        addRecipeToList(recipe.name, recipe.ingredients, recipe.instructions);
                    });
                }
            }
        };

        function addFood() {
            const name = document.getElementById('food-name').value;
            const calories = parseFloat(document.getElementById('calories').value) || 0;

            if (name.trim() === '') {
                alert('Please enter a food name.');
                return;
            }

            addFoodToTable(name, calories);

            totalCalories += calories;
            updateTotals();

            document.getElementById('food-name').value = '';
            document.getElementById('calories').value = '';
            saveData();
        }

        function addFoodToTable(name, calories) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${name}</td>
                <td>${calories}</td>
                <td><button onclick="removeFood(this, ${calories})">Remove</button></td>
            `;
            foodTable.appendChild(row);
        }

        function removeFood(button, calories) {
            const row = button.parentElement.parentElement;
            foodTable.removeChild(row);

            totalCalories -= calories;
            updateTotals();
            saveData();
        }

        function updateTotals() {
            totalCaloriesEl.textContent = totalCalories;
        }

        function calculateCalories() {
            const weight = parseFloat(document.getElementById('weight').value) || 0;
            const height = parseFloat(document.getElementById('height').value) || 0;
            const age = parseFloat(document.getElementById('age').value) || 0;
            const activityLevel = parseFloat(document.getElementById('activity-level').value);

            if (weight === 0 || height === 0 || age === 0) {
                alert('Please fill in all fields.');
                return;
            }

            // Mifflin-St Jeor Equation
            const bmr = 10 * weight + 6.25 * height - 5 * age + 5; // For men; subtract 161 for women
            const dailyCalories = bmr * activityLevel;

            dailyCaloriesEl.textContent = dailyCalories.toFixed(2);
            saveData();
        }

        function addRecipe() {
            const name = document.getElementById('recipe-name').value;
            const ingredients = document.getElementById('recipe-ingredients').value;
            const instructions = document.getElementById('recipe-instructions').value;

            if (name.trim() === '' || ingredients.trim() === '') {
                alert('Please fill in all recipe fields.');
                return;
            }

            addRecipeToList(name, ingredients, instructions);

            document.getElementById('recipe-name').value = '';
            document.getElementById('recipe-ingredients').value = '';
            document.getElementById('recipe-instructions').value = '';
            saveData();
        }

        function addRecipeToList(name, ingredients, instructions) {
            const recipeDiv = document.createElement('div');
            recipeDiv.innerHTML = `
                <h3>${name}</h3>
                <p><strong>Ingredients:</strong> ${ingredients}</p>
                <p><strong>Instructions:</strong> ${instructions}</p>
                <hr>
            `;
            recipeList.appendChild(recipeDiv);

            if (recipeList.querySelector('p').textContent === 'No recipes added yet.') {
                recipeList.innerHTML = '';
            }
        }

        function saveData() {
            const foodList = Array.from(foodTable.querySelectorAll('tr')).map(row => {
                const cells = row.querySelectorAll('td');
                return { name: cells[0].textContent, calories: parseFloat(cells[1].textContent) };
            });

            const recipes = Array.from(recipeList.querySelectorAll('div')).map(div => {
                const name = div.querySelector('h3').textContent;
                const ingredients = div.querySelector('p:nth-of-type(1)').textContent.replace('Ingredients: ', '');
                const instructions = div.querySelector('p:nth-of-type(2)').textContent.replace('Instructions: ', '');
                return { name, ingredients, instructions };
            });

            const data = {
                totalCalories,
                dailyCalories: dailyCaloriesEl.textContent,
                foodList,
                recipes
            };

            localStorage.setItem('calorieTrackerData', JSON.stringify(data));
        }

        function confirmClearData() {
            if (confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
                if (confirm('This is your last chance to cancel. Clear all data?')) {
                    clearData();
                }
            }
        }

        function clearData() {
            totalCalories = 0;
            totalCaloriesEl.textContent = '0';
            dailyCaloriesEl.textContent = '0';
            foodTable.innerHTML = '';
            recipeList.innerHTML = '<p>No recipes added yet.</p>';
            localStorage.removeItem('calorieTrackerData');
        }
    </script>
</body>
</html>
