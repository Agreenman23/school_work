--TO CREATE THE NEW DATABASE FOR THE PIZZERIA

--C:\Users\User>docker exec -it nosql-postgres /bin/bash
--root@nosql-postgres:/# su - postgres
--postgres@nosql-postgres:~$ createdb Bob_Pizza
--postgres@nosql-postgres:~$ psql Bob_Pizza

--TO CREATE THE USERS TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Users (
User_ID serial PRIMARY KEY,
Email_Address varchar(255) NOT NULL,
First_Name varchar(255) NOT NULL,
Last_Name varchar(255) NOT NULL,
Phone_Number varchar(255) NOT NULL,
Address_Line_1 varchar(255) NOT NULL,
Address_Line_2 varchar(255) NOT NULL,
City varchar(255) NOT NULL,
State char(2) NOT NULL,
Zip varchar(10) NOT NULL
);


--ADD USERS INTO THE Users TABLE
\i /app/postgres/examples/usersinsert.sql

--TO CREATE THE Inventory TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Inventory (
Ingredient_ID serial PRIMARY KEY,
Ingredient_Name varchar(255) NOT NULL,
Description varchar(255) NOT NULL,
Quantity integer NOT NULL
);

--ADD INGREDIENTS INTO THE Inventory TABLE
\i /app/postgres/examples/inventoryinsert.sql


--TO CREATE THE Recipes TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Recipes (
Recipe_ID serial PRIMARY KEY,
Recipe_Name varchar(255) NOT NULL,
Description varchar(255) NOT NULL,
Instructions varchar(500)[] NOT NULL
);

--ADD RECIPES INTO THE Recipes TABLE
\i /app/postgres/examples/recipesinsert.sql

--Create intermediate join table to map the many => many relationship between
--them. A recipe references many ingredient, and an ingredient is referenced
--by many recipes

--TO CREATE THE Inventory_Recipe_Relation TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Inventory_Recipe_Relation(
Inv_Recipe_ID serial PRIMARY KEY,
Recipe_ID integer REFERENCES Recipes(Recipe_ID),
Ingredient_ID integer REFERENCES Inventory(Ingredient_ID),
Quantity_Needed integer NOT NULL
);

--POPULATE THE Inventory_Recipe_Relation TABLE
\i /app/postgres/examples/recipe_inv_relation_insert.sql


--TO CREATE THE Orders TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Orders(
Order_ID serial PRIMARY KEY,
User_ID integer REFERENCES Users(User_ID),
Recipe_ID integer REFERENCES Recipes(Recipe_ID),
Time_Of_Order TIMESTAMP DEFAULT current_timestamp
);

--The Orders table is populated using Postgres syntax below

--THIS IS COOL!!!! Generate records using Postgres (and the
--take_order function) rather than Python
select take_order(floor(random() * 25 + 1)::int
  , floor(random() * 25 + 1)::int)
from generate_series(1,50000) i;

--Another option to generate records using Postgres code rather than Python

-- insert into Orders (User_ID, Recipe_ID) VALUES (6, 10);
-- select floor(random() * 25 + 1)::int as recipe_id
--   , floor(random() * 25 + 1)::int as User_id
-- from generate_series(1,50000) i;

--Change column name in mapping table when I realized the name of the column
--was misleading. Had to change in Python and in the create table instructions

--ALTER TABLE Inventory_Recipe_Relation RENAME COLUMN Inventory_Quantity TO Quantity_Needed;

--Change quantity of spam to a lower number to ensure the error is throw when
--there is not sufficient inventory to fulfill a given order

--UPDATE Inventory SET Quantity = 20 WHERE Ingredient_ID = 13;



--Change quantitities back to huge number so errors aren't thrown during insert
--into Orders table
--UPDATE Inventory SET Quantity = 10000000;
