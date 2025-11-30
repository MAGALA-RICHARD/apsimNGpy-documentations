.. _editor:

.. caption:: Model Parameter Editing

Editing model parameters
===========================================

Editing a model involves changing model parameter values. This task can be accomplished via
a unified method called  :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model` or :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model_by_path` from ``ApsimModel`` Class
by specifying the model type, name and simulation name, or path, respectively.

.. tip::

   Editing APSIM models in **apsimNGpy** does *not* require placing the
   target model inside a *Replacements* folder or node. However, when
   modifying **cultivar parameters**, it can be helpful to include a
   Replacements folder containing the relevant plant definition hosting
   that cultivar. In many cases, apsimNGpy will handle this automatically.

Selective editing
-----------------
Selective editing allows you to apply modifications only to certain
simulations. This is *not* possible when the same model instance is shared
through a common Replacements folder. For reliable selective editing,
each simulation should ideally reference a uniquely named model.
However, even when model names are not unique, apsimNGpy still enables
targeted editing through two mechanisms:

1. **Exclusion strategy**
   You can explicitly *exclude* simulations to which the edits should
   **not** be applied.

2. **Specification strategy**
   You can explicitly *specify* which simulations should have their
   models edited or replaced with new parameters.

`edit_method` function signature
---------------------------------

.. code-block:: python

     edit_model(model_type: str, simulations: Union[str, list], model_name: str, **kwargs)


``model_type`` : str, required
    Type of the model component to modify (e.g., 'Clock', 'Manager', 'Soils.Physical', etc.). Please see more :ref:`details here <model_List>`

``simulations`` : Union[str, list], optional
    A simulation name or list of simulation names in which to search. Defaults to all simulations in the model.

``model_name`` : str, required
    Name of the model instance to modify.

The following additional kwargs are specific to each each model type.

``**kwargs`` : dict, required

    - ``Weather``: requires a ``weather_file`` (str) argument, describing path to the ``.met`` weather file.

    - ``Clock``: Date properties such as ``Start`` and ``End`` in ISO format (e.g., '2021-01-01').

    - ``Manager``: Variables to update in the Manager script using ``update_mgt_by_path``. The parameters in a manager script are specific to each script. See :ref:`inspect_model_parameters:Inspect Model Parameters` for more details. for more details. for more details. on how to inspect and retrieve these paramters without opening the file in a GUI

    - ``Physical | Chemical | Organic | Water:``
      The supported key word arguments for each model type are given in the table below. Please note the values are layered and thus a ``str`` or ``list`` is accepted.
      when a value is supplied as ``str``, then it goes to the top soil layer. In case of a ``list``, value are replaced based on their respective index in the list.
      As a caution if the length of the list supplied exceeds the available number of layers in the profile, a ``RuntimeError`` during model ``runs`` will be raised.
      It is possible to target a specific layer(s) by supplying the location of that layer(s) using ``indices`` key word argument, if there is a need to target the bottom layer, use ``indices  = [-1]``

        +------------------+--------------------------------------------------------------------------------------------------------------------------------------+
        | Soil Model Type  | **Supported key word arguments**                                                                                                     |
        +==================+======================================================================================================================================+
        | Physical         | AirDry, BD, DUL, DULmm, Depth, DepthMidPoints, KS, LL15, LL15mm, PAWC, PAWCmm, SAT, SATmm, SW, SWmm, Thickness, ThicknessCumulative  |
        +------------------+--------------------------------------------------------------------------------------------------------------------------------------+
        | Organic          | CNR, Carbon, Depth, FBiom, FInert, FOM, Nitrogen, SoilCNRatio, Thickness                                                             |
        +------------------+--------------------------------------------------------------------------------------------------------------------------------------+
        | Chemical         | Depth, PH, Thickness                                                                                                                 |
        +------------------+--------------------------------------------------------------------------------------------------------------------------------------+
            - ``SurfaceOrganicMatter``
       - InitialCNR: (int)
       - InitialResidueMass (int)

    - ``Report``:
        - ``report_name`` (str): Name of the report model (optional depending on structure).
        - ``variable_spec`` (list[str] or str): Variables to include in the report.
        - ``set_event_names`` (list[str], optional): Events that trigger the report.

    - ``Cultivar``:
        - ``commands`` (str, required): APSIM path to the cultivar model to update.
        - ``values`` (Any. required): Value to assign.
        - ``new_cultivar_name`` (str, required): the new name for the edited cultivar.
        - ``cultivar_manager`` (str, required): Name of the Manager script managing the cultivar, which must contain the `CultivarName` parameter. Required to propagate updated cultivar values, as APSIM treats cultivars as read-only.

.. warning::
    Raises the following errors:

    ``ValueError``
        If the model instance is not found, required kwargs are missing, or `kwargs` is empty.

    ``NotImplementedError``
        If the logic for the specified `model_type` is not implemented.

