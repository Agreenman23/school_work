from faker import Faker
import names
from random import randint
import random
import string
import csv
import psycopg2
import json
import itertools
import re
fake = Faker()

            #######CREATE USERS, ADD TO USERS TABLE IN POSTGRES#######
                                    #AND#
            #####CREATE AND POPULATE USERS COLLECTION IN MONGODB#####

number_of_records=100

def randomString(stringLength=2):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def random_with_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

emailaddresses = []
for i in range(0, number_of_records):
    emailaddresses.append(str(fake.email()))

first_names = []
for i in range(0, number_of_records):
    first_names.append(str(names.get_first_name()))

last_names = []
for i in range(0, number_of_records):
    last_names.append(str(names.get_last_name()))

list_of_phonenumbers = []
for phonenumbers in range(0,number_of_records):
    list_of_phonenumbers.append(random_with_n_digits(10))

physical_addresses = []
for i in range(0, number_of_records):
    physical_addresses.append(str(fake.address()))

Address_Line_1 =[]
for i in physical_addresses:
    Address_Line_1.append(str(i.split('\n')[0]))

Address_Line_2 = []
for i in range(0,number_of_records):
    random_four = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    Address_Line_2.append(str(random_four))

list_of_cities = []
for states in range(0,number_of_records):
    list_of_cities.append(str(randomString(stringLength=7)))

list_of_states = []
for states in range(0,number_of_records):
    list_of_states.append(str(randomString(stringLength=2)))

list_of_zipcodes = []
for zipcodes in range(0,number_of_records):
    list_of_zipcodes.append(random_with_n_digits(5))
user_ids_mongo = []
user_string = 'userid_'
for u in range(0, number_of_records):
    mongo_user_id = user_string+str(u)
    user_ids_mongo.append(mongo_user_id)

users_js = open(r"C:\Users\User\nosql-db\docker\mongodb\mongodb\examples\userinsert.js", "w")

mongo_user_insert_statement = 'db.Users.insert({'

for (a, b, c, d, e, f, g, h, i, j) in zip(user_ids_mongo, emailaddresses, first_names, last_names, list_of_phonenumbers, Address_Line_1, Address_Line_2, list_of_cities, list_of_states, list_of_zipcodes):
    mongo_user_insert=mongo_user_insert_statement+'_id: ' + '"' + str(a) + '"' + ', ' + 'Email_Address: ' + '"' + str(b) + '"' + ', ' + 'First_Name: ' + '"' + str(c) + '"' + ', ' + 'Last_Name: ' + '"' + str(d) + '"' + ', '  + 'Phone_Number: ' + '"' + str(e) + '"' + ', ' + 'Address_Line_1: ' + '"' + str(f) + '"' + ', ' + 'Address_Line_2: ' + '"' + str(g) + '"' + ', ' + 'City: ' + '"' + str(h) + '"' + ', ' + 'State: ' + '"' + str(i) + '"' + ', '+ 'Zip: ' + '"' + str(j) + '"' + '})'
    print(mongo_user_insert, file = users_js)

users_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\usersinsert.sql", "w")

user_insert_statement = 'INSERT INTO Users (Email_Address, First_Name, Last_Name, Phone_Number, Address_Line_1, Address_Line_2, City, State, Zip) VALUES '


user_traits = list(zip(emailaddresses, first_names, last_names, list_of_phonenumbers, Address_Line_1,Address_Line_2, list_of_cities, list_of_states, list_of_zipcodes))
user_statement = ''
for elements in user_traits:
    user_statement = user_insert_statement+str(elements)+';'
    print(user_statement, file = users_sql)
