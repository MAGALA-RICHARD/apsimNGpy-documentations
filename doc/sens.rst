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


Workflow Diagram
----------------

The sensitivity analysis process in ``apsimNGpy`` consists of four stages:

1. **Define factors**
   Each factor maps to an APSIM model path and a range of possible values.

2. **Select method**
   Choose between Morris or Sobol.

3. **Build sensitivity experiment**
   ``SensitivityManager`` injects a sensitivity node into your APSIM file.

4. **Run and interpret**
   Execute the analysis and evaluate APSIM’s native output products.

::

        +-----------------+       +----------------------+
        |  Define Factors |-----> |  Select Method       |
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
