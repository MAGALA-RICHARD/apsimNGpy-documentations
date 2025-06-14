Weather Data Replacement.
============================
apsimNGpy provides both an object oriented structure and procedural structure to replace the weather data. Here, I only demonstrate the object oriented one.

Replace instantly from the instantiated apsimNGpy model object. This is achieved with ``get_weather_from_web`` the with the following signature

.. code-block:: python

     def get_weather_from_web(self, lonlat: tuple, start: int, end: int, simulations=MissingOption, source='nasa',
                                 filename=None)

``lonlat``: ``tuple`` containing the longitude and latitude coordinates.

``start``: Start date for the weather data retrieval.

``end``: End date for the weather data retrieval.

``simulations``: str, list of simulations to place the weather data, defaults to all simulation if user specification is missing.

``source``: Source of the weather data. Defaults to 'nasa' because its world wide coverage, but other sources includes the ``daymet`` (Contiguous U.S. Only)

``filename``: Name of the file to save the retrieved data. If None, a default name is generated.

Example.
========

To use get_weather_from_web(), it requires instantiation of the model as follows;

.. code-block:: python

         from apsimNGpy.core.apsim import ApsimModel
         maize_model = ApsimModel(model='Maize') # replace maize with your apsim template file

         # replace the weather with lonlat specification as follows;
         maize_model.get_weather_from_web(lonlat = (-93.885490, 42.060650), start = 1990, end  =2001)

Changing weather data with non matching start and end dates in the simulation will lead to ``RuntimeErrors``.
To avoid this first check the start and end date before proceeding as follows.

.. code-block:: python

          dt = model.inspect_model_parameters(model_type='Clock', model_name='Clock', simulations='Simulation')
          start, end = dt['Start'].year, dt['End'].year
          # out put:  1990, 2000


