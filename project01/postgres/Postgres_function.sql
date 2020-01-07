CREATE OR REPLACE FUNCTION take_order(
  UserID integer,
  RecipeID integer)
RETURNS integer AS $$
DECLARE
  ingredients_missing integer := 0;
BEGIN
  SELECT COUNT(*) INTO ingredients_missing
  FROM Recipes r
  INNER JOIN Inventory_Recipe_Relation m
  ON r.Recipe_ID = m.Recipe_id
  LEFT OUTER JOIN Inventory i
  ON m.Ingredient_ID = i.Ingredient_ID AND m.Quantity_Needed <= i.Quantity
  WHERE r.Recipe_ID = RecipeID AND i.Ingredient_Name IS NULL;

  IF ingredients_missing > 0 THEN
      RAISE EXCEPTION 'Not enough quantity';
  ELSE
    UPDATE Inventory i
    SET Quantity = i.Quantity - m.Quantity_Needed
    FROM Inventory_Recipe_Relation m
    WHERE m.Recipe_ID = RecipeID AND m.Ingredient_ID = i.Ingredient_ID;
    INSERT INTO Orders (User_ID, Recipe_ID, Time_Of_Order) VALUES (UserID, RecipeID, Now());

  END IF;
  RETURN(SELECT ingredients_missing);
END;
$$ LANGUAGE plpgsql;


--join newly created table with inventory by adding to the join table
--where clause after the joins (based on quatity), where the right side
--is null


--
-- UPDATE Inventory i
-- SET Quantity = i.Quantity - m.Quantity_Needed
-- FROM Inventory_Recipe_Relation m
-- WHERE m.Recipe_ID = RecipeID AND m.Ingredient_ID = i.Ingredient_ID;


--'take order' means that the decrement took place
