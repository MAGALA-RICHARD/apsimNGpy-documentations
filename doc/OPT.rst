
Single-Objective Optimization with apsimNGpy
============================================

Optimization is the science of selecting the best input values (decision variables) to achieve a desired output (objective). In the context of crop modeling, this might mean finding the optimal fertilizer rate or planting density to maximize yield or minimize nutrient leaching. Optimization problems can be:

- Single-objective (e.g., maximize yield)
- Multi-objective (e.g., maximize yield while minimizing nitrate leaching, covered in the next tutorial)
- Continuous (variables take any value within bounds)
- Discrete or categorical (variables take on fixed options)
- Mixed (a combination of variable types)

The apsimNGpy package provides a comprehensive framework for optimizing both single- and multi-objective problems through the ``apsimNGpy.optimizer`` module. Users can define decision variables (also known as control variables) associated with various APSIM components such as cultivars, manager scripts, and soil properties—for example, fertilization rate or sowing density.

The module supports a wide range of built-in performance metrics including ``mse, rmse, rrmse, ccc, and wia`` etc, which are available as attributes of the optimization classes. These metrics allow users to define appropriate loss functions that compare predicted values against observations.

Once the objective function (e.g., minimizing ``RMSE`` or maximizing mean yield) is specified, users can run supported solvers to find optimal configurations of the decision variables.

Demonstration
^^^^^^^^^^^^^

.. code-block:: python

    from apsimNGpy.optimizer.single import ContinuousVariable, MixedVariable
    from apsimNGpy.core.apsim import ApsimModel

