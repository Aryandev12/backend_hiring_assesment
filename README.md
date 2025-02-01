# Multilingual FAQ System

A Django-based FAQ management system with multilingual support, WYSIWYG editor, and caching.

## Features

- Multilingual FAQ management (English, Hindi, Bengali)
- WYSIWYG editor support using CKEditor
- Automatic translation using Google Translate
- Redis caching for improved performance
- RESTful API with language selection
- Docker support for easy deployment

## Prerequisites

- Python 3.11+
- Redis
- Docker and Docker Compose (optional)

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Aryandev12/backend_hiring_assesment.git
cd faq
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Start Redis server:
```bash
# Ubuntu/Debian
sudo service redis-server start

# macOS
brew services start redis
```

7. Run development server:
```bash
python manage.py runserver
```

### Docker Setup

1. Build and start containers:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

3. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## API Usage

### Endpoints

- List FAQs: `GET /api/faqs/`
- Create FAQ: `POST /api/faqs/`
- Retrieve FAQ: `GET /api/faqs/{id}/`
- Update FAQ: `PUT /api/faqs/{id}/`
- Delete FAQ: `DELETE /api/faqs/{id}/`

### Language Selection

Add `lang` parameter to select language:

```bash
# English (default)
curl http://localhost:8000/api/faqs/

# Hindi
curl http://localhost:8000/api/faqs/?lang=hi

# Bengali
curl http://localhost:8000/api/faqs/?lang=bn
```

## Running Tests

```bash
pytest
```

Generate coverage report:
```bash
pytest --cov=faqs --cov-report=html
```



## License

This project is licensed under the MIT License - see the LICENSE file for details.
