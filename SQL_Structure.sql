CREATE TABLE User
(
  UserID INT NOT NULL,
  UserFName INT NOT NULL,
  UserLName INT NOT NULL,
  Weight INT,
  Height INT,
  UserEmail INT NOT NULL,
  UserPass INT NOT NULL,
  Gender INT NOT NULL,
  DoB INT,
  PRIMARY KEY (UserID)
);

CREATE TABLE Workout
(
  Duration INT,
  WorkoutType INT NOT NULL,
  Reps INT,
  WeightLifted INT,
  WorkoutID INT NOT NULL,
  PRIMARY KEY (WorkoutID)
);

CREATE TABLE Meal
(
  MealID INT NOT NULL,
  DateEaten INT NOT NULL,
  MealName INT NOT NULL,
  UserID INT NOT NULL,
  PRIMARY KEY (MealID),
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Routine
(
  RoutineName INT NOT NULL,
  DayOfWeek INT NOT NULL,
  RoutineID INT NOT NULL,
  UserID INT NOT NULL,
  PRIMARY KEY (RoutineID),
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Drink
(
  DrinkType INT NOT NULL,
  Amount INT NOT NULL,
  DrinkCalDensity INT NOT NULL,
  DrinkID INT NOT NULL,
  MealID INT NOT NULL,
  PRIMARY KEY (DrinkID),
  FOREIGN KEY (MealID) REFERENCES Meal(MealID)
);

CREATE TABLE Ingredient
(
  IngredType INT NOT NULL,
  IngredWeight INT NOT NULL,
  FoodCalDensity INT NOT NULL,
  IngredID INT NOT NULL,
  MealID INT NOT NULL,
  PRIMARY KEY (IngredID),
  FOREIGN KEY (MealID) REFERENCES Meal(MealID)
);

CREATE TABLE ComposedOf
(
  RoutineID INT NOT NULL,
  WorkoutID INT NOT NULL,
  PRIMARY KEY (RoutineID, WorkoutID),
  FOREIGN KEY (RoutineID) REFERENCES Routine(RoutineID),
  FOREIGN KEY (WorkoutID) REFERENCES Workout(WorkoutID)
);
