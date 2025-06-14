Instantiating apsimNGpy model objects.
======================================

.. code-block:: python

         from apsimNGpy.core import base_data


Instantiating with default template apsim Models.
-------------------------------------------------
this can be achieved in two ways as follows


load default ``maize`` module::

    model = base_data.load_default_simulations(crop ='maize')

Same as::

    from apsimNGpy.core.apsim import ApsimModel
    model = ApsimModel(model= 'Maize')


Use you local apsim file template
-----------------------------------
Many times if the file is on your pc or you saved it from the previous session, you can still use ``ApsimModel`` to load the dataset


.. code-block:: python

     from apsimNGpy.core.apsim import ApsimModel
     model = ApsimModel(model= 'filepathtoyourapsimtemplates')

We are now set and ready to conduct simulation edit the file or inspect the file see preceeding sections