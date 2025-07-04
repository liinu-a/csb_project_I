## Installing and running the application
Clone the project repository from GitHub

```bash
git clone https://github.com/liinu-a/csb_project_I
cd csb_project_I
```

Create a virtual environment by running the command

```bash
python3 -m venv venv
```

Activate the virtual environment on Linux/macOS with the command

```bash
source venv/bin/activate
```

on Windows

```bash
venv/Scripts/activate.bat  # CMD
venv/Scripts/Activate.ps1  # PowerShell
```

Install packages with the command

```bash
pip install -r requirements.txt
```

Create a .env file in the root directory and set a SECRET_KEY on the file to a unique, unpredictable value as follows:  
SECRET_KEY=*set this to a unique, unpredictable value*

To create the database tables, run the following command

```bash
python manage.py migrate
```

The Django development server can now be started with the command

```bash
python manage.py runserver
```
