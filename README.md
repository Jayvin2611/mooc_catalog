# MOOC Catalog

A simple MOOC-style course catalog built with Django where users can browse courses, enroll, view lessons, and track their progress.

## Features

- **User Authentication**: Sign up and log in using Django's built-in auth system
- **User Profile**: Edit profile with username, email, first name, and last name
- **User Dropdown Menu**: Navbar dropdown with quick access to profile and logout
- **Course Catalog**: Browse all available courses with thumbnails and instructor info
- **Course Thumbnails**: Optional thumbnail images for courses
- **Instructor Profiles**: Instructor name, bio, profile picture, and website
- **More Courses by Instructor**: Discover other courses by the same instructor
- **Course Details**: View full course information, instructor profile, and lesson lists
- **Enrollment**: Logged-in users can enroll in courses
- **Lesson Viewing**: Access lesson content for enrolled courses
- **YouTube Video Support**: Optional embedded YouTube videos in lessons
- **Lesson Sidebar**: Hamburger menu with all course lessons for easy navigation
- **Progress Tracking**: Automatic tracking of viewed lessons with visual indicators
- **Progress Bar**: Visual progress bar showing completion percentage on My Courses page
- **Smart Resume**: "Continue Learning" button takes you directly to the next uncompleted lesson
- **Responsive Design**: Mobile-friendly with collapsible sidebar
- **Admin Panel**: Full CRUD operations for courses and lessons via Django admin
- **My Courses Dashboard**: View all enrolled courses with progress bars, status badges, and quick actions

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (Docker) / SQLite (local development)
- **Image Processing**: Pillow (for thumbnails and profile pictures)
- **Deployment**: Docker & Docker Compose

## Project Structure

```
mooc_catalog/
├── accounts/                 # User authentication app
│   ├── templates/accounts/   # Login, signup templates
│   ├── forms.py              # User registration form
│   ├── urls.py               # Auth URL routes
│   └── views.py              # Auth views
├── courses/                  # Main courses app
│   ├── templates/courses/    # Course templates
│   ├── admin.py              # Admin configuration
│   ├── models.py             # Course, Lesson, Enrollment, Progress models
│   ├── urls.py               # Course URL routes
│   └── views.py              # Course views
├── mooc_catalog/             # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI application
├── templates/                # Base templates
├── static/                   # Static files (favicon, etc.)
├── media/                    # User uploads (thumbnails, profile pics)
├── scripts/                  # Helper scripts
├── docker-compose.yml        # Production Docker config
├── docker-compose.dev.yml    # Development Docker config
├── Dockerfile                # Docker image definition
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mooc_catalog
   ```

2. **Start with Docker Compose**
   ```bash
   # Production mode
   docker-compose up --build

   # Or development mode (with hot reload)
   docker-compose -f docker-compose.dev.yml up --build
   ```

3. **Create a superuser** (in a new terminal)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Seed sample data** (optional)
   ```bash
   docker-compose exec web python scripts/seed_data.py
   ```

5. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Option 2: Local Development (without Docker)

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd mooc_catalog
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations courses
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed sample data** (optional)
   ```bash
   python scripts/seed_data.py
   ```
   This creates sample courses with IIT Madras BS Degree instructors:
   - Prof. Andrew Thangaraj
   - Prof. Madhavan Mukund
   - Thejesh Gangaiah Nagarathna

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

### Helper Scripts

Windows users can use the batch scripts:
```bash
# Local development
scripts\run_local.bat

# Docker deployment
scripts\docker_run.bat
```

Linux/Mac users can use the shell scripts:
```bash
# Local development
chmod +x scripts/run_local.sh
./scripts/run_local.sh

# Docker deployment
chmod +x scripts/docker_run.sh
./scripts/docker_run.sh
```

## Usage Guide

### For Students

