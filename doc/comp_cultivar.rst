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

