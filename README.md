# mail_app

This is a sample messaging app coded in python as a backend and angular4 as a frontend.

## Frontend:-

Make sure you have angular cli installed
go to mail-client folder and run npm install
then run ng serve

## Backend:-

- Make sure you have python3.5 installed
- Run python src/main.py
- Db migrations are there in db folder.

Go to localhost:4200 and see the magic

##### Add some sample users with add user API 
URL    /users \
Method POST \  
BODY {'name':'','email':'','password':''}

## Functionality

- Send mail to multiple users by providing their mail ids as a CSV (comma seperated values).
- Send, save and delete mails and they will appear in the placeholders accordingly.
    - For Example If you send a mail then it will appear in your sent mail box  
- Reply, Forward a message
- Color coding of a message when read


### Find the DB dump in backend/db folder