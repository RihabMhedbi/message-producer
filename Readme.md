# Running the Producer Project

## Prerequisites

Before running the project, ensure you have the following installed on your system:

- Python 3.8 or higher
- Pip (Python package installer)

## Setup Instructions

1. **Clone the Repository:**
   ```bash
    cd producer_project
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
   ```

2. **Run migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```
3. **Create super user:**
   ```bash
    python manage.py createsuperuser
   ```

4. **Environment variables:**
   
   - CONSUMER_URL: url of the consumer project instance

5. **Run server:**
   ```bash
    python manage.py runserver
   ```