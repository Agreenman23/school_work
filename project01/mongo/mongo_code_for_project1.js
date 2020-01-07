//TO ACCESS/CREATE DATABASE
//C:\Users\User>docker exec -it nosql-node /bin/bash
//mongo --host nosql-mongodb Pizzeria_Bob

//TO CREATE THE USERS COLLECTION WITH THE REQUIRED FIELDS
db.Users.insert({
	_id: 'userid_0',
	Email_Address: "alex@pizzeria_bob.com",
	First_Name: "Alex",
	Last_Name: "Greenman",
	Phone_Number: "303-562-5801",
	Address_Line_1: "6017 E Briarwood Cir",
	Address_Line_2: "Apt A324",
	City: "Centennial",
	State: "Colorado",
	Zip: "80112"
})

load('/app/mongodb/examples/usersinsert.js')

//TO CREATE THE INGREDIENTS COLLECTION WITH THE REQUIRED FIELDS
db.Inventory.insert({
	_id: "inv_0",
	Ingredient_Name: "cheese",
	Ingredient_Description: "cheese imported weekly from Italy",
	Quantity: 173317
})

load('/app/mongodb/examples/NEWinventoryinsert.js')

//TO CREATE THE INGREDIENTS COLLECTION WITH THE REQUIRED FIELDS
db.Recipes.insert({
	_id: "rec_0",
	Recipe_Name: "pepperoni pizza",
	Recipe_Description: "pizza with pepperoni on top of it",
	Ingredients: ['inv_18', 'inv_12', 'inv_21', 'inv_5'],
	Quantities: [10, 23, 3, 19],
	Recipe_Instructions: "slice pepperoni, then place on top of pizza, then bake"
})

load('/app/mongodb/examples/NEWrecipeinsert1.js')
