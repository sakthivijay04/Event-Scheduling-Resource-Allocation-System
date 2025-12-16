# 📅 Event Scheduling & Resource Allocation System
**Project Overview**

This project is a Flask-based web application designed to manage events and efficiently allocate shared resources such as rooms, instructors, and equipment.

The system helps users:

Create and manage events with start and end times

Add reusable resources

Allocate one or more resources to events

Prevent double-booking of resources using conflict detection

View resource utilization reports for better planning

The application is intentionally kept simple, clean, and readable, making it suitable for interview demonstrations, academic projects, and early-stage production use.

 # 🛠️ Tech Stack
**Layer**	        **Technology**
Backend	         Python (Flask)
Database	         SQLite
ORM	              SQLAlchemy
Frontend	      HTML, Bootstrap 5
Templating	       Jinja2
Version          Control	Git

# 🗄️ Database Design

The application uses a relational database design with three main tables:

**1. Event**

Stores event details such as title and schedule.

Key fields:

event_id (Primary Key)

title

start_time

end_time

description

**2. Resource**

Represents reusable assets like rooms, instructors, or equipment.

Key fields:

resource_id (Primary Key)

resource_name

resource_type

**3. EventResourceAllocation (Junction Table)**

Handles the many-to-many relationship between events and resources.

Why this table exists:

One event can use multiple resources

One resource can be reused across multiple events

A junction table ensures clean normalization and flexibility

Key fields:

allocation_id (Primary Key)

event_id (Foreign Key → Event)

resource_id (Foreign Key → Resource)

# 🚫 Conflict Detection Logic

To prevent double-booking of resources, the system checks for time overlaps before saving an allocation.

Core Rule Used
**(existing_start < new_end) AND (new_start < existing_end)**

What this logic ensures:

❌ Same start time → blocked

❌ Same end time → blocked

❌ Partial overlap → blocked

❌ Nested overlap → blocked

✅ Back-to-back events (end_time == start_time) → allowed

This approach is:

Simple

Reliable

Widely used in real-world scheduling systems

# 📊 Resource Utilisation Report

The system includes a Resource Utilisation Report that allows users to:

Select a date range

View total hours each resource is used within that range

See upcoming future bookings for each resource

How utilisation is calculated:

Only the overlapping portion of an event within the selected date range is counted

This prevents over-counting and ensures accurate reporting

# ▶️ Steps to Run the Project Locally
**1. Clone the Repository**
git clone <repository-url>
cd event_scheduler

**2. Create Virtual Environment (Optional but Recommended)**
python -m venv venv
venv\Scripts\activate   # Windows

**3. Install Dependencies**
pip install flask flask-sqlalchemy

**4. Create the Database**
python
>>> from app import app
>>> from extensions import db
>>> with app.app_context():
...     db.create_all()
>>> exit()

**5. Run the Application**
python app.py

**6. Open in Browser**
http://127.0.0.1:5000/events


# 📸 Screenshots 

Screenshots can be added here for visual reference.

**Event creation page**
<img width="954" height="846" alt="Screenshot 2025-12-16 203704" src="https://github.com/user-attachments/assets/e1795455-31dd-4c28-b2c1-5e34f6eb1425" />

**Resource creation page**
<img width="961" height="804" alt="Screenshot 2025-12-16 203728" src="https://github.com/user-attachments/assets/4839975b-433d-4d17-a10d-b144ced7dc63" />

**Resource management page**
<img width="961" height="560" alt="Screenshot 2025-12-16 203739" src="https://github.com/user-attachments/assets/ad68ab3b-f9ac-4b9d-8658-dce5a6ebc6bf" />

**Resource allocation page**
<img width="959" height="671" alt="Screenshot 2025-12-16 203750" src="https://github.com/user-attachments/assets/97c10455-8fbe-425d-8d88-c75b8169f7a2" />

**Resource utilisation report**
<img width="948" height="711" alt="Screenshot 2025-12-16 203830" src="https://github.com/user-attachments/assets/ffffd4b4-8abb-4317-9d7f-a1de6eb6e341" />








 
# 🎥 Screen-Recorded Demo

A short screen recording explaining the flow of the application.


https://github.com/user-attachments/assets/5a4ada88-1890-4c55-aa8e-efa7ebd0c4a6

