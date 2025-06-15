
Instantiating `apsimNGpy` Model Objects
=========================================
You can either load a built-in template or use your own APSIM file.

Loading Default APSIM Templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can quickly get started by loading a default simulation model (e.g., maize) in one of two ways:

.. code-block:: python

    from apsimNGpy.core import base_data
    # Option 1: Load default maize simulation
    model = base_data.load_default_simulations(crop='maize')

    # Option 2: Equivalent direct instantiation. Supported by versions 0.35 +
    from apsimNGpy.core.apsim import ApsimModel
    model = ApsimModel(model='Maize')


Using a Local APSIM File
^^^^^^^^^^^^^^^^^^^^^^^^
If you have an `.apsimx` file saved on your machine—either from a previous session or custom template—you can easily load it like so:

.. code-block:: python

    from apsimNGpy.core.apsim import ApsimModel

    # Load a local APSIM file
    model = ApsimModel(model='path/to/your/apsim/file.apsimx')

Once your model is instantiated, you're ready to run simulations, edit model components, or inspect simulation settings. See the following sections for editing examples and diagnostics tools.
