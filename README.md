 # 🛒 Amazon Clone - Django E-Commerce Project

Welcome to **Amazon Clone**, a **fully featured, professional e-commerce platform** built with **Django**. This project replicates the **core functionalities of a modern online store like Amazon**, delivering a smooth shopping experience with a sleek, dark-mode-ready interface.

---

## 🚀 Features

- 🔐 **User Authentication**
  - Secure login, registration, and logout using Django’s authentication system.

- 🛍️ **Product Listings**
  - Browse featured and recommended products with images, prices, and detailed descriptions.

- 🛒 **Cart Management**
  - Add/remove items, view cart totals, and persist cart data for logged-in users.

- 📦 **Order Placement**
  - Seamlessly place orders and track delivery status via a user-friendly navbar.

- 👤 **User Dashboard**
  - Personalized welcome screen, cart overview, and address management.

- 🛠️ **Admin Dashboard**
  - Add, edit, and delete products with a customized admin interface.

- 🗂️ **Product Categories** *(In Progress)*
  - Organize products into intuitive categories for easier navigation.

- 🔍 **Search Functionality** *(In Progress)*
  - Find your favorite products instantly with smart search.

- 🌟 **Ratings & Reviews** *(Planned)*
  - Let users share their experience through ratings and reviews.

- 💳 **Checkout Process**
  - A basic but extendable checkout system with scope for payment gateway integration.

- 📉 **Stock Management** *(Planned)*
  - Automatically track product stock and availability.

- 🤖 **Recommendations System** *(Optional ML Integration)*
  - Personalized product suggestions with fallback randomizer logic.

- 🌙 **Dark Mode Design**
  - Fully responsive layout with a modern **dark theme** for enhanced UX.

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django (Python) |
| Frontend | HTML • CSS • JavaScript • Bootstrap 5 |
| Database | SQLite (default), compatible with PostgreSQL/MySQL |
| Authentication | Django Authentication System |
| API Integration | OpenWeatherMap (for delivery weather updates) |

---

## 🚀 Deployment Ready

- 🟢 Heroku  
- 🟢 Render  
- 🟢 VPS / Custom Hosting

---

### 📌 Future Enhancements
- Payment Gateway Integration (Stripe/Razorpay)
- Product Filtering & Sorting
- Coupon/Discount System
- Wishlist Feature

 Project Structure

amazon_clone/
├── Procfile              # For Render deployment
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
├── amazon/               # Main Django project folder
│   ├── __init__.py
│   ├── settings.py       # Configuration (ALLOWED_HOSTS, static files, etc.)
│   ├── urls.py           # Project-level URL routing
│   ├── wsgi.py           # WSGI entry point
│   └── asgi.py           # ASGI entry point
├── shop/                 # Main app (e.g., 'shop' instead of 'app')
│   ├── __init__.py
│   ├── admin.py          # Admin panel configuration
│   ├── models.py         # Database models (User, Product, Cart, Order)
│   ├── views.py          # Logic for home, register, etc.
│   ├── forms.py          # Forms (e.g., SignUpForm)
│   ├── urls.py           # App-level URL routing
│   ├── migrations/       # Database migrations
│   └── templates/        # HTML templates
│       ├── base.html     # Base template with navbar
│       ├── home.html     # Home page with carousel and products
│       ├── register.html # Registration page
│       └── ...           # Other templates
├── static/               # Static files (CSS, JS, images)
│   └── images/           # Product and banner images
└── .gitignore            # Ignore unnecessary files

 Setup Instructions
Prerequisites
Python 3.12+

Git

OpenWeatherMap API Key (for weather feature)

Local Installation
Clone the Repository:
bash

git clone https://github.com/yourusername/amazon_clone.git
cd amazon_clone

Create a Virtual Environment:
bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install Dependencies:
bash

pip install -r requirements.txt

Configure Environment:
Copy amazon/settings.py and adjust:
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

Add your OpenWeatherMap API key in views.py.

Run Migrations:
bash

python manage.py makemigrations
python manage.py migrate

Create Superuser:
bash

python manage.py createsuperuser

Collect Static Files:
bash

python manage.py collectstatic

Start the Server:
bash

python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser.

 Deployment
