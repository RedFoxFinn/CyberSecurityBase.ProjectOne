
# Cyber Security Base - Course project 1

This repository is housing the course project of mine for the University of Helsinki course CSB.

Goal is to build a web app that's faulty and the provide the fixes. Faulty in this context means that it should contain at least 5 of the vulnerability categories from the [OWASP Top 10](https://owasp.org/Top10/) (2025 version could be already released. If that's true, try [this](https://owasp.org/www-project-top-ten/2021/) link instead).

```
Make sure that (these are the most common reasons for project being rejected)

- The flaws are real, and not just hypothetical, and the fixes are included in the code.
- The flaws are in the code or in installation script, for example, having admin/admin user in the database is not enough.
- The fix actually fixes the problem, and not just hide it.
- Screenshots are included in the repository.
- There is a backend, and the flaws/fixes occur in the backend. Remember that the user can manipulate the frontend as much as possible.
```

## The Application: Task Management System

A Django-based task management system that demonstrates selection (the greatest hits) of OWASP vulnerabilities.

### How It Works

**Normal (Secure) Behavior:**
- Users can only view their own tasks
- Users can only edit/delete their own tasks
- Tasks are private by default
- Proper authorization checks on all operations

**Vulnerable Mode (`VULNERABLE=True`, the default):**
- All tasks visible to all users (even anonymous)
- Logged-in users can edit ANY task (not just their own)
- Logged-in users can delete ANY task (not just their own)
- No ownership verification
- Creation still requires authentication (secure feature)

This demonstrates real-world broken access control vulnerabilities that could allow users to:
- See private data of other users
- Modify other users' information
- Delete other users' data
- Escalate their privileges

## Selected Vulnerability Categories

### A01 - Broken Access Control
[description](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

### A03 - Injection
[description](https://owasp.org/Top10/A03_2021-Injection/)

### A04 - Insecure Design
[description](https://owasp.org/Top10/A04_2021-Insecure_Design/)

### A07 - Identification and Authentication Failures
[description](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

### A08 - Software and Data Integrity Failures
[description](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

## Technically

The project is implemented in Python(3) using [Django](https://www.djangoproject.com/) framework and their features.

The code was written with Visual Studio Code as the IDE and in CUBBLI OS (Uni. Helsinki flavor of the Ubuntu).

## Setup & running the application

### 1. Create virtual environment (VENV)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```
pip3 install -r requirements.txt
```

### 3. Run migrations
```
python3 manage.py migrate
```

### 4. Create superuser (optional, but might be useful)
```
python3 manage.py createsuperuser
```

### 5. Create initial data for testing purposes
```
python3 manage.py create_test_data
```

### 6. Run the server

**Run in Vulnerable Mode (default):**
```
python3 manage.py runserver
```

**Run in Secure Mode:**
```
VULNERABLE=False python3 manage.py runserver
```

Visit `http://localhost:8000/` in your browser and have fun

## Report

The Essay / report is in a separate file [here](REPORT.md). This is due to the fact that it is easier to copy/paste for submission form of the course.

Report states where in the code the vulnerabilities are implemented AND how or where the fix is provided.

- Approx. 1000 words, hard limit 800 -- 1500 words

### Screenshots

So.. the screenshots we're talking about? As files, they're [here](screenshots/).

As extension to the report they are provided as a separate `.md` [here](SCREENSHOTS.md).
````

## Selected vulnerability categories

### A01 - Broken access control
[description](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

### A03 - Injection
[description](https://owasp.org/Top10/A03_2021-Injection/)

### A04 - Insecure design
[description](https://owasp.org/Top10/A04_2021-Insecure_Design/)

### A07 - Identification and authentication failures
[description](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

### A09 - Security logging and monitoring failures
[description](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)

## Technically

The project is implemented in Python(3) using [Django](https://www.djangoproject.com/) framework and its features.

The code was written with Visual Studio Code as the IDE and in CUBBLI OS (Uni. Helsinki flavor of the Ubuntu).

## Report

The Essay / report is in separate file [here](REPORT.md). This is due to the fact that it is easier to copy/paste for submission form of the course.

Report states where in the code the vulnerabilities are implemented AND how or where the fix is provided.

- Approx. 1000 words, hard limit 800 -- 1500 words

### Screenshots

So.. the screenshots we're talking about? As files, they're [here](screenshots/).

As extension to the report they are provided as a separate `.md` [here](SCREENSHOTS.md).