#
#
#         ######CREATE INGREDIENTS, ADD TO INVENTORY TABLE IN POSTGRES#######
#                                     #AND#
#             #####CREATE AND POPULATE INVENTORY COLLECTION IN MONGODB#####
#
Ingredients_Name = ['cheese', 'flour', 'yeast', 'pepperoni', 'peppers', 'artichokes',
'tomato sauce', 'sausage', 'olives', 'basil', 'mushrooms', 'prosciutto', 'spam',
'gouda', 'salt', 'pepper', 'garlic', 'beef', 'chicken', 'ranch', 'bacon', 'pineapple',
'oil', 'parmesian', 'oregano' ]

Ingredients_Descriptions = []
for ingredient in Ingredients_Name:
    ingredient_desc = ingredient + ' imported weekly from Italy'
    Ingredients_Descriptions.append(ingredient_desc)

Quantities = []
for i in range(0,25):
    Quantities.append(random.randrange(1000000, 2000000, 1))

inv_ids_mongo = []
inv_mongo_string = 'inv_'
for u in range(0, 25):
    mongo_inv_id = inv_mongo_string+str(u)
    inv_ids_mongo.append(mongo_inv_id)

mongo_inventory_insert_statement = 'db.Inventory.insert({'

inventory_js = open(r"C:\Users\User\nosql-db\docker\mongodb\mongodb\examples\NEWinventoryinsert.js", "w")
for (a, b, c, d) in zip(inv_ids_mongo, Ingredients_Name, Ingredients_Descriptions, Quantities):
    mongo_inventory_insert=mongo_inventory_insert_statement+'_id: ' + '"' + str(a) + '"' + ', ' + 'Ingredient_Name: ' + '"' + str(b) + '"' + ', ' + 'Ingredient_Description: ' + '"' + str(c) + '"' + ', ' + 'Quantity : ' + str(d) + '})'
    print(mongo_inventory_insert, file = inventory_js)

Inventory_zip = list(zip(Ingredients_Name,Ingredients_Descriptions,Quantities))

inventory_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\inventoryinsert.sql", "w")

inventory_insert_statement = 'INSERT INTO Inventory (Ingredient_Name, Description, Quantity) VALUES '

inventory_statement = ''
for elements in Inventory_zip:
    inventory_statement = inventory_insert_statement+str(elements)+';'
    print(inventory_statement, file = inventory_sql)

    ######CREATE RECIPES, ADD TO RECIPES TABLE IN POSTGRES#######

Recipe_Names = ['pepperoni pizza', 'sausage pizza', 'ham pizza', 'meatball pizza', 'olive pizza',
'green pizza', 'red pizza', 'onion pizza', 'hawaiian pizza', 'cheese pizza',
'italian pizza', 'french pizza', 'german pizza', 'burger pizza', 'veggie pizza', 'grinder pizza',
'neopolitan pizza', 'spam pizza', 'avocado pizza', 'birthday pizza', 'special pizza',
'works pizza', 'gouda pizza', 'garlic pizza', 'victory pizza']
Recipe_Descriptions = []
for recipes in Recipe_Names:
    a,b = recipes.split()
    descriptions = b + ' with ' + a +' on top of it'
    Recipe_Descriptions.append(descriptions)

Recipe_Instructions = []
for recipes in Recipe_Names:
    a,b = recipes.split()
    instructions = '{slice ' + a + ',' + ' then place on top of ' + b + ',' + ' then bake}'
    Recipe_Instructions.append(instructions)

Recipe_zip = list(zip(Recipe_Names,Recipe_Descriptions,Recipe_Instructions))

recipe_insert_statement = 'INSERT INTO Recipes (Recipe_Name, Description, Instructions) VALUES '

recipes_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\recipesinsert.sql", "w")

recipe_statement = ''
for elements in Recipe_zip:
    recipe_statement = recipe_insert_statement+str(elements)+';'
    print(recipe_statement, file = recipes_sql)

    ####GENERATE VALUES TO BE INSERTED INTO Inventory_Recipe_Relation####

Recipe_ID_num = []
Ingredient_ID_num = []
Inventory_Quantity = []
i=1

