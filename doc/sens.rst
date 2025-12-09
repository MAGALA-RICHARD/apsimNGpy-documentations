Sensitivity Analysis in apsimNGpy
=================================

Sensitivity analysis in ``apsimNGpy`` implements the same established
methods used in APSIM—namely the **Morris Elementary Effects** method and
the **Sobol variance–based method**. The key difference is flexibility:
``apsimNGpy`` allows you to **construct a sensitivity analysis directly from
any APSIM template file**, including the model you are actively developing.
With only a few lines of Python code, you can specify the sensitivity
method, configure the factors, build the sensitivity model, and execute it.

In contrast to the APSIM GUI, which provides graphical representations and
interactive controls, the Python interface expects the user to understand
the fundamentals of the analysis being performed. ``apsimNGpy`` does not
generate graphical summaries automatically. However, interpretation is not
lost—APSIM’s native sensitivity outputs remain accessible, and the
``SensitivityManager`` class provides convenient access points for
visualization and custom analysis, enabling you to create your own plots
using Matplotlib, Seaborn, or other Python libraries.

The workflow for creating a sensitivity analysis is conceptually similar to
setting up factorial experiments: define the method, specify the factors,
build the sensitivity experiment node, and run the simulations. The example
below shows a minimal, practical workflow for constructing a sensitivity
analysis directly from Python.

.. tip::

   ``apsimNGpy`` is designed to integrate sensitivity analysis seamlessly
   into reproducible pipelines. Because everything is defined in Python,
   you can version-control the full sensitivity experiment, regenerate it
   consistently, and run it across multiple APSIM templates or scenarios.

Workflow Overview
-----------------

The sensitivity analysis workflow in ``apsimNGpy`` follows a structured,
reproducible sequence of steps. The process is designed to mirror APSIM’s
internal sensitivity framework while providing full programmatic control in
Python. The key stages are:

1. **Initialize the manager instance**
   Create a ``SensitivityManager`` object using your APSIM template file.
   This instance will hold the experiment configuration and manage all
   subsequent steps.

2. **Define sensitivity factors**
   Add one or more factors (parameters) to the manager instance. Each factor
   corresponds to an APSIM model path and a numerical range to be explored.
   Factors are defined using methods on the instantiated ``SensitivityManager``
   object.

3. **Build the sensitivity simulation model**
   Construct the sensitivity experiment node within the APSIM file.
   During this step the user:

   - selects the sensitivity method (Morris or Sobol),
   - specifies the database table name for storing results,
   - determines the aggregation column used to summarize outputs,
   - and, when using the Morris method:
     - sets the number of jumps,
     - defines the number of intervals,
     - and optionally customizes the step size ``Δ``.

   For **all** sensitivity methods, this step also sets the number of
   parameter paths, which controls the total number of simulations executed.

4. **Run the sensitivity simulations**
   Execute the sensitivity experiment. ``apsimNGpy`` automatically handles
   model expansion, path construction, execution, and data storage.


Workflow Diagram
----------------

::

        +-----------------+       +----------------------+
        |instantiate class |----> |  define parameters      |
        +-----------------+       +----------------------+
                   |                       |
                   v                       v
        +-----------------+       +----------------------+
        |  Build Node     |-----> |  Run Simulations     |
        +-----------------+       +----------------------+

Step 1.

.. code-block:: python

     from apsimNGpy.core import senstivitymanager import SensitivityManager
     exp = SensitivityManager("Maize", out_path='sob.apsimx')

Step 2.

.. code-block:: python

     exp.add_sens_factor(name='cnr', path='Field.SurfaceOrganicMatter.InitialCNR', lower_bound=10, upper_bound=120)
     exp.add_sens_factor(name='cn2bare', path='Field.Soil.SoilWater.CN2Bare', lower_bound=70, upper_bound=100)

Step 3.

.. code-block:: python