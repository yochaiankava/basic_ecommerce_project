# Basic E-Commerce Website

This is a basic e-commerce website built as a starting point for an online store. The project aims to provide fundamental functionality for showcasing products and enabling customers to make purchases.

## Features

- Display a catalog of products with details such as name, price, and image.
- Allow customers to add products to their shopping cart.
- Provide for customers to review and confirm their orders & a checkout process that close the purchase & save to DB.
- Provide for customers to review their purchases history.
- Handle user authentication for creating accounts and logging in.
- Admin panel for managing products, orders, and customer information.

## Getting Started

1. Clone the repository: `git clone https://github.com/yochaiankava/basic_ecommerce_project.git`
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` 
4. Install dependencies: `pip install -r requirements.txt`
5. Apply database migrations: `python manage.py migrate`
6. Create a superuser for accessing the admin panel: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## Usage

1. Access the admin panel at `http://localhost:8000/admin` and log in using the superuser credentials.
2. Add products through the admin panel.
3. Browse the products on the main site and add them to the cart.
4. Proceed to the checkout process and confirm the order.
5. Review order history and customer information through the admin panel.

## Admin Details:

   user name-yochai
   password-1234

## Special Button Actions:

   checkout button-will finish purchase & will change purchase cart status to "closed"     

## Render URL-

   https://meshek-ankave-basic-ecommerce.onrender.com
