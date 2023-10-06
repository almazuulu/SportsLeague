# Django Sports League Ranking Table

## Introduction

Welcome to the Django-based Sports League Ranking Table web application. 
This application allows users to upload a CSV file containing the results of 
games in a sports league, and it displays the ranking table based on the uploaded data.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [CSV Format](#csv-format)
- [Points System](#points-system)
- [Sample Input](#sample-input)
- [Sample Output](#sample-output)
- [Installation & Setup](#installation--setup)
- [Screenshots](#screenshots-of-the-web-application)
  - [Main Page to Upload CSV](#main-page-to-upload-csv)
  - [Games Table after Uploading CSV File](#games-table-after-uploading-csv-file)
  - [Editing the Game](#editing-the-game)
  - [Deleting the Game](#deleting-the-game)
  - [Adding Game](#adding-game)
  - [Authorization Permissions](#authorization-permissions)
  - [Login and Register](#login-and-register)

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
## Installation & Setup

### 1. Clone the Repository:

```bash
git clone https://github.com/almazuulu/SportsLeague.git
cd sportleague
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

### 8. Upload CSV File:

From the page `http://127.0.0.1:8000/` you can upload CSV File if you LogedIn User, 
Else you have to register

NOTICE: You can use "sport_games.csv" file to upload csv and test it

# Screenshots of the Web Application:

### Main page to Upload CSV: 

![Upload CSV](sportleague/screenshots/upload_csv.png)

### Games table after uploading CSV File:

There you can make all CRUD Operations:
- Edit Game
- Delete Game
- Add New Game (Add New Team)

![Games Table](sportleague/screenshots/games_table.png)

### Editing the Game:

![Edit Game1](sportleague/screenshots/edit_game.png)
![Edit Game2](sportleague/screenshots/edit_game1.png)

NOTICE: After editing the game, ranking also dynamically updates
Example of game between teams Crazy Ones vs. Misfits and how their ranking updates 
after we edit the game:

![Edit Game3](sportleague/screenshots/update_ranking_ed1.png)
![Edit Game4](sportleague/screenshots/update_ranking_ed.png)
![Edit Game5](sportleague/screenshots/update_ranking_ed2.png)
![Edit Game6](sportleague/screenshots/update_ranking_ed3.png)
![Edit Game6](sportleague/screenshots/update_ranking_ed4.png)

### Deleting the Game:

![Delete Game1](sportleague/screenshots/delete_game.png)
![Delete Game2](sportleague/screenshots/delete_game1.png)

Notice: After deleting the game, ranking also dynamically updates
If we delete the game and one of the team has no more games between other teams 
this team is removed from the Ranking table also

See the example bellow between Real Madrid vs. Barcelona, where Barcelona has no more games apart
from Real Madrid:

![Delete Game3](sportleague/screenshots/delete_update_rating1.png)
![Delete Game4](sportleague/screenshots/delete_update_rating2.png)

And Now there no more Barcelona team in the Ranking:

![Delete Game5](sportleague/screenshots/delete_update_rating3.png)

### Adding Game:

![Add Game1](sportleague/screenshots/add_game.png)

You can choose from the old teams and create from them some game

![Add Game2](sportleague/screenshots/add_game1.png)

Also you can choose "Create New Team" and forms dynamically opens for the new teams

![Add Game3](sportleague/screenshots/add_game2.png)

After adding the team it will apear in the Game and Ranking table with their scores:

![Add Game4](sportleague/screenshots/add_game3.png)
![Add Game5](sportleague/screenshots/add_game4.png)
![Add Game6](sportleague/screenshots/add_game5.png)

## Only Authorized users can Upload CSV, Edit Game Table (Delete, Update, Add):
![Permission 1](sportleague/screenshots/permission1.png)
![Permission 2](sportleague/screenshots/permission2.png)

If there are no data yet, not registered users are promted 
to Login to Upload, Add or Edit games:

![Permission 3](sportleague/screenshots/permission3.png)
![Permission 4](sportleague/screenshots/permission4.png)
If there are no data yet authorized users are promted to Upload, Add or Edit games:
![Permission 5](sportleague/screenshots/permission5.png)
![Permission 6](sportleague/screenshots/permission6.png)

## Login and Register:

#### Login Page:
![Login 1](sportleague/screenshots/login1.png)
![Login 2](sportleague/screenshots/login2.png)
![Login 3](sportleague/screenshots/login3.png)

#### Register Page:
![Register 1](sportleague/screenshots/register1.png)
![Register 2](sportleague/screenshots/register2.png)

## Unit Test Result Output:
![Unit Test](sportleague/screenshots/unit_test.png)

