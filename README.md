flask-restaurant
================
this is the project for (Da Chuang) that i build it all by own.

IT IS STILL UNDER DEVELOPMENT

#it is build with python/flask

#content:
  1: users with four kinds of roles
    1: admin role
      1: can change users roles(like change normal users to staff to help manage the website)
      2: handle users requests for transfer to salesmanagers role
      3: enable or disable users      ----   not implemented
      3: enable or disable restaurants     ----    not implemented
    
    2: staff role
      1: with some rights of the admin, so it help admin to manage the website

    3: salesmanager
      1: add/alter/delete restaurants
      2: add/alter/delete fooditems of one specific restaurant
      3: handle unhandled orders      -----   not implemented
  
    4: normal user
      1: register, confirm, login, reset password, alter password, alter email
      2: request salesmanager role (once everyone registered, it is only normal user)
      3: make orders
      4: search restaurants, lookup his own orders
      5: make comments for his own orders  -----   not implemented

  2: rest api (only for communicate with the mobile client)


#to run it
  add the environment
    export MAIL_USERNAME='gmail account'
    export MAIL_PASSWORD='password for gmail accout'
    export EJILE_ADMIN='the admin email'
    export SECRET_KEY='your secret_key here'
  or set in the config.py file
  
  virtualenv venv
  source ./venv/bin/activate
  python manage.py shell
      db.create_all()
      Role.insert_roles()
      ...you can add some fake users(and restaurants, salesmanager, fooditems or so on)
    
  python manage.py runserver

restful api -- http://localhost:5000/api/v1.0/......