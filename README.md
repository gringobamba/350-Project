# Database Logic for a Fitness Tracker App

This is our repo for IT&C 350.

## How to connect to this repo on GitHub

*These instructions assume that you already have Git installed and are using a linux-based machine*

1. Navigate to the directory on your local machine that you'd like to clone the repository into. For example:
```cd /path/to/your/directory```
2. Clone the repository using:
```git clone https://github.com/gringobamba/350-Project.git```
3. Navigate into the cloned repository:
```cd 350-Project```

Now you are ready to make changes, create files, and use these scripts on your local machine!

## What's contained in this Repo
In this repo, you'll find useful files to setup the Fitness Tracker database and web application.

```static/css``` contains our CSS files.

```templates``` contains all of the html files for the Flask to dynamically render the app's routes.

```.env.example``` contains the environment variables needed to run the app. Change this to .env after cloning to your environment.

```.gitignore``` makes sure that you don't upload your actual .env to GitHub.

```SQL_structure.sql``` contains a basic script to initialize the database schema.

```delete_script.sql``` contains scripts to delete rows from each of the database's tables.

```insert_script``` contains scripts to insert rows into each of the database's tables.

```main.py``` contains all of the logic and routes that make the magic happen.

```views.sql``` contains a script that will create the views used by the app's routes.

## First Steps
After you've cloned the repo, there are a few steps before you can start up the app.

1. Install mySQL
2. Create your database (make sure to include your database name in the appropriate files like the .sql scripts and the .env file)
3. Run the sql scripts in your database to establish the schema and create the views.
4. Create the webuser in mySQL and give it permissions to SELECT, INSERT, DELETE, and UPDATE your database.

After you've completed these steps, you should be ready to start the app! (```python3 main.py```)