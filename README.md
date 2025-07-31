# django_admin_command_runner

A Django app that lets you run management commands directly from the Django Admin interface.

## 🔧 Installation

1. Install the package:

```bash
pip install django_admin_command_runner
```

2. Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_admin_command_runner',
]
```

That's it! No need to modify `urls.py`.

## 🚀 Features

- Run Django management commands from the admin.
- See full-page terminal-style output.
- No configuration or URL includes required.
- Fully plug-and-play.

## 💻 Usage

Go to:

```
/admin/django_admin_command_runner/commandlog/
```

Click “Run Command” to execute commands via the web interface.

## 🔐 Permissions

Ensure the user has access to the Django admin and is a staff member.

## ✅ Django Compatibility

Tested with Django 3.2 – 5.2+

