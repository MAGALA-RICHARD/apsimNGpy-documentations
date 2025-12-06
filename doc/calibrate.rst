Parameter calibration
======================
This tutorial demonstrates how to automatically calibrate APSIM parameters using the optimization algorithms
available in apsimNGpy. For detailed information on defining and submitting optimization factors,
refer to the API documentation for :meth:`~apsimNGpy.optimizer.problems.smp.MixedProblem.submit_factor`.


.. code-block:: python

        import numpy as np
        from apsimNGpy.core.config import apsim_bin_context
        with apsim_bin_context(apsim_bin_path=r'bin_dist/APSIM2025.8.7844.0/bin'):
            from apsimNGpy.optimizer.minimize.single_mixed import MixedVariableOptimizer
            from apsimNGpy.optimizer.problems.smp import MixedProblem
            from apsimNGpy.tests.unittests.test_factory import obs# mimics observed data
            from apsimNGpy.optimizer.problems.variables import UniformVar, QrandintVar

Some algorithms like Differential Evolution can be set to run in parallel, therefore everything needs to be executed below the module guard

Defining the Optimization Problem
----------------------------------

To define an optimization problem that identifies the optimum APSIM parameters, use the class :class:`~apsimNGpy.optimizer.minimize.single_mixed.MixedProblem`.
This class accepts an APSIM template file, a training (observed) dataset, and the corresponding index variables linking observed and simulated data.

A key requirement is to specify a performance metric that serves as the optimization target. This metric guides the algorithm in assessing model performance and convergence quality.
Commonly used metrics include WIA, RMSE, RRMSE, Bias, CCC, R², Slope, ME, and MAE.

An example usage is shown below.

.. code-block:: python

    if __name__ == "__main__":
        # -------------------------------------------------------------
        # 1. Define the mixed-variable optimization problem
        # -------------------------------------------------------------
        mp = MixedProblem(
            model="Maize",
            trainer_dataset=obs,
            pred_col="Yield",
            metric="wia",
            index="year",
            trainer_col="observed"
        )

Defining the factors
---------------------
Once the optimization problem is instantiated, the remaining task is to submit the factors, the parameters that will be sampled during the search process.
These factors finalize the problem specification and determine the parameter space over which the optimization algorithm will operate.

Each factor requires a set of python parameters that define how it will be sampled and handled by apsimNGpy execution engine.
For example, the dictionary below specifies the target model path, the variable type and sampling range,
the starting value, the candidate parameter to modify, and any additional parameters needed by the APSIM model component.

.. code-block:: python

        soil_param = {
            "path": ".Simulations.Simulation.Field.Soil.Organic",
            "vtype": [UniformVar(1, 200)],
            "start_value": [1],
            "candidate_param": ["FOM"],
            "other_params": {"FBiom": 0.04, "Carbon": 1.89},
        }

In general as seen in the example above, the keys in the dictionary above can be broken down as follows;

- **path**: a fully qualified model path pointing to the APSIM component to be edited. For extracting this path, please see :ref:`inspect model section <plain_inspect>`

