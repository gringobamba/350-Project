import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


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


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST
@app.route("/", methods=["GET"])
def home():
    items = get_all_items() # Call defined function to get all items
    return render_template("index.html", items=items) # Return the page to be rendered

# EXAMPLE OF POST REQUEST
@app.route("/new-item", methods=["POST"])
def add_item():
    try:
        # Get items from the form
        data = request.form
        item_name = data["name"] # This is defined in the input element of the HTML form on index.html
        item_quantity = data["quantity"] # This is defined in the input element of the HTML form on index.html

        # TODO: Insert this data into the database
        
        # Send message to page. There is code in index.html that checks for these messages
        flash("Item added successfully", "success")
        # Redirect to home. This works because the home route is named home in this file
        return redirect(url_for("home"))

    # If an error occurs, this code block will be called
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error") # Send the error message to the web page
        return redirect(url_for("home")) # Redirect to home
    

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

# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
    #this can also be the place where we have the sql_script_execution methods.
    #it would allow it to just do it on start up