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