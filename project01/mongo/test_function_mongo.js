
function take_order(user_id, recipe_id) {
  var time_of_order = ISODate();
  // printjson  ('HelloWorld4');

  var rec = db.Recipes.findOne({"_id": recipe_id });
  if(rec ==null) {
    return 'that recipe does not exist';
  }

  var ingredients_for_recipe = { "Ingredients": rec.Ingredients, "Quantity":db.Recipes.findOne({"_id": recipe_id }, {_id:0, Quantities:1})};
  // printjson  ('-----------------------------------------------------');
  // printjson(ingredients_for_recipe);
  // printjson  ('-----------------------------------------------------');

//  for(var i in ingredients_for_recipe.Ingredients){

  for (var i = 0; i < ingredients_for_recipe.Ingredients.length; i++){
    // printjson  ('-----------------------------------------------------');
    // printjson  (ingredients_for_recipe.Ingredients[i]);
    // printjson  (ingredients_for_recipe.Quantity.Quantities[i]);
    // printjson  (db.Inventory.findOne({"_id": ingredients_for_recipe.Ingredients[i]}).Quantity);
    // printjson  ('-----------------------------------------------------');

    var onHand = db.Inventory.findOne({"_id": ingredients_for_recipe.Ingredients[i]}).Quantity;
    var needQuant  =  ingredients_for_recipe.Quantity.Quantities[i];

    if(onHand == null || onHand < needQuant){
      return 'not enough ingredients for order';
    }
    else{
      // var existing_ingr_count = db.Inventory.findOne({"_id": i).Quantity;
      // var current_quantity = i.Quantity;
      db.Inventory.updateOne({"_id": ingredients_for_recipe.Ingredients[i]},{$set:{"Quantity" : onHand - needQuant}});

    }

  }
  db.Orders.insertOne({user_id: user_id, recipe_id: recipe_id, order_time: time_of_order});
}
//TO ADD ORDERS DATA TO COLLECTION
{
  for (var i = 0; i < 25000; i++)
  {
    var time_of_order = ISODate();
    var user_id   = 'userid_' + Math.floor(Math.random() * 1000);
    var recipe_id = 'rec_'    + Math.floor(Math.random() * 25);
    db.Orders.insertOne({user_id: user_id, recipe_id: recipe_id, order_time: time_of_order});
    //printjson(user_id);
    //printjson(recipe_id);
  }
}
