## Setup Instructions

### 1. Create virtual environment (VENV)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Run migrations
```bash
python3 manage.py migrate
```

### 4. Create superuser (optional, but might be useful)
```bash
python3 manage.py createsuperuser
```

### 5. Create initial data for testing purposes
```bash
python3 manage.py create_test_data
```

### 6. Run the server

**Run in Vulnerable Mode (default):**
```bash
python3 manage.py runserver
```

**Run in Secure Mode:**
```bash
VULNERABLE=False python3 manage.py runserver
```

Visit `http://localhost:8000/` in your browser and have fun