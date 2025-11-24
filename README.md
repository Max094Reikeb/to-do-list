# To-Do List App

Simple To-Do List application built with Django to create, update and delete tasks.

<br>

![todolist](https://user-images.githubusercontent.com/65074901/125083144-a5e03900-e0e5-11eb-9092-da716a30a5f3.JPG)

---

## 1. Requirements

- Python 3.10+ (3.11+ recommended)
- Git
- (Optional but recommended) Virtual environment support (`venv` – built into Python)
- `pip` (Python package manager)

---

## 2. Getting Started (Local Development)

### 2.1. Clone the repository

```bash
git clone <REPO_URL> todolist
cd todolist
```
Replace `<REPO_URL>` with your Git URL (HTTPS or SSH).

### 2.2. Create and activate a virtual environment
macOS / Linux:
````bash
python -m venv .venv
source .venv/bin/activate
````

Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\Activate
```
You should now see `(.venv)` at the beginning of your terminal prompt.

### 2.3. Install dependencies
Dependencies are listed in requirements.txt:
```bash
pip install -r requirements.txt
```
By default this includes Django (3.2.x range).

### 2.4. Database migrations
Apply migrations (this sets up the SQLite database):
```bash
python manage.py migrate
```

### 2.5. Run the development server
```bash
python manage.py runserver 8000
```
Then open:
```bash
http://localhost:8000/
```
You should see the To-Do List app running.
The app’s current version is displayed on the main page (using the `APP_VERSION` setting).

## 3. Project Structure (Short Overview)
Key files and directories:
* `manage.py` – Django management script
* `todo/` – Django project configuration
  * `settings.py` – settings (including APP_VERSION)
  * `urls.py` – URL configuration
* `tasks/` – main application
  * `models.py` – Task model
  * `views.py` – task listing/creation logic
  * `templates/tasks/list.html` – main HTML template

## 4. Development Workflow
### 4.1. Coding
Typical workflow:
1. Create a new branch for a feature or fix:
```bash
git checkout -b feature/my-awesome-change
```
2. Edit Python/Django files as needed.
3. Run the app locally to test:
```bash
python manage.py runserver
```
4. (Optional) If you add tests, run them with:
```bash
python manage.py test
```

### 4.2. Useful Django commands
* Apply migrations:
```bash
python manage.py migrate
```
* Create a new migration (after changing models):
```bash
python manage.py makemigrations
```
* Create a superuser (if you want to use the admin):
```bash
python manage.py createsuperuser
```

## 5. Git: How to Commit
### 5.1. Check what changed
```bash
git status
git diff
```

### 5.2. Stage your changes
```bash
git add <file1> <file2>
# or add everything
git add .
```

### 5.3. Write a clear commit message
Use short, imperative messages like:
* `Add version display on main page`
* `Fix task deletion`
* `Refactor views into class-based views`
Example:
```bash
git commit -m "Add version display on main page"
```

### 5.4. Push your branch
```bash
git push origin feature/my-awesome-change
```
Then you can open a pull request if you’re using a platform like GitHub/GitLab.

## 6. Versioning & Releases
This project uses a simple versioning mechanism:
* The version is stored in `todo/settings.py` as:
```bash
APP_VERSION = "1.0.0"
``` 
* The main page displays this value.

### 6.1. `build.sh` – Release Script
There is a `build.sh` script at the root of the project that:
1. Takes a version number as parameter (e.g. `2.0.3`)
2. Updates `APP_VERSION` in `todo/settings.py`
3. Tags the current Git commit with that version
4. Generates a new zip archive named `todolist-<version>.zip` from the current Git HEAD<br>
**Usage**<br>
From the project root:
```bash
./build.sh version=2.0.3
```
What happens:
* `APP_VERSION` in `todo/settings.py` becomes `"2.0.3"`
* A Git tag `2.0.3` is created on the current commit
* An archive `todolist-2.0.3.zip` is created in the repository root
> Note:<br>
   The script expects:<br>
    "You’re in a Git repository"
   "`todo/settings.py` contains a line like APP_VERSION = "...""

**After running the script**<br>
If you’re using a remote (e.g. GitHub), don’t forget to push:
```bash
git push origin main       # or your default branch
git push origin 2.0.3      # push the tag
```
You can then use `todolist-2.0.3.zip` as a packaged version of the project.

## 7. Updating Dependencies
If you add new Python packages in the future:
1. Install them:
```bash
   pip install <package-name>
```
2. Freeze them into requirements.txt:
```bash
   pip freeze > requirements.txt
```
(Be careful not to include unrelated global packages; do this from inside the virtual environment.)

## 8. Troubleshooting
* **`ModuleNotFoundError: No module named 'django'`**<br>
→ Make sure you activated the virtualenv and installed requirements:
```bash
source .venv/bin/activate           # or .\.venv\Scripts\Activate on Windows
pip install -r requirements.txt
```
* **`Permission denied` when running `./build.sh`**<br>
→ Make the script executable:
```bash
chmod +x build.sh
```
* **Server doesn’t start / migration issues**<br>
* Try :
```bash
python manage.py migrate
```