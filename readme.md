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
    https://atrux-717ecf8763ea.herokuapp.com//auth/users/ -> Create user [POST]
    https://atrux-717ecf8763ea.herokuapp.com//auth/users/resend_activation/ -> Resend user activation email [POST]
    https://atrux-717ecf8763ea.herokuapp.com//auth/token/login/ -> Login user [POST]
    https://atrux-717ecf8763ea.herokuapp.com//auth//token/logout/ -> Get new refresh token [POST]
    https://atrux-717ecf8763ea.herokuapp.com//auth/users/reset_password/ -> Password reset [POST]
    https://atrux-717ecf8763ea.herokuapp.com//auth/users/me/ -> User delete [DELETE]
    https://atrux-717ecf8763ea.herokuapp.com//auth/users/me/ -> Get authenticated user [GET]
    https://atrux-717ecf8763ea.herokuapp.com/get_drivers -> Get all drivers from the same company (must be authenticated as a dispacher) [GET]
    https://atrux-717ecf8763ea.herokuapp.com/get_profile -> Get user profile(must be authenticated) [GET]
    https://atrux-717ecf8763ea.herokuapp.com/give_rating/ -> Give rating to a driver (as a dispacher) [PUT] fields: "driver_id", "rating"
