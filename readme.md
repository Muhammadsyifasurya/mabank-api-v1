# MaBank API Documentation

## Overview

This is a RESTful API for **MaBank**, which provides functionalities for **User Management**, **Account Management**, and **Transaction Management**. The API is designed to handle secure and efficient interactions between users and the system. this is link for my documentation :
[MaBank API Postman Documentation](https://documenter.getpostman.com/view/40816177/2sAYkDNLiK)

## Features

- **User Management**: Allows users to create, update, and view their profile.
- **Account Management**: Supports creating, retrieving, updating, and deleting accounts.
- **Transaction Management**: Facilitates transaction operations like deposits, withdrawals, and transfers.

## Installation & Setup

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- Postman (for API testing)
- dbeaver (for checking the database)

### Installation Steps

1. Clone the repository :

   ```bash
   git clone https://github.com/revou-fsse-oct24/milestone-3-Muhammadsyifasurya.git
   ```

2. Navigate to the project directory :

   ```bash
   cd milestone-3-Muhammadsyifasurya
   ```

3. Install a virtual environment and activate it :

   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```

4. Navigate to the project folder where the dependencies are located :

   ```bash
   cd mabank_api
   ```

5. Install required dependencies :

   ```bash
   pip install -r requirements.txt
   ```

6. Create file .env and fill with this configurtaion :

   ```bash
   DATABASE_URL=sqlite:///revo_bank.db
   SECRET_KEY=super_secret_key
   FLASK_ENV=development
   FLASK_DEBUG=False
   ```

7. Initialization database with Flask-Migrate :

   ```bash
   flask db init  # just do this if 'migrations' folder is nothing
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. Run the application :

   ```bash
   flask run
   ```
