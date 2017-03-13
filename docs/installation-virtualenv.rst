VirtualEnv Installation
=======================

Requirements: You will need python, python-virtualenvwrapper, pip and git


#. **Build the environment**

   Clone source code from the `repository <https://github.com/satnogs/satnogs-db>`_::

     $ git clone https://github.com/satnogs/satnogs-db.git

   Set up the virtual environment. On first run you should create it and link it to your project path.::

     $ cd satnogs-db
     $ mkvirtualenv satnogs-db -a .

   Set your environmental variables::

     $ cp .env-dist .env

   Activate your python virtual environment::

     $ workon satnogs-db

   Install local development requirements::

     $ (satnogs-db)$ pip install -r requirements/dev.txt


#. **Database**

   Create, setup and populate the database with demo data::

     (satnogs-db)$ ./manage.py initialize


#. **Run it!**

  Just run it::

    (satnogs-db)$ ./manage.py runserver

  Your satnogs-db development instance is available in localhost:8000. Go hack!
