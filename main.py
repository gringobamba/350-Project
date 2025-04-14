import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt


# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
bcrypt = Bcrypt(app)


# ------------------------ BEGIN FUNCTIONS ------------------------ #
# Function to retrieve DB connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    return conn

# Get all items from the "items" table of the db
def get_all_items():
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT name, quantity FROM items"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    return result

# Get all info on the user via the user VIEW
def get_user_data(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_view WHERE UserID = %s", (user_id,))

    result = cursor.fetchone()
    conn.close()
    return result

def sql_script_execution(file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for result in cursor.execute(sql_script, multi=True):
            pass
        conn.commit()
        print(f"successfully executed script: {file_path}")
    except Exception as e:
        print(f"error executing script {file_path}: {e}")
    finally:
        cursor.close()
        conn.close()
# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------
# forces the user to login if they navigate to a secure page without a session
@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

# HOMEPAGE ROUTE
@app.route("/", methods=["GET"])
def home():
    # Checks if user has a session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    user_data = get_user_data(user_id) # Call defined function to get all the current user's data
    return render_template("index.html", user=user_data) # Return the user's homepage
    
# REGISTRATION ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST': # if the user submits the registration form
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        dob = request.form['dob']
        height = request.form['height']
        weight = request.form['weight']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user already exists
        cursor.execute("SELECT * FROM AppUser WHERE UserEmail = %s", (email,))
        existing = cursor.fetchone()
        if existing:
            error = 'Email already in use.'
        else:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute("""
                INSERT INTO AppUser (UserFName, UserLName, UserEmail, UserPass, Gender, DoB, Height, Weight)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, email, hashed_pw, gender, dob, height, weight))
            conn.commit()
            session['user_id'] = cursor.lastrowid
            return redirect(url_for('home'))

        cursor.close()
        conn.close()

    return render_template('register.html', error=error)

# LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST': # If user submits the login form
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM AppUser WHERE UserEmail = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['UserPass'], password):
            session['user_id'] = user['UserID']
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials'
    
    return render_template('login.html', error=error)

# LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# INITIAL POPULATION OF THE DATABASE. REQUIRES THAT THE DB WAS CREATED MANUALLY FIRST.
@app.route("/init-db", methods=["GET"])
def init_db():
    try:
        sql_script_execution("SQL_structure_1.sql")
        sql_script_execution("insert_script_1.sql")
        sql_script_execution("delete_script_1.sql")
        sql_script_execution("views.sql")
        flash(f"initialization of database succeeded", "success")
    except Exception as e:
        flash(f"initialization of database failed: {str(e)}", "error")
    return redirect(url_for("home"))

@app.route("/add_workout", methods=["GET"])
def add_workout():
    user_id = session.get("user_id")
    routines = get_user_routines(user_id)
    return render_template("add_workout.html", routines=routines)

@app.route("/save_workout", methods=["POST"])
def save_workout():
    # Retrieve form data
    workout_type = request.form.get("workout_type")
    duration = float(request.form.get("duration"))
    reps = request.form.get("reps")
    weight_lifted = request.form.get("weight_lifted")
    routine_id = request.form.get("routine_id")  # Routine selection from the form

    reps = int(reps) if reps else None
    weight_lifted = float(weight_lifted) if weight_lifted else None

    # Insert into Workout table
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO Workout (WorkoutType, Duration, Reps, WeightLifted)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (workout_type, duration, reps, weight_lifted))
    conn.commit()
    workout_id = cursor.lastrowid  # Retrieve the WorkoutID for the inserted workout

    # Links workout with routine
    if routine_id:
        insert_composedof_query = """
            INSERT INTO ComposedOf (RoutineID, WorkoutID)
            VALUES (%s, %s)
        """
        cursor.execute(insert_composedof_query, (routine_id, workout_id))
        conn.commit()

    cursor.close()
    conn.close()
    
    flash("Workout added successfully", "success")
    return redirect(url_for('home'))

@app.route("/add_routine", methods=["GET"])
def add_routine():
    # Render the routine creation form
    return render_template("add_routine.html")

@app.route("/save_routine", methods=["POST"])
def save_routine():
    # Retrieve form data
    routine_name = request.form.get("routine_name")
    day_of_week = request.form.get("day_of_week")
    
    # Make sure user is logged in 
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in.", "error")
        return redirect(url_for("login"))
    
    # Insert the new routine into the Routine table
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO Routine (RoutineName, DayOfWeek, UserID)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (routine_name, day_of_week, user_id))
    conn.commit()
    routine_id = cursor.lastrowid  
    cursor.close()
    conn.close()
    
    flash("Routine created successfully.", "success")
    return redirect(url_for("home"))

@app.route("/view_workouts", methods=["GET"])
def view_workouts():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view workouts.", "error")
        return redirect(url_for("login"))
    workouts = get_all_workouts(user_id)
    return render_template("view_workouts.html", workouts=workouts)




# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
    #this can also be the place where we have the sql_script_execution methods.
    #it would allow it to just do it on start up