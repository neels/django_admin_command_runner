
from setuptools import setup, find_packages

setup(
    name="django_admin_command_runner",
    version="0.9.3",
    packages=find_packages(),
    include_package_data=True,
    description="Run management commands from Django Admin",
    author="Your Name",
    author_email="you@example.com",
    url="https://example.com/django-admin-command-runner",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>=3.2"
    ],
    python_requires='>=3.6',
)
