# StudySetU - College Notes Sharing Platform

A modern Django-based web application for sharing and managing college notes. Students can upload, search, and download study materials organized by course, subject, and semester.

## Features

- 🔐 **User Authentication**: Secure registration with email activation
- 📚 **Note Management**: Upload, edit, delete, and organize study notes
- 🔍 **Advanced Search**: Search notes by title, subject, or course
- 📊 **Analytics Dashboard**: Track downloads and note statistics (admin only)
- 👤 **User Profiles**: Customizable profiles with avatar support
- 🔑 **Password Recovery**: Email-based OTP password reset system
- 📱 **Responsive Design**: Modern, mobile-friendly interface
- 🎨 **Beautiful UI**: StudySetU branded design with custom logo

## Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, Custom CSS
- **Email**: SMTP (Gmail) / Console backend (development)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohitsharma10618-ship-it/Notes-website.git
   cd Notes-website/collegenotes
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   pip install pillow  # For image handling
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Email Configuration

For password reset and account activation, configure email settings in `collegenotes/settings.py`.

### Development (Console Backend)
```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### Production (Gmail SMTP)
See `EMAIL_SETUP.md` for detailed instructions.

## Project Structure

```
collegenotes/
├── accounts/          # User authentication and profiles
├── notes/             # Note management app
├── collegenotes/      # Project settings
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploads
└── manage.py          # Django management script
```

## Key Features Explained

### User Registration
- Email verification required
- Automatic profile creation
- Redirects to profile page after activation

### Note Management
- Upload PDFs and documents
- Organize by course, subject, semester
- Download tracking
- User-specific note collections

### Password Recovery
- OTP-based password reset
- Email verification
- Secure session management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Mohit Sharma

## Support

For issues and questions, please open an issue on GitHub.

---

**StudySetU** - Your journey to academic excellence! 📚✨

