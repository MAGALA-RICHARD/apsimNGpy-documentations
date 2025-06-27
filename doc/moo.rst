# How to Run Multi-Objective Optimization with apsimNGpy

This tutorial demonstrates how to perform multi-objective optimization on an APSIM Next Generation model using the `apsimNGpy.optimizer.moo` module. You will learn two ways to specify decision variables and how to run an evolutionary optimization algorithm using `pymoo`. This approach enables you to explore trade-offs between objectives like crop yield and environmental outcomes.

## Prerequisites

Make sure you have the following installed and configured:

* **APSIM Next Generation**
* **Python 3.8+**
* **apsimNGpy** package (latest version)
* Python packages: `pymoo`, `matplotlib`, `numpy`, and `pandas`

## Step 1: Import Required Modules

You need to import necessary components from `apsimNGpy.optimizer.moo` and supporting packages.

.. code-block:: python

    from apsimNGpy.optimizer.moo import ApsimOptimizationProblem, Runner, compute_hyper_volume, NSGA2
    from pymoo.optimize import minimize
    import matplotlib.pyplot as plt


* `Runner`: handles model simulation and editing
* `ApsimOptimizationProblem`: wraps your problem setup for `pymoo`
* `NSGA2`: a multi-objective genetic algorithm
* `minimize`: pymoo's driver for optimization

## Step 2: Initialize the APSIM Model Runner

You create a runner tied to a specific `.apsimx` model file. This runner manages simulation and parameter editing.

.. code-block:: python

    runner = Runner("Maize")
    runner.add_report_variable('[Soil].Nutrient.NO3.kgha[1] as nitrate', report_name='Report')


This ensures APSIM includes nitrate outputs in the report.

## Step 3a: Define Decision Variables (Approach 1 - Direct List)

You can directly supply a list of variables to optimize.

.. code-block:: python

```
decision_vars = [
    {'path': '.Simulations.Simulation.Field.Fertilise at sowing',
     'Amount': "?", 'bounds': [50, 300], 'v_type': 'float'},

    {'path': '.Simulations.Simulation.Field.Sow using a variable rule',
     'Population': "?", 'bounds': [4, 14], 'v_type': 'float'}
]

problem = ApsimOptimizationProblem(runner, objectives=[], decision_vars=decision_vars)
```

Each dictionary defines:

* `path`: the APSIM model path to the component
* `Amount` / `Population`: the parameter to be optimized (denoted by '?')
* `bounds`: lower and upper bounds for the optimizer
* `v_type`: variable type

## Step 3b: Define Decision Variables (Approach 2 - Using `.add_parameters()`)

Instead of a list, you can add each parameter one at a time.

.. code-block:: python

    problem = ApsimOptimizationProblem(runner, objectives=[])

    problem.add_parameters(
        path='.Simulations.Simulation.Field.Fertilise at sowing',
        Amount='?', bounds=[50, 300], v_type='float')

    problem.add_parameters(
        path='.Simulations.Simulation.Field.Sow using a variable rule',
        Population='?', bounds=[4, 14], v_type='float')


This method is more flexible for programmatically building problems.

## Step 4: Define Objective Functions

Objective functions take APSIM output (as a DataFrame) and return scalar values.

.. code-block:: python

    def negative_yield(df):
        return -df['Yield'].mean()

    def nitrate_leaching(df):
        return df['nitrate'].sum()

    problem.objectives = [negative_yield, nitrate_leaching]


You can define any number of such functions depending on the goals.

## Step 5: Run the NSGA-II Optimizer

NSGA-II is a commonly used algorithm for multi-objective problems. You can now run the optimization:

.. code-block:: python

    algorithm = NSGA2(pop_size=20)

    result = minimize(
        problem.get_problem(),
        algorithm,
        ('n_gen', 10),
        seed=1,
        verbose=True
    )


* `pop_size`: number of candidate solutions per generation
* `n_gen`: number of generations to run

## Step 6: Plot the Pareto Front

The results show trade-offs between competing objectives. You can visualize them:

.. code-block:: python

    F = result.F
    plt.scatter(F[:, 0], F[:, 1])
    plt.xlabel("Yield")
    plt.ylabel("N Leaching")
    plt.title("Pareto Front")
    plt.show()


## Step 7: Compute Hypervolume (Optional)

The hypervolume gives a scalar metric of solution quality.

.. code-block:: python

    hv = compute_hyper_volume(F, normalize=True)
    print("Hypervolume:", hv)


Summary
-------
This tutorial introduced you to setting up and running a multi-objective optimization on APSIM models using `apsimNGpy`. Both list-based and incremental parameter addition were demonstrated. You can now adapt this workflow for more complex calibration or decision-support tasks.

