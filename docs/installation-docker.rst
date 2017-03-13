Docker Installation
===================

#. **Requirements**

   You will need `docker <https://docs.docker.com/installation/#installation>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_.


#. **Build the containers**

   Clone source code from the `repository <https://github.com/satnogs/satnogs-db>`_::

     $ git clone https://github.com/satnogs/satnogs-db.git
     $ cd satnogs-db

   Set your environmental variables::

     $ cp .env-dist .env

   Start database containers::

     $ docker-compose up -d db

   Build satnogs-db container::

     $ docker-compose build web

   Run the initialize script to populate the database with scheme and demo data::

    $ docker-compose run web python manage.py initialize


#. **Run it!**

   Run satnogs-db::

     $ docker-compose up

   Your satnogs-db development instance is available in localhost:8000. Go hack!