.. admonition:: Explanation

    * ``ApsimModel```: used to initialise apsim model and handles model simulation and editing
    * ``ContinuousVariable``: wraps your problem setup for continuous variables
    * ``MixedVariable``: wraps your problem setup for mixed variables


Load the APSIM model. This is typically a single simulation file you want to calibrate or optimize.

.. code-block:: python

   maize_model = ApsimModel("Maize") # replace with the template path

.. note::

  You should be familiar with the structure of the model, including available report tables, as we will be calling the results method on this model object. It is assumed that the model is correctly configured and ready for use.

.. tip::

   Use the inspection or edit methods available in apsimNGpy to customize your model, or use the graphical user interface

.. attention::

    Sometimes we want to train our model using observed data (e.g., yield, soil carbon, etc.), so we need to load it as well. Please note that this is just a made-up example and not real data
.. code-block:: python

    obs = [
        7000.0, 5000.505, 1000.047, 3504.000, 7820.075,
        7000.517, 3587.101, 4000.152, 8379.435, 4000.301
    ]

.. hint::

   Observed data should always match the predicted data.

Minimizing continuous variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These parameters—such as sowing density, nitrogen application rate, irrigation thresholds, or cultivar-specific coefficients—are often continuous in nature. here, I describe two ways of how to deal with them in apsimNGpy

- 1. Inheriting from ``ContinuousVariable`` class.

.. hint::

     A common and effective approach is to define a custom optimization problem class and override the evaluate_objectives() method to implement your specific objective function.

.. code-block:: python

    class Problem(ContinuousVariable):
        def __init__(self, apsim_model, obs):
            super().__init__(apsim_model=apsim_model)
            self.obs = obs

        def evaluate_objectives(self, **kwargs):
            # This function runs APSIM and compares the predicted maize yield results with observed data.
            predicted = self.apsim_model.run(verbose=False).results.Yield
            # Use root mean square error or another metric.
            return self.rmse(self.obs, predicted)

    problem = Problem(maize_model, obs)


.. admonition:: Explanation

    In this example, a custom optimization problem is defined by subclassing ``ContinuousVariable``.
    The class is tailored to work with a specific APSIM model and a corresponding set of observed data.

    The observed values (e.g., actual maize yield from experiments or field trials) are passed to the constructor and stored as an attribute ``self.obs``. This enables the model’s predicted values to be evaluated directly against real-world data.

    The core logic resides in the ``evaluate_objectives()`` method, which runs the APSIM simulation and retrieves the predicted yield. It then computes the **Root Mean Square Error (RMSE)** between the predicted and observed values.

    Since ``RMSE`` quantifies prediction error, and **lower values indicate better model performance**, this setup implicitly tells the optimizer to search for parameter values that minimize RMSE. In effect, this drives the optimization process toward solutions that better match the observed system behavior.

-2.  Alternatively, you can define the objective directly. This is useful for simpler problems where you only need to extract something from the APSIM report table.

.. code-block:: python

    def maximize_yield(df):
        # Negate yield to convert to a minimization problem
        return -df.Yield.mean()

    problem = ContinuousVariable(maize_model, objectives = maximize_yield)

No, time to add  the control variables (i.e., what you want the optimizer to change) or variables that will control the outcomes of our objective values
 - You can use 'add_control' to specify the path, type, and bounds.


.. code-block:: python

    problem.add_control(
        path='.Simulations.Simulation.Field.Fertilise at sowing',
        Amount="?", bounds=[50, 300], v_type='int', start_value=150
    )
    problem.add_control(
        path='.Simulations.Simulation.Field.Sow using a variable rule',
        Population="?", v_type='int', bounds=[4, 14], start_value=8
    )

 .. hint::

   - 'Amount' will be filled in by the optimizer. '?' marks the variable to optimize. it is possible to supply extra parameters associated with any of the model path, this is important if you want to change them on the fly, but you dont want to optimize them. let's see an example

The manager script ``Simulations.Simulation.Field.Sow using a variable rule`` includes another parameter called ``CultivarName``. Let's change its value to 'B_110'

.. code-block:: python

     problem.add_control(
        path='.Simulations.Simulation.Field.Fertilise at sowing', CultivarName= 'B_110',
        Amount="?", bounds=[50, 300], v_type='int', start_value=150
    )

 Run a local optimization solver. This is suitable for smooth problems and quick feedback.

.. code-block:: python

    res_local = problem.minimize_with_alocal_solver(
        method='Powell',
        options={
            'maxiter': 100,
            'disp': True
        }
    )

.. admonition:: Explanation

    In this example, we use a **local optimization algorithm** to minimize the objective function defined in our custom `Problem` class. Local optimizers are generally efficient and fast, making them suitable for problems where:

    - The objective function is **smooth** (i.e., differentiable or continuous).
    - The problem is likely **unimodal**, meaning it has a single global minimum.
    - You need **quick feedback** for parameter tuning or iterative experimentation.

    Here, the method used is ``'Powell'``, a **derivative-free** optimization algorithm that performs a directional search in successive, conjugate directions. It is robust for many types of problems, especially when gradient information is unavailable.

The `minimize_with_alocal_solver()` method is a wrapper around `scipy.optimize.minimize`, making it easy to plug in a solver of your choice while passing solver-specific options.


When optimizing complex models such as APSIM simulations, the shape of the objective function surface can significantly impact the choice of optimization strategy.

Local optimizers (e.g., 'Powell', 'Nelder-Mead', 'L-BFGS-B') are designed to find a minimum near the starting point. They work well when the objective function is smooth, differentiable, and unimodal (i.e., has a single minimum). However, in problems where the surface is noisy, non-convex, or contains multiple local minima, these methods often get "trapped" in suboptimal solutions.

In contrast, global optimizers like differential evolution (DE) are designed to explore the entire search space. DE is a stochastic population-based algorithm that samples multiple candidate solutions and evolves them over generations. This makes it well-suited for:

    - Noisy objective functions

    - Highly non-linear problems

    - Multi-modal landscapes (i.e., many local minima)

    - Black-box functions where gradients are unavailable or unreliable

.. note::

    Although global optimizers may require more function evaluations and run time, they provide a more robust search and are less likely to miss the global minimum—especially in complex systems like agroecosystem models.

.. code-block:: python

    # STEP 4B: Run a global optimizer using differential evolution
    # This is useful when the surface is noisy or has many local minima.
    res_de = problem.minimize_with_de(
        popsize=10,
        maxiter=100,
        polish=False  # Set to True if you want to refine with a local solver at the end
    )

Mixed-Variable Optimization in apsimNGpy
============================================

.. important::

    While continuous-variable optimization is often considered straightforward—where parameters can smoothly vary within defined bounds—real-world agroecosystem modeling problems are rarely that simple. Many decision variables are not continuous but instead:

    - Take on categorical values (e.g., cultivar type or fertilizer formulation),

    - Follow discrete steps (e.g., plant density in fixed intervals),

    - Or must be selected from a fixed grid of management practices (e.g., irrigation schedules, sowing dates).

    These challenges make optimization more complex, as standard solvers typically assume a continuous search space.


To tackle this, APSIMNGpy provides the ``MixedVariable`` class, which allows users to define optimization problems involving a mixture of variable types:

    - Continuous (float-valued)

    - Quantized integers (step-wise discrete values)

    - Categorical (unordered choices)

This abstraction allows you to work seamlessly with APSIM models by recasting all variables internally into a continuous representation, while still respecting their original type during evaluation.

Using MixedVariable in Practice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The example below demonstrates how to define and solve a mixed-variable optimization problem using APSIMNGpy. We'll configure a maize model to maximize yield by tuning both:

    - A categorical fertilizer rate, and

    - A quantized sowing density.

print('Testing mixed variable optimization...')

You can then optimize this setup using either local or global solvers, as shown in the rest of the tutorial.

.. code-block:: python

    from apsimNGpy.optimize import MixedVariable

    # Define the optimization problem
    problem = MixedVariable(maize_model, objectives=maximize_yield)

    # Add a categorical (choice-based) variable
    problem.add_control(
        path='.Simulations.Simulation.Field.Fertilise at sowing',
        Amount="?",
        v_type='choice',
        categories=[100, 150, 200, 250, 300],
        start_value=150
    )

    # Add a quantized integer variable with fixed step size
    problem.add_control(
        path='.Simulations.Simulation.Field.Sow using a variable rule',
        Population="?",
        v_type='qrandint',
        bounds=[4, 14],
        start_value=8,
        q=2
    )

.. hint::

    You can then optimize this setup using either local or global solvers, as shown in the rest of the tutorial.


Review optimization results
^^^^^^^^^^^^^^

.. code-block:: python

    print(problem)

Summary
^^^^^^^^^^^

+-----------------------+---------------------------+-------------------------------+
| Feature               | Local Solver (e.g, Powell)| Global Solver (DE)            |
+=======================+===========================+===============================+
| Speed                 | Fast                      | Slower                        |
+-----------------------+---------------------------+-------------------------------+
| Risk of local traps   | High                      | Low                           |
+-----------------------+---------------------------+-------------------------------+
| Use case              | Smooth, simple surfaces   | Rugged, multi-modal surfaces  |
+-----------------------+---------------------------+-------------------------------+


