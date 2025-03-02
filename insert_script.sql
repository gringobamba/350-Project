USE project_350;

-- Insert dummy data into User table
INSERT INTO User (UserFName, UserLName, Weight, Height, UserEmail, UserPass, Gender, DoB)
VALUES ('John', 'Doe', 70.5, 175.3, 'john.doe@example.com', 'password123', 'Male', '1990-01-01');

-- Insert dummy data into Workout table
INSERT INTO Workout (Duration, WorkoutType, Reps, WeightLifted)
VALUES (60, 'Cardio', NULL, NULL);

-- Insert dummy data into Meal table
INSERT INTO Meal (DateEaten, MealName, UserID)
VALUES ('2025-02-28', 'Breakfast', 1);

-- Insert dummy data into Routine table
INSERT INTO Routine (RoutineName, DayOfWeek, UserID)
VALUES ('Morning Routine', 'Monday', 1);

-- Insert dummy data into Drink table
INSERT INTO Drink (DrinkType, Amount, DrinkCalDensity, MealID)
VALUES ('Orange Juice', 250, 0.45, 1);

-- Insert dummy data into Ingredient table
INSERT INTO Ingredient (IngredType, IngredWeight, FoodCalDensity, MealID)
VALUES ('Oats', 100, 0.38, 1);

-- Insert dummy data into ComposedOf table
INSERT INTO ComposedOf (RoutineID, WorkoutID)
VALUES (1, 1);
