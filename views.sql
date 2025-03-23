-- View for displaying USER info

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
FROM User;

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
  COUNT(c.WorkoutID) AS WorkoutCountTotal,
  SUM(w.Duration) AS TotalDuration
FROM Routine r
LEFT JOIN ComposedOf c ON r.RoutineID = c.RoutineID
LEFT JOIN Workout w ON c.WorkoutID = w.WorkoutID
GROUP BY r.RoutineID, r.RoutineName, r.UserID;
