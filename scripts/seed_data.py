#!/usr/bin/env python
"""
Script to seed the database with sample courses, lessons, and instructors.
Run with: python scripts/seed_data.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mooc_catalog.settings')
django.setup()

from courses.models import Course, Lesson, Instructor

# Sample instructors data - IIT Madras BS Degree Professors
instructors_data = [
    {
        'name': 'Prof. Andrew Thangaraj',
        'bio': 'Professor Andrew Thangaraj is a faculty member in the Department of Electrical Engineering at IIT Madras. He specializes in information theory, coding theory, and wireless communications. He is known for his engaging teaching style and has been instrumental in developing the foundational courses for the IIT Madras BS Degree program.',
        'website': 'https://www.ee.iitm.ac.in/andrew/',
    },
    {
        'name': 'Prof. Madhavan Mukund',
        'bio': 'Professor Madhavan Mukund is a distinguished faculty member at Chennai Mathematical Institute and teaches for the IIT Madras BS Degree program. He is an expert in formal verification, automata theory, and programming languages. He has designed several programming courses that are highly acclaimed for their clarity and depth.',
        'website': 'https://www.cmi.ac.in/~madhavan/',
    },
    {
        'name': 'Thejesh Gangaiah Nagarathna',
        'bio': 'Thejesh Gangaiah Nagarathna is an experienced software developer and educator who teaches web development for the IIT Madras BS Degree program. He has extensive experience in building scalable web applications and is passionate about making web development accessible to beginners.',
        'website': 'https://thejeshgn.com/',
    },
]

# Sample courses data
courses_data = [
    {
        'title': 'Introduction to Python Programming',
        'short_description': 'Learn the fundamentals of Python programming from scratch.',
        'long_description': '''This comprehensive course will teach you Python programming from the ground up.

You'll learn:
- Variables and data types
- Control flow and loops
- Functions and modules
- Object-oriented programming
- File handling and exceptions

Perfect for beginners with no prior programming experience.''',
        'instructor_name': 'Prof. Madhavan Mukund',
        'lessons': [
            {'title': 'Getting Started with Python', 'content': 'Welcome to Python! In this lesson, we will install Python and write our first program.\n\nPython is a versatile, high-level programming language known for its readability and simplicity.\n\nLet\'s start by printing "Hello, World!":\n\nprint("Hello, World!")', 'youtube_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw'},
            {'title': 'Variables and Data Types', 'content': 'Variables are containers for storing data values.\n\nPython has several built-in data types:\n- Strings: "Hello"\n- Integers: 42\n- Floats: 3.14\n- Booleans: True/False\n\nExample:\nname = "Alice"\nage = 25\nheight = 5.6\nis_student = True', 'youtube_url': 'https://www.youtube.com/watch?v=Z1Yd7upQsXY'},
            {'title': 'Control Flow: If Statements', 'content': 'Control flow allows your program to make decisions.\n\nif condition:\n    # do something\nelif another_condition:\n    # do something else\nelse:\n    # default action\n\nExample:\nage = 18\nif age >= 18:\n    print("You can vote!")\nelse:\n    print("You cannot vote yet.")', 'youtube_url': 'https://www.youtube.com/watch?v=Zp5MuPOtsSY'},
            {'title': 'Loops: For and While', 'content': 'Loops allow you to repeat code multiple times.\n\nFor loop:\nfor i in range(5):\n    print(i)\n\nWhile loop:\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1'},
            {'title': 'Functions', 'content': 'Functions are reusable blocks of code.\n\ndef greet(name):\n    return f"Hello, {name}!"\n\nresult = greet("Alice")\nprint(result)  # Output: Hello, Alice!', 'youtube_url': 'https://www.youtube.com/watch?v=u-OmVr_fT4s'},
        ]
    },
    {
        'title': 'Web Development with Django',
        'short_description': 'Build modern web applications using Django framework.',
        'long_description': '''Master web development with Django, the high-level Python web framework.

Topics covered:
- Django project structure
- Models and databases
- Views and templates
- URL routing
- Forms and validation
- User authentication
- Deployment strategies

By the end of this course, you'll be able to build full-featured web applications.''',
        'instructor_name': 'Thejesh Gangaiah Nagarathna',
        'lessons': [
            {'title': 'Introduction to Django', 'content': 'Django is a high-level Python web framework that encourages rapid development.\n\nKey features:\n- Built-in admin interface\n- ORM for database operations\n- Template engine\n- URL routing\n- Security features\n\nInstall Django:\npip install django', 'youtube_url': 'https://www.youtube.com/watch?v=UmljXZIypDc'},
            {'title': 'Creating Your First Project', 'content': 'Create a new Django project:\n\ndjango-admin startproject myproject\ncd myproject\npython manage.py runserver\n\nVisit http://localhost:8000 to see your app!', 'youtube_url': 'https://www.youtube.com/watch?v=PtQiiknWUcI'},
            {'title': 'Models and Databases', 'content': 'Models define your data structure.\n\nfrom django.db import models\n\nclass Article(models.Model):\n    title = models.CharField(max_length=200)\n    content = models.TextField()\n    created_at = models.DateTimeField(auto_now_add=True)\n\nRun migrations:\npython manage.py makemigrations\npython manage.py migrate'},
            {'title': 'Views and Templates', 'content': 'Views handle requests and return responses.\n\nfrom django.shortcuts import render\nfrom .models import Article\n\ndef article_list(request):\n    articles = Article.objects.all()\n    return render(request, "articles/list.html", {"articles": articles})', 'youtube_url': 'https://www.youtube.com/watch?v=0sMtoedWaf0'},
            {'title': 'User Authentication', 'content': 'Django includes a built-in authentication system.\n\nfrom django.contrib.auth.decorators import login_required\n\n@login_required\ndef dashboard(request):\n    return render(request, "dashboard.html")'},
        ]
    },
    {
        'title': 'Data Science Fundamentals',
        'short_description': 'Introduction to data analysis and visualization with Python.',
        'long_description': '''Dive into the world of data science with Python.

What you'll learn:
- NumPy for numerical computing
- Pandas for data manipulation
- Matplotlib and Seaborn for visualization
- Basic statistical analysis
- Introduction to machine learning

Ideal for those who want to start a career in data science.''',
        'instructor_name': 'Prof. Andrew Thangaraj',
        'lessons': [
            {'title': 'Introduction to NumPy', 'content': 'NumPy is the fundamental package for numerical computing in Python.\n\nimport numpy as np\n\n# Create arrays\narr = np.array([1, 2, 3, 4, 5])\nprint(arr.mean())  # 3.0\nprint(arr.sum())   # 15', 'youtube_url': 'https://www.youtube.com/watch?v=8JfDAm9y_7s'},
            {'title': 'Data Manipulation with Pandas', 'content': 'Pandas provides data structures for efficient data manipulation.\n\nimport pandas as pd\n\ndf = pd.DataFrame({\n    "name": ["Alice", "Bob", "Charlie"],\n    "age": [25, 30, 35]\n})\n\nprint(df.describe())', 'youtube_url': 'https://www.youtube.com/watch?v=PcvsOaixUh8'},
            {'title': 'Data Visualization Basics', 'content': 'Visualize your data with Matplotlib.\n\nimport matplotlib.pyplot as plt\n\nx = [1, 2, 3, 4, 5]\ny = [2, 4, 6, 8, 10]\n\nplt.plot(x, y)\nplt.xlabel("X axis")\nplt.ylabel("Y axis")\nplt.title("Simple Line Plot")\nplt.show()', 'youtube_url': 'https://www.youtube.com/watch?v=3Xc3CA655Y4'},
        ]
    },
    {
        'title': 'Advanced Python Techniques',
        'short_description': 'Take your Python skills to the next level with advanced concepts.',
        'long_description': '''Build on your Python foundation with advanced programming techniques.

Topics include:
- Decorators and generators
- Context managers
- Metaclasses
- Async programming
- Performance optimization

Prerequisite: Basic Python knowledge required.''',
        'instructor_name': 'Prof. Madhavan Mukund',
        'lessons': [
            {'title': 'Decorators Deep Dive', 'content': 'Decorators are a powerful feature that allows you to modify the behavior of functions.\n\ndef my_decorator(func):\n    def wrapper(*args, **kwargs):\n        print("Before function")\n        result = func(*args, **kwargs)\n        print("After function")\n        return result\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print("Hello!")'},
            {'title': 'Generators and Iterators', 'content': 'Generators provide a memory-efficient way to work with large datasets.\n\ndef fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b\n\nfor num in fibonacci(10):\n    print(num)'},
            {'title': 'Context Managers', 'content': 'Context managers help you manage resources properly.\n\nclass FileManager:\n    def __init__(self, filename):\n        self.filename = filename\n    \n    def __enter__(self):\n        self.file = open(self.filename, "r")\n        return self.file\n    \n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()'},
        ]
    },
]

def seed_database():
    """Create sample instructors, courses, and lessons."""
    print("Seeding database with sample data...")

    # Create instructors
    instructors = {}
    for instructor_data in instructors_data:
        instructor, created = Instructor.objects.get_or_create(
            name=instructor_data['name'],
            defaults=instructor_data
        )
        instructors[instructor.name] = instructor
        if created:
            print(f"Created instructor: {instructor.name}")
        else:
            print(f"Instructor already exists: {instructor.name}")

    # Create courses and lessons
    for course_data in courses_data:
        lessons = course_data.pop('lessons')
        instructor_name = course_data.pop('instructor_name')
        instructor = instructors.get(instructor_name)

        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults={**course_data, 'instructor': instructor}
        )

        if created:
            print(f"Created course: {course.title}")
            for i, lesson_data in enumerate(lessons):
                Lesson.objects.create(
                    course=course,
                    order=i,
                    **lesson_data
                )
                print(f"  - Created lesson: {lesson_data['title']}")
        else:
            print(f"Course already exists: {course.title}")

    print("\nSeeding complete!")
    print(f"Total instructors: {Instructor.objects.count()}")
    print(f"Total courses: {Course.objects.count()}")
    print(f"Total lessons: {Lesson.objects.count()}")

if __name__ == '__main__':
    seed_database()
