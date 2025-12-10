








def get_top_ingredients(limit: int = 12) -> List[Tuple[str, int]]:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
      """
      SELECT Ingredients.name, COUNT(*) AS usage_count
      FROM MealIngredients
      JOIN Ingredients ON MealIngredients.ingredient_id = Ingredients.ingredient_id
      GROUP BY Ingredients.name
      ORDER BY usage_count DESC
      LIMIT ?
      """,
      (limit,),
  )
  rows = cursor.fetchall()
  connection.close()
  return [(row[0], row[1]) for row in rows]















def get_meal_ingredient_summary() -> Dict[str, float]:
  connection = get_connection()
  cursor = connection.cursor()

  cursor.execute("SELECT COUNT(*) FROM Meals")
  meal_count_row = cursor.fetchone()
  total_meals = meal_count_row[0] if meal_count_row is not None else 0

  cursor.execute(
      """
      SELECT Meals.meal_id, COUNT(MealIngredients.ingredient_id) AS ingredient_count
      FROM Meals
      LEFT JOIN MealIngredients ON Meals.meal_id = MealIngredients.meal_id
      GROUP BY Meals.meal_id
      """
  )
  ingredient_rows = cursor.fetchall()
  connection.close()

  if total_meals == 0:
      avg_ingredients = 0.0
  else:
      total_ingredients = sum(row[1] for row in ingredient_rows)
      avg_ingredients = total_ingredients / float(total_meals)

  return {
      "total_meals": float(total_meals),
      "avg_ingredients_per_meal": float(avg_ingredients),
  }



def write_calculations_to_file(output_path: str = "results_summary.txt") -> None:
  brewery_type_counts = get_brewery_type_counts()
  glass_type_counts = get_glass_type_counts()
  top_ingredients = get_top_ingredients()
  top_states = get_brewery_counts_by_state()
  meal_summary = get_meal_ingredient_summary()

  lines: List[str] = []

  lines.append("Brewery Types by Count\n")
  for name, count in brewery_type_counts:
      lines.append(f"  {name}: {count}\n")
  lines.append("\n")

  lines.append("Cocktail Glass Types by Count\n")
  for name, count in glass_type_counts:
      lines.append(f"  {name}: {count}\n")
  lines.append("\n")

  lines.append("Top Ingredients in Meals\n")
  for name, count in top_ingredients:
      lines.append(f"  {name}: {count}\n")
  lines.append("\n")

  lines.append("Top States by Number of Breweries\n")
  for state_name, count in top_states:
      lines.append(f"  {state_name}: {count}\n")
  lines.append("\n")

  lines.append("Meal and Ingredient Summary\n")
  lines.append(f"  Total meals: {int(meal_summary['total_meals'])}\n")
  lines.append(
      "  Average ingredients per meal: "
      f"{meal_summary['avg_ingredients_per_meal']:.2f}\n"
  )

  with open(output_path, "w", encoding="utf-8") as file:
      file.writelines(lines)