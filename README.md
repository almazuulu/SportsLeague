# Django Sports League Ranking Table

## Introduction

Welcome to the Django-based Sports League Ranking Table web application. 
This application allows users to upload a CSV file containing the results of 
games in a sports league, and it displays the ranking table based on the uploaded data.

## Table of Contents

- [Features](#features)
- [CSV Format](#csv-format)
- [Points System](#points-system)
- [Sample Input](#sample-input)
- [Sample Output](#sample-output)
- [Extra Features](#extra-features)
- [Evaluation](#evaluation)
- [Submission](#submission)
- [Platform](#platform)

## Features

- Upload a CSV with game results.
- Dynamic ranking table based on game results.
- Ability to add, edit, and delete games via the web interface.
- Authentication, Authorization, Registration for enhanced security.

## CSV Format

The CSV file should be structured as follows:
```
team_1 name, team_1 score, team_2 name, team_2 score
```

## Points System

- **Win**: 3 points
- **Draw**: 1 point
- **Loss**: 0 points

Teams with the same points will be ranked alphabetically.

## Sample Input

[Your sample input goes here, if you have any]

## Sample Output

```
Ranking   | Team       | Points
--------- | ---------- | ------
1         | Fantastics | 6
2         | Crazy Ones | 5
3         | FC Super   | 1
4         | Rebels     | 1
5         | Misfits    | 0
```

## Screenshots:

#### Main page to Upload CSV: 
![Главная страница](sportleague/screenshots/upload_csv.png)

#### Games table after uploading CSV File:
There you can make all CRUD Operations:
- Edit Game
- Delete Game
- Add New Game (Add New Team)
![Главная страница](sportleague/screenshots/games_table.png)

##### Editing the Game:






## Installation & Setup

### 1. Clone the Repository:

```bash
git clone [YOUR REPO LINK]
cd [YOUR PROJECT DIRECTORY]
```

### 2. Set Up a Virtual Environment (Optional but Recommended):

```bash
python -m venv venv
source venv/bin/activate  # for Linux/macOS
# or
venv\Scripts\activate     # for Windows
```

### 3. Install Required Dependencies:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations:

```bash
python manage.py migrate
```

### 4.1 Optional Data Loading:

If you have any sample data you wish to preload:

```bash
python manage.py loaddata [YOUR DATA FILE].json
```

### 5. Create an Admin User (for managing the web interface):

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server:

```bash
python manage.py runserver
```

Now, the application should be running at `http://127.0.0.1:8000/`.

### 7. Access the Admin Panel:

1. Open your browser and navigate to `http://127.0.0.1:8000/admin/`.
2. Log in using the superuser credentials you created in step 5.

Now, you can manage the games and other contents of your project from the admin panel.