.. seealso::

    - API description: :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model`
    - :ref:`model_List`

Quick Examples:

.. code-block:: python
        print('start')
        from apsimNGpy.core.apsim import ApsimModel
        model = ApsimModel(model='Maize')
        print(model)

Edit a cultivar model:

.. code-block:: python

    model.edit_model(
        model_type='Cultivar',
        simulations='Simulation',
        commands='[Phenology].Juvenile.Target.FixedValue',
        values=256,
        new_cultivar_name = 'B_110-e',
        model_name='B_110',
        cultivar_manager='Sow using a variable rule')

.. Hint::

    ``model_name: 'B_110'`` is an existing cultivar in the Maize Model, which we want to edit. Please note that editing a cultivar without specifying the  ``new_cultivar_name`` will throw a ``ValueError``.
    The name should be different to the the one being edited.

Edit a soil organic matter module:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Organic',
        simulations='Simulation',
        model_name='Organic',
        Carbon=1.23)

Edit multiple soil layers:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Organic',
        simulations='Simulation',
        model_name='Organic',
        Carbon=[1.23, 1.0])

Edit solute models:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Solute',
        simulations='Simulation',
        model_name='NH4',
        InitialValues=0.2)

    model.edit_model(
        model_type='Solute',
        simulations='Simulation',
        model_name='Urea',
        InitialValues=0.002)

Edit a manager script:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Manager',
        simulations='Simulation',
        model_name='Sow using a variable rule',
        population=8.4)

Edit surface organic matter parameters:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='SurfaceOrganicMatter',
        simulations='Simulation',
        model_name='SurfaceOrganicMatter',
        InitialResidueMass=2500)

    model.edit_model(
        model_type='SurfaceOrganicMatter',
        simulations='Simulation',
        model_name='SurfaceOrganicMatter',
        InitialCNR=85)

Edit Clock start and end dates:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Clock',
        simulations='Simulation',
        model_name='Clock',
        Start='2021-01-01',
        End='2021-01-12')

Edit report variables:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Report',
        simulations='Simulation',
        model_name='Report',
        variable_spec='[Maize].AboveGround.Wt as abw')

Multiple report variables:

.. code-block:: python

    model = ApsimModel(model='Maize')
    model.edit_model(
        model_type='Report',
        simulations='Simulation',
        model_name='Report',
        variable_spec=[
            '[Maize].AboveGround.Wt as abw',
            '[Maize].Grain.Total.Wt as grain_weight'
        ])


If you prefer little boiler plate code, we got you covered with ``edit_model_by_path``
The `edit_model_by_path` method enables surgical model editing by using the full
APSIM component path to identify the exact target node. This direct addressing
avoids the need for recursive tree traversal, name-matching, or guessing which
simulation contains the intended model. As a result, users
can modify parameters reliably even in complex, deeply nested APSIM structures. Please refer to functional signature and examples

.. code-block:: python

   with ApsimModel(model='Maize') as model:
        model.edit_model_by_path(path, **kwargs)

.. hint::

   The method :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model_by_path` from :class:`~apsimNGpy.core.apsim.ApsimModel` class operates on the same principle as :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model`, where each model type requires specific keyword arguments.
   For example, let’s edit a manager script: ``"Sow using a variable rule"`` that performs sowing operations such as plant population, sowing date etc.

.. code-block:: python

    with ApsimModel(model='Maize') as model
         model.edit_model_by_path(path = '.Simulations.Simulation.Field.Sow using a variable rule', Population =12)

.. warning::

    When using the full path, keep in mind that it inherently references a specific model type. The edit_model_by_path method internally detects this type and applies the appropriate logic.
    Therefore, if you supply an argument that is not valid for that model type, a ``ValueError`` will be raised.

.. tip::
   if in doubt, use ``detect_model_type`` followed by the corresponding full model path or use :meth:`~apsimNGpy.core.apsim.ApsimModel.inspect_file`

.. code-block:: python

   with ApsimModel(model='Maize')
       model_type = model.detect_model_type('.Simulations.Simulation.Field.Sow using a variable rule')
   # outputs: Models.Manager

.. include:: edit_by_path.rst

Editing nested simulation models
================================
apsimNGpy provides robust capabilities for editing and inspecting deeply nested APSIM NG models,
including models containing multiple simulations that users may wish to run in combination with different
inputs. The example below demonstrates the two complementary strategies for targeted modification—exclusion
and specification. Some of these ideas have already been introduced implicitly; for instance, edit_model_by_path
is an exclusion-based, surgical editing method that applies changes only to the model component identified by its full path.
More generally, the broader edit_model function offers two useful arguments—simulations and exclude—that
allow users to explicitly select which simulations should receive an edit and which should be omitted, as illustrated in the example that follows.

.. tip::

    After editing the file or model, you can save the file using the :meth:`~apsimNGpy.core.apsim.ApsimModel.save` method. This method takes a single argument: the desired file path or name.
    Without specifying the full path to the desired storage location, the file will be saved in the current working directory.

.. code-block:: python

    model.save('./edited_maize_model.apsimx')


.. seealso::

   - save: :meth:`~apsimNGpy.core.apsim.ApsimModel.save`
   - results retrieval API: :attr:`~apsimNGpy.core.apsim.ApsimModel.results`

.. seealso::

   - :ref:`API Reference <api_ref>`
   - :ref:`apsimNGpy Cheat sheat <cheat>`
   - :ref:`Inspecting Model Parameters <inspect_params>`
   - :ref:`APSIM Model types <model_List>`
   - :ref:`Go back to the home page<master>`


