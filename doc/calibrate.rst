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
=================================

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


- **candidate_param**: str — the specific model parameter(s) to be calibrated.

- **other_params**: dict — any additional fixed parameters required by the APSIM component to compute or update the variable of interest.
  For details see :meth:`~apsimNGpy.core.apsim.ApsimModel.edit_model_by_path`

- **cultivar**: bool to signal to apsimNGpy that the parameters on this node are cultivar specific call the relevant editor

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
  if you are Operations, it is not currently supported

Submitting the define factor
------------------------------
.. code-block:: python

        # Submit optimization factors
        #mp.submit_factor(**soil_param)
        mp.submit_factor(**rue)
       # mp.submit_factor(**cultivar_param)

        print(f" {mp.n_factors} optimization factors registered.")

        # -------------------------------------------------------------
        # 3. Configure and execute the optimizer
        # -------------------------------------------------------------
        from scipy.optimize import NonlinearConstraint


        def hess(x):
            return np.zeros((len(x), len(x)))
        minim = MixedVariableOptimizer(problem=mp)
        nlc = NonlinearConstraint(mp.evaluate_objectives, lb=-1.1, ub=-0.98)
        #tc=minim.minimize_with_local(method="trust-constr", constraints=[nlc],  # or empty list if you don't want nonlinear constraints
        #options={"verbose": 3}, hess=hess )
        #print(tc)
        de = minim.minimize_with_de(
            use_threads=True,
            updating="deferred",
            workers=14,  # Number of parallel workers
            popsize=30,  # Population size per generation
            constraints=nlc,
        )
        print(de)
        # (a) Local optimization examples
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

