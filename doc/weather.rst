Weather Data Replacement.
============================
apsimNGpy provides both an object oriented structure and procedural structure to access the weather data.

Replace instantly from the instantiated apsimNGpy model object. This is achieved with ``get_weather_from_web`` the with the following signature

.. code-block:: python

     def get_weather_from_web(self, lonlat: tuple, start: int, end: int, simulations=MissingOption, source='nasa',
                                 filename=None)

Example.
========

To use get_weather_from_web(), it requires instantiation of the model as follows;

.. code-block:: python

         from apsimNGpy.core.apsim import ApsimModel
         maize_model = ApsimModel(model='Maize') # replace maize with your apsim template file
         # replace the
         maize_model.

