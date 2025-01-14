# StockTracker
 Warehouse Management System

## Overview
The **StockTracker** is a Django-based web application designed to help users efficiently manage warehouse inventory. It includes features such as category and item management, low-stock and expiry notifications, bulk editing, and visual insights through charts. 

---

## Features
### 1. **Category Management**
- Create, view, update, and delete categories.
- Organize items under specific categories.

### 2. **Item Management**
- Add, update, and delete items with attributes like:
  - Name
  - Location
  - Quantity
  - Expiry date
  - Description
- Bulk update item quantities.

### 3. **Notifications**
- Low-stock alerts via email when item quantity drops below a threshold (default: 5).
- Alerts for items expiring within one month.

### 4. **Search and Detail View**
- Search items by name.
- View detailed information about items.

### 5. **Visual Insights**
- Interactive bar charts powered by Chart.js for stock visualization.
- Dynamic bar colors to represent stock levels (low, medium, high).

---

## Project Structure
```
warehouse-management-system/
│
├── warehouses/                # Main app
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   ├── views.py               # View logic
│   ├── models.py              # Database models
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin site customization
│   ├── apps.py                # App configuration
│
├── StockTracker/              # Project directory
│   ├── urls.py                # URL routing for the project
│   ├── settings.py            # Project settings
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

```

## Installation

### Prerequisites
- Python 3.8 or later
- Django 5.1.4
- A virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Sajjadke92/StockTracker.git
   cd warehouse-management-system

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

5. Install dependencies:
   ```bash
   pip install -r requirements.txt

7. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

9. Start the development server:
   ```bash
   python manage.py runserver
   
11. Access the application in your browser at http://127.0.0.1:8000.

   


