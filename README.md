# Flask Cafe  & Wifi App

The Flask Cafe  & Wifi App is a web application that allows users to review and discover cafes. It provides a platform where users can register, log in, and add cafes they have visited. Users can also search for cafes based on their locations and view cafe details, such as amenities and coffee prices.

## Introduction Video of the Website



https://github.com/muzeffertagiyev/Cafe-WifiWebpage/assets/75939608/fbdef755-51a6-4e81-b62f-5c758ed4385c



## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Folder Structure](#folder-structure)


## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3
- Flask
- Flask SQLAlchemy
- Flask Login

### Installation

1. Clone the repository from GitHub:

   ```
   git clone https://github.com/muzeffertagiyev/Cafe-WifiWebpage.git
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt (or pip3 for mac users)
   ```

## Usage

1. **Register/Login**: Users can create an account by registering with their username and email. If they already have an account, they can log in using their credentials.

2. **Home Page**: The home page displays a list of cafes, showing their data and creators. Users can browse through the cafes by clicking the account name and see the user's added cafes

3. **Add a New Cafe**: Logged-in users can add new cafes they have visited. They need to provide the cafe's name, location, map URL, image URL, seating capacity, availability of toilet, Wi-Fi, sockets, and whether the cafe allows taking calls. Users can also specify the coffee price (optional).

4. **Search Cafes**: Users can search for cafes by entering a location in the search bar. The app will display cafes that match the entered location or have similar locations.

5. **Update/Delete Cafes**: Users can update or delete cafes they have added. They can edit the cafe's information or remove it from the list.

6. **User Profile**: Each user has a profile page that displays their added cafes. Users can update their username and email or reset their passwords.

## Features

- User authentication and authorization using Flask Login.
- Database models for users and cafes using SQLAlchemy.
- Adding, updating, and deleting cafes by registered users.
- Searching for cafes by location.
- Password reset functionality.
- Error handling for 404 pages.

## Folder Structure

The repository is organized as follows:

- `app.py`: The main Flask application file containing the routes and configurations.
- `forms.py`: Contains Flask-WTF forms used for registration, login, adding cafes, updating user details, and resetting passwords.
- `templates`: This directory contains the HTML templates used for rendering the web pages.
- `static`: Contains static files like CSS, images, and JavaScript files.
- `cafe.db`: The SQLite database file where the cafes and user information are stored.
- `README.md`: This file, providing information about the application and its usage.



Enjoy the app! 😊

