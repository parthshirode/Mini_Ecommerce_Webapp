Mini Flask E-commerce Web Application
This is a dynamic, multi-user e-commerce web application built entirely in Python using the Flask framework. It simulates a real-world online store by managing all data—users, products, and orders—from a single Excel file (data.xlsx), leveraging the pandas library for in-memory data manipulation.

The application features a modern, responsive frontend with a "glassmorphism" design aesthetic, providing a visually appealing and intuitive user experience across all pages.

✨ Core Features
Role-Based User System: The application supports three distinct user roles with different permissions:

Customers: Can browse products, add items to a persistent shopping cart, manage their cart, and view their order history.

Sellers: Can log in to a dedicated dashboard to add, view, edit, and delete their own product listings.

Admins: Have full administrative access, including the ability to manage all users and products on the platform.

Dynamic Product Catalog: Instead of a static table, products are displayed in an engaging, card-based grid layout similar to modern e-commerce sites like Amazon and Flipkart.

Full Shopping Cart Functionality: A complete shopping cart system that allows users to add items, view their cart with subtotals, remove items, and "check out" to place an order.

Database-Free Operation: Utilizes pandas to read data from an Excel file at startup, effectively using DataFrames as an in-memory database. This makes the application lightweight, portable, and easy to set up.

Modern & Responsive Frontend: A consistent and stylish UI/UX built with pure CSS. The design is fully responsive and looks great on devices of all sizes.

Secure Authentication: Implements robust login, registration, and session management to protect user accounts and ensure a secure experience.

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.x

Git (for cloning the repository)

1. Clone the Repository
First, clone this repository to your local machine.

git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

(Replace YOUR_USERNAME and YOUR_REPOSITORY_NAME with your actual GitHub details)

2. Install Dependencies
All the required Python packages are listed in the requirements.txt file. Install them in one command using pip.

pip install -r requirements.txt

3. Add the Data File
Place your data.xlsx file in the main root directory of the project. This Excel file must contain three sheets named exactly:

Users

Products

Orders

4. Run the Application
Start the Flask development server by running the app.py file.

python app.py

The application will now be running. Open your web browser and navigate to http://127.0.0.1:5000 to start using the app.

📂 Project Structure
The project is organized into a modular and easy-to-understand structure using Flask Blueprints.

ECOMMERCE_APP/
│── app.py # Main entry point
│── requirements.txt # Dependencies
│── data_new.xlsx # Excel file (if using Excel DB)
│── .gitignore
│
├── routes/ # All routes organized
│ ├── users/ # Customer/Seller/Admin routes
│ │ └── users.py
│ ├── products/ # Product related routes
│ │ └── products.py
│ └── orders/ # Order management
│ └── orders.py
│
├── templates/ # HTML files
│ ├── users/
│ │ ├── register.html
│ │ ├── login.html
│ │ └── dashboard.html
│ ├── products/
│ │ └── products.html
│ └── orders/
| │ ├── cart.html
│ └── orders.html
│         
└── templates/          # Contains all the HTML files for the frontend
    ├── base.html       # The master template with the main layout and navbar
    ├── users/          # User-related templates
    ├── products/       # Product-related templates
    └── orders/         # Order and cart templates
