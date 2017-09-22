=============
ws2812-server
=============


.. image:: https://img.shields.io/pypi/v/ws2812_server.svg
        :target: https://pypi.python.org/pypi/ws2812_server

.. image:: https://img.shields.io/travis/phephik/ws2812_server.svg
        :target: https://travis-ci.org/phephik/ws2812_server

.. image:: https://readthedocs.org/projects/ws2812-server/badge/?version=latest
        :target: https://ws2812-server.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/phephik/ws2812_server/shield.svg
     :target: https://pyup.io/repos/github/phephik/ws2812_server/
     :alt: Updates


Python server providing API remote access to control WS2812.


* Free software: MIT license
* Documentation: https://ws2812-server.readthedocs.io.


Overview
========

WS2812-server allows remote control for WS2812 LED strip. Server application use RESTful API.

Dependencies
==============

Compatible with Python 3.5

* Required packages: WS2812-driver

.. code-block:: bash

    pip3 install git+https://github.com/calcite/ws2812-driver.git

Functionality
=============

* Click argument - config_file.yaml, which set server, driver and layers

.. code-block:: bash

    ws2812-driver setting.yaml
    
WS2812-server is controled over HTTP request POST.

* Set up a new layer

.. code-block:: bash

    POST 0.0.0.0:8080/layers/{new}/set
    

.. code-block:: bash

    {
		"origin": 0,
		"leds": 100,
		"alpha": 100
    }  
    
* Show_scale

.. code-block:: bash

    POST 0.0.0.0:8080/layers/{layer}/show_scale
    

.. code-block:: bash

   {
	"min": 0,
	"max": 100,
	"temp": 100,
	"bright": 100,
	"heatmap": [{"min": 0, "max": 80, "colour": [20,0,0]},{"min": 100, "max": 300, "colour": [0,20,0]}, {"min": 500, "max": 1000, "colour": [80,0,30]}] ,
	"reverse": 0
    }

* Show_raw

.. code-block:: bash

    POST 0.0.0.0:8080/layers/{layer}/show_raw
    

.. code-block:: bash

    {
		"red": 80,
		"green": 200,
		"blue": 116
    }

* Show_animation

.. code-block:: bash

    POST 0.0.0.0:8080/layers/{layer}/show_animation
    

.. code-block:: bash

    {
		"speed": 100
    }
    
    



This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

