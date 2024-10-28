# AtruX backend repository

## Main branch available on Heroku

https://atrux-717ecf8763ea.herokuapp.com/

## 🛠 How to build locally 

### Windows

Clone project*

    git clone https://github.com/AtruXX/AtruX_BE.git

Create virtual environment*
    
    python -m venv ./venv

Activate virtual environment

    venv\Scripts\activate.bat

Install dependencies into virtual environment*

    pip install -r requirements.txt

Run server 
    
    python manage.py runserver 8080

*Remember to skip these steps when running after the initial setup

If you get https errors clear browser cache

<br><br>

# Methods

Response is returned in **.json** format

## <b>User management</b>
    http://127.0.0.1:8080/auth/users/ -> Create user [POST]
    http://127.0.0.1:8080/auth/users/resend_activation/ -> Resend user activation email [POST]
    http://127.0.0.1:8080/auth/token/login/ -> Login user [POST]
    http://127.0.0.1:8080/auth//token/logout/ -> Get new refresh token [POST]
    http://127.0.0.1:8080/auth/users/reset_password/ -> Password reset [POST]
    http://127.0.0.1:8080/auth/users/me/ -> User delete [DELETE]
    http://127.0.0.1:8080/auth/users/me/ -> Get authenticated user [GET]
