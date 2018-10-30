# ACMResumeWebsite
This is the resume website for the ACM fundraiser Fall 2018. Created by Meg Anderson. 

In order to run this website locally (ie test it out), create a venv with flask installed (I'm using python 3.5 cause that's what I had installed). 

Navigate to the upper level directory, and use the commands (Linus/Unix you know the drill): 

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run
```

This will start the development environment. You don't have to restart the app while you make changes, it will update whenever you refresh your browser. If you edit your schema, you will have to reinit the db. 

Have fun 
If you have an questions, start with the flask documentation upon which this app is built. 
http://flask.pocoo.org/docs/1.0/tutorial/factory/