- **vtype**: A list defining the variable types used for sampling parameter values
  (e.g., ``UniformVar``, ``GridVar``, ``CategoricalVar``). Variable types may also
  be provided as strings.

  Supported Variable Types
  ------------------------

  1. **ChoiceVar(items)**
     Nominal (unordered categorical)
     Example: ``ChoiceVar(["A", "B", "C"])``

  2. **GridVar(values)**
     Ordinal (ordered categorical)
     Example: ``GridVar([2, 4, 8, 16])``

  3. **RandintVar(lower, upper)**
     Integer in ``[lower, upper]``
     Example: ``RandintVar(0, 6)``

  4. **QrandintVar(lower, upper, q)**
     Quantized integer with step ``q``
     Example: ``QrandintVar(0, 12, 3)``

  5. **UniformVar(lower, upper)**
     Continuous float range
     Example: ``UniformVar(0.0, 5.11)``

  6. **QuniformVar(lower, upper, q)**
     Quantized float with step ``q``
     Example: ``QuniformVar(0.0, 5.1, 0.3)``

  Below is a list of allowable string names for each variable type.
  For further details, see :meth:`~apsimNGpy.optimizer.problems.smp.MixedProblem.submit_factor`.

  .. code-block:: python

        ALLOWED_VARIABLES = {
            # Original canonical names
            "UniformVar": UniformVar,
            "QrandintVar": QrandintVar,
            "QuniformVar": QuniformVar,
            "GridVar": GridVar,
            "ChoiceVar": ChoiceVar,
            "RandintVar": RandintVar,

            # Short aliases
            "uniform": UniformVar,
            "quniform": QuniformVar,
            "qrandint": QrandintVar,
            "grid": GridVar,
            "choice": ChoiceVar,
            "randint": RandintVar,

            # Descriptive aliases (readable English)
            "continuous": UniformVar,
            "quantized_continuous": QuniformVar,
            "quantized_int": QrandintVar,
            "ordinal": GridVar,
            "categorical": ChoiceVar,
            "integer": RandintVar,

            # Alternative descriptive (for domain users)
            "step_uniform_float": QuniformVar,
            "step_random_int": QrandintVar,
            "ordered_var": GridVar,
            "choice_var": ChoiceVar
        }


- **start_value**: A list of initial parameter values.
  Each entry corresponds to one parameter within the factor definition
  and is used to seed the optimizer or establish a baseline.


- **candidate_param**: list or tuple of str Names of APSIM variables (e.g., ``"FOM"``, ``"FBiom"``) to be optimized.
            These must exist within the APSIM node path.

