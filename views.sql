USE project_350;

-- View for displaying AppUSER info

CREATE VIEW user_view AS
SELECT 
  UserID, 
  UserFName, 
  UserLName, 
  UserEmail, 
  Gender, 
  DoB, 
  Height, 
  Weight
FROM AppUser;

-- View for displaying WORKOUT info

CREATE VIEW workout_view AS
SELECT 
  w.WorkoutID,
  c.RoutineID,
  r.RoutineName,
  r.DayOfWeek,
  r.UserID,
  w.WorkoutType,
  w.Duration,
  w.Reps,
  w.WeightLifted
FROM Workout w
JOIN ComposedOf c ON w.WorkoutID = c.WorkoutID
JOIN Routine r ON c.RoutineID = r.RoutineID;

-- View for displaying WORKOUT ROUTINE info

CREATE VIEW routine_view AS
SELECT 
  r.RoutineID,
  r.RoutineName,
  r.UserID,
  -- Num of workouts associated with routine
  COUNT(c.WorkoutID) AS WorkoutCountTotal,
  -- Total time spent on workouts within the routine
  SUM(w.Duration) AS TotalDuration
FROM Routine r
LEFT JOIN ComposedOf c ON r.RoutineID = c.RoutineID
LEFT JOIN Workout w ON c.WorkoutID = w.WorkoutID
GROUP BY r.RoutineID, r.RoutineName, r.UserID;

-- View for displaying MEAL info

CREATE VIEW meal_view AS
SELECT 
  m.MealID,
  m.MealName,
  m.DateEaten,
  m.UserID,
  -- Calculates total calories from ingredients and drinks
  SUM(i.IngredWeight * i.FoodCalDensity) AS TotalIngredientCalories,
  SUM(d.Amount * d.DrinkCalDensity) AS TotalDrinkCalories
FROM Meal m
LEFT JOIN Ingredient i ON m.MealID = i.MealID
LEFT JOIN Drink d ON m.MealID = d.MealID
GROUP BY m.MealID, m.MealName, m.DateEaten, m.UserID;

