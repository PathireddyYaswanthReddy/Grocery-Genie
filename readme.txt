In order to run the project,

Open terminal and go to the base directory of the project.

Install and activate the virtual environment.

Now run the command "pip install -r requirements.txt" in the terminal, this command will install all the requirements required to run the flask app.

Then run the command "python3 store.py" to run/activate the flask server.

Now open a new terminal,make pwd as the base-folder of the project and follow the below steps.

Now make "grocery-store" as your present working directory.

Then run the command "npm install" to install node modules.

Now run the command "npm run dev" to run the server for the Vue.js.

In order to run redis ,run the command : "redis-server" in a new terminal.

In order to run celery workers,
Run these commands in two different terminals:

"celery -A store.celery worker -l info"

"celery -A store.celery beat --max-interval 1 -l info".


Now Open link "http://localhost:5173" in a browser to see the website.