# FD Management System

A web application for managing fixed deposits.

## Backend

### Requirements

```plaintext
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-CORS
```

### Configuration

```python
# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
