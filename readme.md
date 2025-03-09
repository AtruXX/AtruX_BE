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
    https://atrux-717ecf8763ea.herokuapp.com/auth/users/ -> Create user [POST]
    https://atrux-717ecf8763ea.herokuapp.com/auth/users/resend_activation/ -> Resend user activation email [POST]
    https://atrux-717ecf8763ea.herokuapp.com/auth/token/login/ -> Login user [POST]
    https://atrux-717ecf8763ea.herokuapp.com/auth//token/logout/ -> Get new refresh token [POST]
    https://atrux-717ecf8763ea.herokuapp.com/auth/users/reset_password/ -> Password reset [POST]
    https://atrux-717ecf8763ea.herokuapp.com/auth/users/me/ -> User delete [DELETE]
    https://atrux-717ecf8763ea.herokuapp.com/auth/users/me/ -> Get authenticated user [GET]
    https://atrux-717ecf8763ea.herokuapp.com/get_drivers -> Get all drivers from the same company (must be authenticated as a dispacher) [GET]
    https://atrux-717ecf8763ea.herokuapp.com/get_profile -> Get user profile(must be authenticated) [GET]
    https://atrux-717ecf8763ea.herokuapp.com/give_rating/ -> Give rating to a driver (as a dispacher) [PUT] fields: "driver_id", "rating"
    https://atrux-717ecf8763ea.herokuapp.com/change_status/ -> Change driver status (on_road) [PUT]
    https://atrux-717ecf8763ea.herokuapp.com/get_documents/<category>/ -> Get current user documents [GET]
    https://atrux-717ecf8763ea.herokuapp.com/upload_documents/ -> Upload a document for the current user [PUT]
    https://atrux-717ecf8763ea.herokuapp.com/delete_documents/ -> Delete a document from the current user by document_id [DELETE]
    https://atrux-717ecf8763ea.herokuapp.com/change_document_title/ -> Change the name of a document by document_id [PUT]
    https://atrux-717ecf8763ea.herokuapp.com/replace_document/ -> Replace a document by document_id and the new document [PUT]
    https://atrux-717ecf8763ea.herokuapp.com/create_route/ ->create route [POST]
    https://atrux-717ecf8763ea.herokuapp.com/get_routes ->get routes [GET]
    https://atrux-717ecf8763ea.herokuapp.com/create_driver/ -> create driver(must be authenticated as dispatcher) [POST]
    https://atrux-717ecf8763ea.herokuapp.com/drivers_number/ -> get the number of drivers of a company [GET]
    https://atrux-717ecf8763ea.herokuapp.com/create_transport/ -> create a new transport [POST]
    https://atrux-717ecf8763ea.herokuapp.com/upload_transport_documents/ -> upload document for a transport [POST]
    https://atrux-717ecf8763ea.herokuapp.com/update_transport/ -> update a transport [PUT]
    https://atrux-717ecf8763ea.herokuapp.com/delete_transport_document/ -> delete a transport document [DELETE]
    https://atrux-717ecf8763ea.herokuapp.com/list_transports/ -> list transports for a user [GET]
    https://atrux-717ecf8763ea.herokuapp.com/delete_transport/ -> delete a transport [DELETE]