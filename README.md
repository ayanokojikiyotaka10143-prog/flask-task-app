# Flask Task Manager

A simple task management web application built with Flask.
Created as part of 43030 Professional Practice in Computing at UTS.

## Features
- User registration and authentication
- Create, view, complete, and delete tasks
- Due date tracking
- Input validation on all forms
- Automated CI/CD pipeline with GitHub Actions
- Dockerised deployment

## Running Locally
```bash
pip install -r requirements.txt
python app.py
```
Visit http://localhost:5000

## Running with Docker
```bash
docker build -t flask-task-app .
docker run -p 5000:5000 flask-task-app
```

## Running Tests
```bash
python -m pytest tests/ -v
```

## CI/CD Pipeline
GitHub Actions runs automated tests on every push and PR to main.

## Author
Hasibul Islam Shihab — 14607889 — UTS
