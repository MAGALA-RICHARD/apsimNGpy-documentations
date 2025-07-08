Comparing cultivars yield
===============================

In this tutorial we are going to compare the cultivar yield across different cultivars using apsimNGpy

Firstly, we are going to start by creating a none permutation experiment

.. code-block:: python

    from apsimNGpy.core.apsim import ApsimModel
    model = ApsimModel('Maize')
    model.create_experiment(permutation=False)
    model.add_factor(specification="[Sow using a variable rule].Script.CultivarName =  Dekalb_XL82, Melkassa, Pioneer_34K77, Laila, B_110, A_90")
    model.run()
    df = model.results


getting info about the simulated output

.. code-block:: python

    import pandas as pd
    pd.set_option('display.max_columns', None)
    df.info
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 60 entries, 0 to 59
    Data columns (total 18 columns):
     #   Column                            Non-Null Count  Dtype
    ---  ------                            --------------  -----
     0   SimulationName                    60 non-null     object
     1   SimulationID                      60 non-null     int64
     2   CheckpointID                      60 non-null     int64
     3   CheckpointName                    60 non-null     object
     4   Clock.Today                       60 non-null     object
     5   CultivarName                      60 non-null     object
     6   Experiment                        60 non-null     object
     7   Maize.AboveGround.N               60 non-null     float64
     8   Maize.AboveGround.Wt              60 non-null     float64
     9   Maize.Grain.N                     60 non-null     float64
     10  Maize.Grain.NumberFunction        60 non-null     float64
     11  Maize.Grain.Size                  60 non-null     float64
     12  Maize.Grain.Total.Wt              60 non-null     float64
     13  Maize.Grain.Wt                    60 non-null     float64
     14  Maize.Phenology.CurrentStageName  60 non-null     object
     15  Maize.Total.Wt                    60 non-null     float64
     16  Yield                             60 non-null     float64
     17  Zone                              60 non-null     object
    dtypes: float64(9), int64(2), object(7)
    memory usage: 8.6+ KB
    # most of the columns in the dataset are float




