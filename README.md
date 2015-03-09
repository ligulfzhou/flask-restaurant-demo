flask-restaurant
================
this is the project for (Da Chuang) that i build it all by own.(IT IS STILL UNDER DEVELOPMENT)

#it is build with python/flask

##content.

 * users with four kinds of roles
    
    admin role
    
        * can change users roles(like change normal users to staff to help manage the website)
        * handle users requests for transfer to salesmanagers role
        * enable or disable users      ----   not implemented
        * enable or disable restaurants     ----    not implemented
    
    staff role

        * with some rights of the admin, so it help admin to manage the website

    salesmanager

        * add/alter/delete restaurants
        * add/alter/delete fooditems of one specific restaurant
        * handle unhandled orders      -----   not implemented
  
    normal user

        * register, confirm, login, reset password, alter password, alter email
        * request salesmanager role (once everyone registered, it is only normal user)
        * make orders
        * search restaurants, lookup his own orders
        * make comments for his own orders  -----   not implemented

 * rest api (only for communicate with the mobile client ---- mobile client is not implemented)

##setup

 * add the environment(like /etc/profile etc.) or set in the config.py file
  
```shell
        export MAIL_USERNAME='gmail account' 
        export MAIL_PASSWORD='password for gmail accout' 
        export EJILE_ADMIN='the admin email' 
        export SECRET_KEY='your secret_key here' 
```
 
 * Then


```shell
        virtualenv venv
        source ./venv/bin/activate
        python manage.py shell
            db.create_all()
            Role.insert_roles()
        you can add some fake users(and restaurants, salesmanager, fooditems or so on)
    
        python manage.py runserver
```

 * restful api -- http.//localhost:5000/api/v1.0/......
