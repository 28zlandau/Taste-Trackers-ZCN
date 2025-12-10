








def create_database() -> None:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS Ingredients (
          ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT UNIQUE
      )
      """
  )

  cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS Meals (
          meal_id INTEGER PRIMARY KEY,
          name TEXT,
          instructions TEXT
      )
      """
  )

  cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS MealIngredients (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          meal_id INTEGER,
          ingredient_id INTEGER,
          UNIQUE (meal_id, ingredient_id),
          FOREIGN KEY (meal_id) REFERENCES Meals(meal_id),
          FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
      )
      """
  )















  def get_or_create_ingredient(cursor: sqlite3.Cursor, name: str) -> int:
  cleaned = normalize_string(name)
  if not cleaned:
      raise ValueError("Ingredient name must be non-empty")
  cursor.execute(
      "INSERT OR IGNORE INTO Ingredients (name) VALUES (?)",
      (cleaned,),
  )
  cursor.execute(
      "SELECT ingredient_id FROM Ingredients WHERE name = ?",
      (cleaned,),
  )
  row = cursor.fetchone()
  if row is None:
      raise RuntimeError("Could not retrieve ingredient_id")
  return int(row[0])














def load_meals(limit: int = 25) -> None:
  create_database()
  connection = get_connection()
  cursor = connection.cursor()

  inserted_this_run = 0
  alphabet = "abcdefghijklmnopqrstuvwxyz"

  for letter in alphabet:
      if inserted_this_run >= limit:
          break

      params = {"f": letter}
      data = fetch_json(f"{MEALDB_API_BASE}search.php", params=params)
      meals = data.get("meals") or []
      for meal in meals:
          if inserted_this_run >= limit:
              break

          try:
              meal_id = int(meal.get("idMeal"))
          except (TypeError, ValueError):
              continue

          cursor.execute("SELECT 1 FROM Meals WHERE meal_id = ?", (meal_id,))
          if cursor.fetchone():
              continue

          name = normalize_string(meal.get("strMeal"))
          instructions = normalize_string(meal.get("strInstructions"))

          cursor.execute(
              """
              INSERT INTO Meals (meal_id, name, instructions)
              VALUES (?, ?, ?)
              """,
              (meal_id, name, instructions),
          )

          for ingredient_index in range(1, 21):
              ingredient_name = normalize_string(
                  meal.get(f"strIngredient{ingredient_index}")
              )
              if not ingredient_name:
                  continue

              ingredient_id = get_or_create_ingredient(cursor, ingredient_name)
              cursor.execute(
                  """
                  INSERT OR IGNORE INTO MealIngredients (meal_id, ingredient_id)
                  VALUES (?, ?)
                  """,
                  (meal_id, ingredient_id),
              )

          inserted_this_run += 1

  connection.commit()
  connection.close()