Render Deployment
Install Gunicorn:
bash

pip install gunicorn
pip freeze > requirements.txt

Update Procfile:

web: gunicorn amazon.wsgi:application --bind 0.0.0.0:$PORT

Configure settings.py:
python

ALLOWED_HOSTS = ['*']  # Adjust for production
DEBUG = False
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

Push to GitHub and Deploy**:
Create a Render app, link your repo, and set:
Build Command: pip install -r requirements.txt && python manage.py migrate

Start Command: Matches Procfile

 Screenshots
Home Page

Registration

Home

Register

(Add screenshots by capturing your current home and register pages!)
 Roadmap
Add product categories and search

Implement full checkout with payment integration

Enhance stock management

Integrate ML-based recommendations

Add user reviews and ratings

 Contributing
Contributions are welcome! Fork the repo, create a branch, and submit a pull request with your changes.
Fork the project

Create your feature branch: git checkout -b feature/YourFeature

Commit changes: git commit -m "Add YourFeature"

Push to branch: git push origin feature/YourFeature

Open a pull request

 Contact
Author: Sayantan Mukherjee

Email: sayantanmukherjee000@gmail.com 

GitHub: meaow-stack

 Show Your Support
If you like this project, give it a star on GitHub! 
Improvements Made
Professional Layout: Used Markdown headers, emojis, and tables for a clean, engaging look.

Detailed Setup: Added step-by-step local and deployment instructions.

Feature Clarity: Listed all features with status (e.g., in progress, planned).

Structure: Updated to reflect your actual app name (shop) and added context.

Visuals: Placeholder for screenshots to showcase your dark-mode design.

Call to Action: Encouraged contributions and starring the repo.

Tech Stack: Highlighted key tools like Bootstrap and SQLite.

Next Steps
Replace "YOUR_OPENWEATHERMAP_API_KEY" in views.py and add it to your README setup instructions (e.g., as an environment variable).

Capture screenshots of your home.html and register.html and add them to static/images/.

Update the author and contact details with your info.

Push this to your GitHub repo:
bash

echo "# Amazon Clone - Django E-Commerce Project" > README.md
# Paste the content above into README.md
git add README.md
git commit -m "Update README with detailed project info"
git push origin main

![Screenshot 2025-03-18 173421](https://github.com/user-attachments/assets/a0925387-4e51-477e-a1f5-147e61223419)
![Screenshot 2025-03-18 173432](https://github.com/user-attachments/assets/aada59f0-eb47-46b8-bb8a-ceea678a77ad)
![Screenshot 2025-03-18 173439](https://github.com/user-attachments/assets/0247eb4c-2874-4431-a95d-069eb2805da4)
![Screenshot 2025-03-18 173448](https://github.com/user-attachments/assets/7f086963-425c-4bdd-9d18-bac10f515f67)
![Screenshot 2025-03-18 173453](https://github.com/user-attachments/assets/4d1d0f4a-4aa8-496e-a38b-87c1c9442f52)
![Screenshot 2025-03-18 173517](https://github.com/user-attachments/assets/4160d155-46e3-4e13-9a02-c7bf09e03019)
![Screenshot 2025-03-18 173525](https://github.com/user-attachments/assets/dcc57b67-aaf6-4711-8e57-1f38e1cbacfd)
![Screenshot 2025-03-18 173547](https://github.com/user-attachments/assets/706c61d5-0d47-41fd-941d-965dad483f9f)
![Screenshot 2025-03-18 173556](https://github.com/user-attachments/assets/6509553e-4b45-47e8-af99-cded5681190b)
![Screenshot 2025-03-18 173727](https://github.com/user-attachments/assets/3b66b08e-1192-4a92-a3e9-70674500b0d2)
![Screenshot 2025-03-18 173744](https://github.com/user-attachments/assets/bc904009-f6c5-42f5-9ba9-efd756204c9f)
when we use search it also shoes products as well as recommended products
![Screenshot 2025-03-18 174301](https://github.com/user-attachments/assets/b803400a-0f56-4b2e-843d-9f867b9e3527)
![Screenshot 2025-03-18 173744](https://github.com/user-attachments/assets/46b200da-9f06-4b9a-8a96-bb8825f12aa8)






