flask-restaurant
================
this is the project for (  ) that i build it all by own.

IT IS STILL UNDER DEVELOPMENT

#it is build with python/flask

#CONTENT:
  it is like ele.me
  with four kinds of different priviledged roles
  1: admin role
    1:can change users roles(like change normal users to staff, to help manage the website)
    2:enable or disable users
    
  2: staff role
    help admin to manage the website
  
  3: salesmanager
    1:add/alter/delete restaurants
    2:add/alter/delete fooditems
    3:handle unhandled orders
  
  4: normal user
    make orders


#TO MAKE IT RUN
  add the environment
    <export .....>
  
  virtualenv venv
  cd venv
  source ./venv/bin/activate
  python manage.py shell
    (
      db.create_all()
      Role.insert_roles()
      ...you can add some fake users(and restaurants, salesmanager, fooditems or so on)
    )
    
  python manage.py runserver
  
  
restful api -- http://localhost:5000/api/v1.0/......
