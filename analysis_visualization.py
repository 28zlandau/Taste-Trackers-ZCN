








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