while i < 25:
    Recipe_ID_num.append([i]*4)
    i+=1

Unpack_Recipe_Num = [item for sublist in Recipe_ID_num for item in sublist]


j=1
numbers = list(range(1,25))
while j < 6:
    Ingredient_ID_num.append(numbers)
    j+=1

Unpack_Ingredient_Num = [item for sublist in Ingredient_ID_num for item in sublist]

for k in range(1,101):
    Inventory_Quantity.append(random.randint(1, 35))

Inv_Recipe_dict = {
'Recipe_ID': Unpack_Recipe_Num,
'Ingredient_ID': Unpack_Ingredient_Num,
'Inventory_Quantity': Inventory_Quantity
}

my_three_numbers = list(zip(Unpack_Recipe_Num, Unpack_Ingredient_Num, Inventory_Quantity))

recipe_inv_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\recipe_inv_relation_insert.sql", "w")

recipe_inv_insert_statement = 'INSERT INTO Inventory_Recipe_Relation (Ingredient_ID, Recipe_ID, Quantity_Needed) VALUES '

recipe_inv_statement = ''
for elements in my_three_numbers:
    recipe_inv_statement = recipe_inv_insert_statement+str(elements)+';'
    print(recipe_inv_statement, file = recipe_inv_sql)


####### CREATE AND POPULATE RECIPES COLLECTION IN MONGODB ########

random_ingredient_quantites = []
for k in range(1,101):
    random_ingredient_quantites.append(random.randint(1, 35))

ingredients_in_a_recipe = []
for elements in inv_ids_mongo:
    ingredients_in_a_recipe.append([elements]*4)

l2 = [([x] if isinstance(x,str) else x) for x in ingredients_in_a_recipe]
Unpacked_ingredients_in_a_recipe=list(itertools.chain(*l2))
random.shuffle(Unpacked_ingredients_in_a_recipe)

empty_list = []
empty_list1 = []
empty_list2 = []
for element, k in zip(Unpacked_ingredients_in_a_recipe, random_ingredient_quantites):
    empty_list.append('{name: ' + '"' + element + '"' + ',' 'quantity: ' + str(k) + '}')
    empty_list1.append(element)
    empty_list2.append(k)

new_list1 = [empty_list1[i:i+4] for i in range(0, len(empty_list1), 4)]
# print(new_list1)
new_list2 = [empty_list2[i:i+4] for i in range(0, len(empty_list2), 4)]
# print(new_list2)

recipe_ids_mongo = []
rec_mongo_string = 'rec_'
for u in range(0, 25):
    mongo_rec_id = rec_mongo_string+str(u)
    recipe_ids_mongo.append(mongo_rec_id)

Mongo_Recipe_Instructions = []
for recipes in Recipe_Names:
    a,b = recipes.split()
    instructions = 'slice ' + a + ',' + ' then place on top of ' + b + ',' + ' then bake'
    Mongo_Recipe_Instructions.append(instructions)

recipe_js = open(r"C:\Users\User\nosql-db\docker\mongodb\mongodb\examples\NEWrecipeinsert1.js", "w")

mongo_recipe_insert_statement = 'db.Recipes.insert({'
for (a, b, c, d, e, f) in zip(recipe_ids_mongo, Recipe_Names, Recipe_Descriptions, new_list1, new_list2, Mongo_Recipe_Instructions):
    mongo_recipe_insert=mongo_recipe_insert_statement+'_id: ' + '"' + str(a) + '"' + ', ' + 'Recipe_Name: ' + '"' + str(b) + '"' + ', ' + 'Recipe_Description: ' + '"' + str(c) + '"' + ', ' + 'Ingredients : ' + str(d) + '' + ', ' + 'Quantities: ' + str(e) + '' + ', ' + 'Recipe_Instructions : ' + '"' + str(f) + '"' + '})'
    print(mongo_recipe_insert, file = recipe_js)
