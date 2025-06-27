
Instantiating `apsimNGpy` Model Objects
========================================
You can either load a built-in template or use your own APSIM file.

.. admonition:: Loading Default APSIM Templates

    You can quickly get started by loading a default simulation model (e.g., maize) in one of two ways:

.. code-block:: python

    from apsimNGpy.core import base_data
    # Option 1: Load default maize simulation
    model = base_data.load_default_simulations(crop='maize')

    # Option 2: Equivalent direct instantiation. Supported by versions 0.35 +
    from apsimNGpy.core.apsim import ApsimModel
    model = ApsimModel(model='Maize', out_path = './maize.apsimx')

.. important::

    If ``out_path`` is not specified, the model will be saved to a randomly generated file path on your computer.
    The ``out_path`` parameter accepts both absolute and relative paths. If a relative path is provided, the file will be saved in the current working directory.

.. admonition:: Using a Local APSIM File

    If you have an ``.apsimx`` file saved on your machine — whether from a previous session or as a custom template—you can easily load it as shown below.
    By default, a random file path is generated as the output path. However, you can specify a custom path to control where the edited file is saved.
    This approach helps preserve the original file in case something goes wrong during the loading or editing process.

.. code-block:: python

    from apsimNGpy.core.apsim import ApsimModel

    # Load a local APSIM file
    model = ApsimModel(model='path/to/your/apsim/file.apsimx', out_path = './maize.apsimx')

.. admonition:: Next Actions
    Once your model is instantiated, you're ready to run simulations, edit model components, or inspect simulation settings. See the following sections for editing examples and diagnostics tools.
