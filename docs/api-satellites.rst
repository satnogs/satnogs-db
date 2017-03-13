Satellites
==========

The ``satellites`` method of the :doc:`SatNOGS DB API </db/api>` returns all Satellites currently used for gathering Transmitters data.

Endpoint
--------

     ``https://db.satnogs.org/api/satellites/``

Examples
--------

Show a specific satellite using its Norad Cat ID:

    Request::

        /api/satellites/25544/?format=json

    Response::

        {
            norad_cat_id": 25544,
            "name": "ISS (ZARYA)"
        }
