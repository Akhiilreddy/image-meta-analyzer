# Image Meta Analyzer

A Flask-based web application for uploading, processing, and analyzing image metadata with robust user authentication.

## Features

- User Authentication (Register/Login)
- Image Upload & Processing
- EXIF Metadata Extraction
- Detailed Image Information Display
- Responsive Dashboard
- History Viewing with Pagination

## Technologies Used

- Flask Web Framework
- SQLite Database
- Python Pillow for Image Processing
- Bootstrap for UI
- Flask-Login for Authentication
- Flask-SQLAlchemy for Database ORM

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd image-meta-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export SESSION_SECRET=your-secret-key
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Project Structure

- `/static` - Static files (CSS, JS, uploaded images)
- `/templates` - HTML templates
- `/instance` - Database files
- `app.py` - Application initialization
- `routes.py` - Route handlers
- `models.py` - Database models
- `forms.py` - Form definitions

## Usage

1. Register a new account
2. Log in to access the dashboard
3. Upload images (supported formats: PNG, JPG, JPEG, GIF)
4. View extracted metadata in the dashboard
5. Access upload history in the History page

## License

MIT License
