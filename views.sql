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
