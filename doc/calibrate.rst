Parameter calibration
======================
This tutorial demonstrates how to calibrate APSIM parameters using the optimization algorithms
available in apsimNGpy. For detailed information on defining and submitting optimization factors,
refer to the API documentation for ~apsimNGpy.optimizer.smp.MixedProblem.submit_factor.


.. code-block:: python

        import numpy as np
        from apsimNGpy.core.config import apsim_bin_context
        with apsim_bin_context(apsim_bin_path=r'bin_dist/APSIM2025.8.7844.0/bin'):
            from apsimNGpy.optimizer.minimize.single_mixed import MixedVariableOptimizer
            from apsimNGpy.optimizer.problems.smp import MixedProblem
            from apsimNGpy.tests.unittests.test_factory import obs# mimics observed data
