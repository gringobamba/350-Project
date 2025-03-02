USE project_350;

-- Delete data from ComposedOf table
DELETE FROM ComposedOf WHERE RoutineID = 1 AND WorkoutID = 1;

-- Delete data from Ingredient table
DELETE FROM Ingredient WHERE IngredID = 1;

-- Delete data from Drink table
DELETE FROM Drink WHERE DrinkID = 1;

-- Delete data from Routine table
DELETE FROM Routine WHERE RoutineID = 1;

-- Delete data from Meal table
DELETE FROM Meal WHERE MealID = 1;

-- Delete data from Workout table
DELETE FROM Workout WHERE WorkoutID = 1;

-- Delete data from User table
DELETE FROM User WHERE UserID = 1;