- **other_params**: dict — Additional APSIM constants to fix during optimization (non-optimized). These must belong to the same APSIM node. For example, when optimizing ``FBiom`` but also modifying ``Carbon``, supply ``Carbon`` under ``other_params``
  For details see :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model_by_path`

- **cultivar**: bool  Indicates whether the parameter belongs to a cultivar node. Set to
            ``True`` when defining cultivar-related optimization factors.

.. tip::

    - Each distinct node on APSIM should appear in one single entry or submission, hence if they are multiple paramters on a single node, they should all be defined by a single entry
    - When a factor contains multiple parameters, the fields ``vtype``, ``start_value``, and ``candidate_param`` provided as a list must be the same size as the number of parameters to optimize on that node and should be the same length

For the example above, if multiple parameters at the same model path need to be optimized, they can be defined as follows:

.. code-block:: python

        soil_param = {
            "path": ".Simulations.Simulation.Field.Soil.Organic",
            "vtype": [UniformVar(1, 200), UniformVar(1, 3)],
            "start_value": [1, 2],
            "candidate_param": ["FOM", 'Carbon'],
            "other_params": {"FBiom": 0.04, },
        }

Cultivar-specific parameters can be defined as shown below. Note that if you do not explicitly set cultivar=True, the factor may still pass Pydantic validation,
but it will not be recognized correctly by apsimNGpy. As a result, an error will be raised when the optimizer starts.

.. code-block:: python

        cultivar_param = {
            "path": ".Simulations.Simulation.Field.Maize.CultivarFolder.Dekalb_XL82",
            "vtype": [ QrandintVar(400, 900, q=10), UniformVar(0.8,2.2)],  # Discrete step size of 2
            "start_value": [ 600, 1],
            "candidate_param": [
                                '[Phenology].GrainFilling.Target.FixedValue',
                                '[Leaf].Photosynthesis.RUE.FixedValue'],
            "other_params": {"sowed": True},
            "cultivar": True,  # Signals to apsimNGpy to treat it as a cultivar parameter
        }

cultivar specific paramters are still tricky, as there is need to specify whether the cultivar to be edited is the one specified in the manager script managing the sowing operations

.. note::
  If you are using Operations, it is not currently supported

Submit optimization factors
------------------------------

.. code-block:: python

        mp.submit_factor(**soil_param)
        # submit the cultivar one
        mp.submit_factor(**cultivar_param)

        print(f" {mp.n_factors} optimization factors registered.")
         #4 optimization factors registered.")

There is still a chance to submit all defined factors at once

.. code-block:: python

  mp.submit_all([soil_param,cultivar_param ])

.. tip::

       All submitted factors are validated using **Pydantic** to ensure adherence to
       expected data structures and variable types — for example checking that
       ``vtype`` includes valid variable types (``UniformVar``, ``GridVar``),
       ensuring ``path`` is a valid string, and that start_values is a string.

       After Pydantic validation, an additional structural check ensures that the
       lengths of ``vtype``, ``start_value``, and ``candidate_param`` are identical.
       Each candidate parameter must have a matching variable type and initial
       value.

       In cases where `other_params` has identical names as `candidate_param`, the `candidate_param`
       takes priority and the identical parameter is decoupled from the other_params

       Optimization methods that do not require bounded or initialized start
       values allow for dummy entries in ``start_value``. These placeholders are
       accepted without affecting the optimization process. The system remains
       flexible across both stochastic and deterministic search methods.

Configure the optimizer
--------------------------
.. code-block:: python

        minim = MixedVariableOptimizer(problem=mp)

Use differential evolution
---------------------------
apsimNGpy provides a high-level wrapper for Differential Evolution
(DE), enabling robust APSIM calibration without requiring users to
manage low-level evolutionary mechanics. DE is well suited to the
irregular, nonlinear parameter landscapes common in crop and soil
model calibration. Its population-based search balances broad
exploration with fine-scale refinement. Effective performance is
typically achieved using moderate population sizes (20–40), but you may consider making the population as 10 * number of parameters, mutation
factors between 0.6 and 0.9, and crossover rates between 0.7 and
0.9. For metrics where larger values indicate improved model
performance (such as WIA, CCC, R², and slope), apsimNGpy internally
transforms the problem into a minimization task, which requires
negative constraint bounds. Parallel execution via the ``workers``
argument is essential for reducing computation time during APSIM
simulations.

.. code-block:: python

        de = minim.minimize_with_de(
            use_threads=True,
            updating="deferred",
            workers=14,
            popsize=30,
            constraints=(-1.1, -0.8))
        print(de)


Local optimization examples
---------------------------
.. code-block:: python

        import gc
        gc.collect()
        nelda = minim.minimize_with_local(method="Nelder-Mead")
        print(nelda)
        powell = minim.minimize_with_local(method="Powell")
        print(powell)
        sqlp = minim.minimize_with_local(method="L-BFGS-B", options={
            "gtol": 1e-12,
            "ftol": 1e-12,
            "maxfun": 50000,
            "maxiter": 30000
        })

        print(sqlp)
        bfgs = minim.minimize_with_local(method="BFGS")
        print(bfgs)

        print("\nOptimization completed:")

After the optimization is completed, compare the simulated results with the training dataset
using the newly optimized parameters. The data attribute contains both the observed and simulated datasets, enabling direct comparison and evaluation of model performance.

.. code-block:: python

        import matplotlib.pyplot as plt
        import os
        # sns.relplot(x="year", y="y")
        plt.figure(figsize=(8, 6))
        df= de.data
        df.eval('ayield =Yield/1000', inplace=True)
        df.eval('oyield =observed/1000', inplace=True)
        # observed → scatter points
        plt.scatter(df["year"], df["ayield"], label="APSIM", s=60, color='red')
        # predicted → line
        plt.plot(df["year"], df["oyield"], label="Training data", linewidth=2)
        plt.xlabel("Time (Year)", fontsize=18)
        plt.ylabel("Maize grain yield (Mg ha⁻¹)", fontsize=18)
        plt.title("") #Observed vs Predicted Yield Over Time
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("figures.png")
        os.startfile("figures.png")
        plt.close()

Full tutorial code:
-------------------
.. code-block:: python

    import numpy as np
    from apsimNGpy.optimizer.minimize.single_mixed import MixedVariableOptimizer
    from apsimNGpy.optimizer.problems.smp import MixedProblem
    from apsimNGpy.optimizer.problems.variables import UniformVar, QrandintVar
    from apsimNGpy.tests.unittests.test_factory import obs
    if __name__ == "__main__":
        # -------------------------------------------------------------
        # 1. Define the mixed-variable optimization problem
        # -------------------------------------------------------------
        mp = MixedProblem(
            model="Maize",
            trainer_dataset=obs,
            pred_col="Yield",
            metric="wia",
            index="year",
            trainer_col="observed"
        )


        # (a) Continuous initial fresh soil organic matter factor
        soil_param = {
            "path": ".Simulations.Simulation.Field.Soil.Organic",
            "vtype": [UniformVar(1, 200)],
            "start_value": [1],
            "candidate_param": ["FOM"],
            "other_params": {"FBiom": 0.04, "Carbon": 1.89},
        }

        # (b) Cultivar-specific
        cultivar_param = {
            "path": ".Simulations.Simulation.Field.Maize.CultivarFolder.Dekalb_XL82",
            "vtype": [QrandintVar(400, 900, q=10), UniformVar(0.8, 2.2)],  # Discrete step size of 2
            "start_value": [600, 1],
            "candidate_param": [
                '[Phenology].GrainFilling.Target.FixedValue',
                '[Leaf].Photosynthesis.RUE.FixedValue'],
            "other_params": {"sowed": True},
            "cultivar": True,  # Signals to apsimNGpy to treat it as a cultivar parameter
        }
        # Submit optimization factors
        mp.submit_factor(**soil_param)
        mp.submit_factor(**cultivar_param)

        print(f" {mp.n_factors} optimization factors registered.")

        # -------------------------------------------------------------
        # 3. Configure and execute the optimizer
        # -------------------------------------------------------------
        minim = MixedVariableOptimizer(problem=mp)
        #_______________________________________________
        # use differential evolution
        de = minim.minimize_with_de(
            use_threads=True,
            updating="deferred",
            workers=14,  # Number of parallel workers
            popsize=30,  # Population size per generation
            constraints=(-1.1, -0.8),     # if metric indicator is one of wia, ccc , r2, slope the constraints must be negative
        )
        print("Differential evolution\n", de)
        # (a) Local optimization examples
        nelda = minim.minimize_with_local(method="Nelder-Mead")
        print('nelda\n', nelda)
        # if you wish to switch algorithm
        powell = minim.minimize_with_local(method="Powell")
        print('Powell', powell)
        sqlp = minim.minimize_with_local(method="L-BFGS-B", options={
            "gtol": 1e-12,
            "ftol": 1e-12,
            "maxfun": 50000,
            "maxiter": 30000
        })

        print('SQLP\n', sqlp)
        bfgs = minim.minimize_with_local(method="BFGS")
        print('bfgs\n', bfgs)

        print("\nOptimization completed:")
        # now plot the results
        import matplotlib.pyplot as plt
        import os
        plt.figure(figsize=(8, 6))
        df= de.data
        df.eval('ayield =Yield/1000', inplace=True)
        df.eval('oyield =observed/1000', inplace=True)
        # observed → scatter points
        plt.scatter(df["year"], df["ayield"], label="APSIM", s=60, color='red')
        # predicted → line
        plt.plot(df["year"], df["oyield"], label="Training data", linewidth=2)
        plt.xlabel("Time (Year)", fontsize=18)
        plt.ylabel("Maize grain yield (Mg ha⁻¹)", fontsize=18)
        plt.title("") #Observed vs Predicted Yield Over Time
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("figures.png")
        os.startfile("figures.png")
        plt.close()

