Editing Model Parameters
===========================================

Editing a model involves changing model parameter values. This task can be accomplished via a unified method called ``edit_model`` from ``CoreModel`` or ``ApsimModel`` Class
by specifying the model type, name and simulation name.

edit_method function signature

.. code-block:: python

     edit_model(model_type: str, simulations: Union[str, list], model_name: str, **kwargs)

Parameters
----------
``model_type`` : str
    Type of the model component to modify (e.g., 'Clock', 'Manager', 'Soils.Physical', etc.).

``simulations`` : Union[str, list], optional
    A simulation name or list of simulation names in which to search. Defaults to all simulations in the model.

``model_name`` : str
    Name of the model instance to modify.

``**kwargs`` : dict
    Additional keyword arguments specific to the model type. These vary by component:

    - ``Weather``:
        - ``weather_file`` (str): Path to the weather ``.met`` file.

    - ``Clock``:
        - Date properties such as ``Start`` and ``End`` in ISO format (e.g., '2021-01-01').

    - ``Manager``:
        - Variables to update in the Manager script using `update_mgt_by_path`.
        The parameters in a manager script are specific to each script. See :ref:`inspect_model_parameters:Inspect Model Parameters` for more details. for more details. for more details. on how to inspect and retrieve these paramters without opening the file in a GUI

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
        - ``commands`` (str): APSIM path to the cultivar model to update.
        - ``values`` (Any): Value to assign.
        - ``cultivar_manager`` (str): Name of the Manager script managing the cultivar, which must contain the `CultivarName` parameter. Required to propagate updated cultivar values, as APSIM treats cultivars as read-only.

Raises
^^^^^^^^
``ValueError``
    If the model instance is not found, required kwargs are missing, or `kwargs` is empty.

``NotImplementedError``
    If the logic for the specified `model_type` is not implemented.

Examples::

        from apsimNGpy.core.apsim import ApsimModel
        model = ApsimModel(model='Maize')

Edit a cultivar model::

    model.edit_model(
        model_type='Cultivar',
        simulations='Simulation',
        commands='[Phenology].Juvenile.Target.FixedValue',
        values=256,
        model_name='B_110',
        cultivar_manager='Sow using a variable rule')

Edit a soil organic matter module::

    model.edit_model(
        model_type='Organic',
        simulations='Simulation',
        model_name='Organic',
        Carbon=1.23)

Edit multiple soil layers::

    model.edit_model(
        model_type='Organic',
        simulations='Simulation',
        model_name='Organic',
        Carbon=[1.23, 1.0])

Edit solute models::

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

Edit a manager script::

    model.edit_model(
        model_type='Manager',
        simulations='Simulation',
        model_name='Sow using a variable rule',
        population=8.4)

Edit surface organic matter parameters::

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

Edit Clock start and end dates::

    model.edit_model(
        model_type='Clock',
        simulations='Simulation',
        model_name='Clock',
        Start='2021-01-01',
        End='2021-01-12')

Edit report variables::

    model.edit_model(
        model_type='Report',
        simulations='Simulation',
        model_name='Report',
        variable_spec='[Maize].AboveGround.Wt as abw')

Multiple report variables::

    model.edit_model(
        model_type='Report',
        simulations='Simulation',
        model_name='Report',
        variable_spec=[
            '[Maize].AboveGround.Wt as abw',
            '[Maize].Grain.Total.Wt as grain_weight'
        ])


