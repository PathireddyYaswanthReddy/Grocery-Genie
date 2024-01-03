# Grocery-Genie

## Embark on a revolutionary grocery shopping experience 🛒✨ with our multi-user app, featuring a seamless collaboration between admins, store managers, and users. Effortlessly fill your cart with a diverse array of products spanning multiple sections. Empower store managers to curate their inventory by adding products and proposing new sections, all while our vigilant admin oversees and manages category requests and store manager signups. Elevate your grocery shopping game with our intuitive and collaborative platform!

# Technologies Used
  ⭐️ <strong>Flask Web Framework</strong><br>
  ⭐️ <strong>Vue.js - JavaScript framework</strong><br>
  ⭐️ <strong>Redis</strong><br>
  ⭐️ <strong>Celery</strong><br>
  ⭐️ <strong>Jijnja2 Template engine</strong><br>
  ⭐️ <strong>Bootstrap</strong><br>

# Installation
  ⭐️ Clone the repository into your local machine.<br>
  ⭐️ Navigate to the project directory.<br>
  ⭐️ Create a virtual environment.<br>
  ⭐️ Activate the virtual environment.<br>
  ⭐️ Install the project dependencies by using the following command "pip install -r requirements.txt".<br>
  ⭐️ Initiate the flask server by running the following command "python3 store.py".<br>
  ⭐️ Open a new terminal and navigate to the grocery-store directory which is located inside the root directory.<br>
  ⭐️ Install the node modules by running the following command "npm install".<br>
  🚀 Launch the application by executing the command "npm run dev".<br>
  ⭐️ To execute the celery jobs initiate the redis-server and run the following commands.<br>
  &nbsp;&nbsp;&nbsp;&nbsp;>"celery -A store.celery worker -l info".<br>
  &nbsp;&nbsp;&nbsp;&nbsp;>"celery -A store.celery beat --max-interval 1 -l info".<br>
  🌐 Visit http://localhost:5173/login in your web browser.<br>

# Appplication Demo

## 🚀 User's Landing page<br>
![](https://github.com/PathireddyYaswanthReddy/Grocery-Genie/blob/main/grocery-genie%20screenshots/User%20homepage.png)<br>

## 🚀 Admin Homepage<br>
![](https://github.com/PathireddyYaswanthReddy/Grocery-Genie/blob/main/grocery-genie%20screenshots/admin%20home%20page.png)<br>

## 🚀 StoreManager's Homepage<br>
![](https://github.com/PathireddyYaswanthReddy/Grocery-Genie/blob/main/grocery-genie%20screenshots/SM%20Homepage.png)<br>

