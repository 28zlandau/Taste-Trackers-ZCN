








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


















def plot_top_ingredients_scatter(output_file: str = "ingredients_top12.png") -> None:
  counts = get_top_ingredients(12)
  if not counts:
      return

  ingredient_names, meal_counts = zip(*counts)
  ranks = list(range(1, len(ingredient_names) + 1))
  fig, axis = plt.subplots(figsize=(12, 6))

  axis.scatter(
      ranks,
      meal_counts,
      s=80,
      color="darkorange",
      edgecolors="black",
  )
  for x_position, y_position, label in zip(ranks, meal_counts, ingredient_names):
      axis.text(
          x_position,
          y_position + 0.5,
          label,
          ha="center",
          va="bottom",
          fontsize=8,
          rotation=45,
      )
  axis.set_xticks(ranks)
  axis.set_xticklabels(ranks)
  axis.set_xlabel("Ingredient Rank (1 = most common)")
  axis.set_ylabel("Number of Meals")
  axis.set_title("Top 12 Ingredients in Meals by Frequency")
  axis.grid(True, linestyle="--", alpha=0.3)

  _ensure_output_folder_exists(output_file)
  fig.tight_layout()
  fig.savefig(output_file, bbox_inches="tight")
  plt.close(fig)












    def test_meals_at_least_100(self) -> None:
      for run_index in range(5):
          load_meals()
      connection = get_connection()
      cursor = connection.cursor()
      cursor.execute("SELECT COUNT(*) FROM Meals")
      count_row = cursor.fetchone()
      connection.close()
      self.assertIsNotNone(count_row)
      self.assertGreaterEqual(count_row[0], 100)


      