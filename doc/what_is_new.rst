.. what_is_new

What is New in **apsimNGpy 1.0.0**
========================================
**apsimNGpy 1.0.0** represents a major milestone in the development of the framework, transitioning from an experimental research tool to a stable, production-ready release. This version consolidates years of development and introduces several key improvements in performance, usability, reproducibility, and analytical capability.

1. Stable, Reproducible Release
=======================================
* First **official 1.0.0** version, signifying a **stable API** and backward compatibility guarantee for future minor releases.

2. Core Engine Improvements
=================================
* **Refactored multiprocessing engine** for robust, scalable execution across multiple CPU cores, including safer handling of parallel APSIM runs on Windows.
* **Improved failure reporting** and retry mechanisms with configurable policies (e.g., `tenacity`-based retries), reducing silent errors in large batch jobs.
* **Improve job submissions** allowing edits to be submitted simulataneusly.

3. Enhanced Spatial Optimization Integration
====================================================
* Fully integrated framework coupling **APSIM**, the **Agricultural Conservation Planning Framework (ACPF)**, and **NSGA-II** for spatial optimization.
* Enables explicit trade-off analysis between production and environmental objectives at field and watershed scales.
* Supports new normalization and summary statistics logic for multi-objective evaluation.

4. Expanded Sensitivity & Uncertainty Analysis
===================================================
* Updated **Sobol sampling** with configurable skip values for improved space-filling design.
* Clean handling of **calc_second_order** options with consistent propagation between sampling and analysis layers.
* Support for additional SALib methods with stable default parameterizations.

5. Improved Database & Output Management
===============================================
* **Schema-hash table naming** to avoid SQLite collisions in parallel executions.
* Stable persistence layer with:
  * deterministic table identifiers
  * execution and process metadata
  * large result handling with chunked writes and WAL support
* Cleaner error handling for results writes under heavy parallel loads.

6. Workflow & Developer Quality-of-Life
===========================================
* Modular, environment-aware `.bat` and `uv` workflows for consistent environment management across Windows and cross-platform environments.
* Cleaned and **modularized dependency structure**, enabling smaller core installs and optional GIS/plotting/optimization profiles.
* Support for locked Python versions via `uv python list` and `.python-version` files.

7. Fixes & Stability Enhancements
==================================
* Resolution of common parallel SQLite locking issues under heavy batch throughput.
* Deterministic hashing for table identifiers even in multiprocessing contexts.
* Guidance and preflight validation for schema drift, unsupported data types, and mixed index/column structures.
* Better error reporting for model editing callbacks and APSIM parameter sets.

Summary
============
**apsimNGpy 1.0.0** delivers:

* A stable, reproducible foundation for agri-environmental modeling workflows
* Scalability for large batch and multi-objective experiments
* Better integration of APSIM with decision support, sensitivity, and spatial optimization routines
* An enduring API that is resilient and robust under a wide range of uncertainties

This release establishes a platform for future enhancements while remaining reliable for academic and applied research in productivity, environmental impacts, and landscape planning.