1. **Sign Up**: Create an account at `/accounts/signup/`
2. **Browse Courses**: View all courses on the homepage
3. **View Course Details**: Click a course to see its description and lessons
4. **Enroll**: Click "Enroll in this Course" button
5. **View Lessons**: Click on any lesson to view its content
6. **Watch Videos**: If a lesson has a YouTube video, it will be embedded at the top
7. **Navigate Lessons**: Use the sidebar (or hamburger menu on mobile) to jump between lessons
8. **Track Progress**: Viewed lessons are marked with green checkmarks in the sidebar
9. **My Courses Dashboard**: Access your enrolled courses at `/my-courses/`
   - View progress bars showing completion percentage
   - See status badges: "Not Started", "In Progress", or "Completed"
   - Click "Continue Learning" to jump directly to your next uncompleted lesson
   - Click "Start Learning" to begin a new course
   - Click "Review Course" to revisit a completed course
10. **Edit Profile**: Click your username in the navbar dropdown to access profile settings
    - Update username, email, first name, and last name

### For Administrators

1. **Access Admin**: Go to `/admin/` and log in with superuser credentials
2. **Manage Instructors**: Add instructors with name, bio, profile picture, and website
3. **Manage Courses**: Add, edit, or delete courses with thumbnails and instructor assignment
4. **Manage Lessons**: Add lessons directly from the course edit page (inline) or separately
5. **Add YouTube Videos**: Paste a YouTube URL in the lesson's `youtube_url` field
   - Supported formats: `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`
6. **Upload Images**: Upload course thumbnails and instructor profile pictures via admin
7. **View Enrollments**: See which users are enrolled in which courses
8. **Monitor Progress**: View lesson progress for all users

## Models

### Instructor
- `name`: Instructor's full name
- `bio`: Biography/description of the instructor
- `profile_pic`: Optional profile picture (ImageField)
- `website`: Optional website URL
- `created_at`: Creation timestamp

### Course
- `title`: Course title
- `short_description`: Brief description for listings
- `long_description`: Full course description
- `thumbnail`: Optional course thumbnail image (ImageField)
- `instructor`: Foreign key to Instructor (optional)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Lesson
- `course`: Foreign key to Course
- `title`: Lesson title
- `content`: Lesson content
- `youtube_url`: Optional YouTube video URL (supports youtube.com and youtu.be links)
- `order`: Display order
- `created_at`: Creation timestamp

### Enrollment
- `user`: Foreign key to User
- `course`: Foreign key to Course
- `enrolled_at`: Enrollment timestamp
- Unique constraint on (user, course)

### LessonProgress
- `user`: Foreign key to User
- `lesson`: Foreign key to Lesson
- `viewed_at`: View timestamp
- Unique constraint on (user, lesson)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | dev key (change in production!) |
| `DEBUG` | Debug mode | True |
| `ALLOWED_HOSTS` | Comma-separated hosts | localhost,127.0.0.1 |
| `DATABASE_URL` | PostgreSQL connection string | SQLite |

## API Endpoints

| URL | View | Description |
|-----|------|-------------|
| `/` | course_list | List all courses |
| `/course/<id>/` | course_detail | Course details and lessons |
| `/course/<id>/enroll/` | enroll_course | Enroll in a course |
| `/course/<id>/lesson/<id>/` | lesson_detail | View lesson content |
| `/my-courses/` | my_courses | User's enrolled courses with progress |
| `/accounts/signup/` | signup | User registration |
| `/accounts/login/` | login | User login |
| `/accounts/logout/` | logout | User logout |
| `/accounts/profile/` | edit_profile | Edit user profile |
| `/admin/` | admin | Django admin panel |

## Development

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations courses
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Re-seeding Database
To reset and re-seed the database with fresh sample data:
```bash
python manage.py shell
>>> from courses.models import Course, Lesson, Instructor, Enrollment, LessonProgress
>>> LessonProgress.objects.all().delete()
>>> Enrollment.objects.all().delete()
>>> Lesson.objects.all().delete()
>>> Course.objects.all().delete()
>>> Instructor.objects.all().delete()
>>> exit()

python scripts/seed_data.py
```

## License

This project is open source and available under the MIT License.
