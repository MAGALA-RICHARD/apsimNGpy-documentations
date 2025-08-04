 Version Control and APSIM Compatibility in apsimNGpy
====================================================

The `apsimNGpy` package is designed to interface tightly with the APSIM Next Generation (APSIM NG) platform. As APSIM NG is under continuous development, changes in its internal structure, APIs, or file formats may occasionally lead to version-breaking issues that impact `apsimNGpy` functionality.


To manage this, an automated robot runs **every two days** to check for new APSIM NG development releases. The robot performs the following tasks:

1. **Downloads and installs** the latest APSIM NG development version.
2. **Runs the complete `apsimNGpy` unit test suite** against the new APSIM version.
3. **Sends a detailed report** of the test outcomes to the `apsimNGpy` administrators.
4. If all tests **pass successfully**, the new APSIM version is marked as the `latestunit apsimNGpy::version` and is published on the documentation homepage.

This ensures that users always have access to a known-compatible APSIM version when using `apsimNGpy`.

In Case of Errors
========================

If the automated test suite identifies **breaking changes** or **errors**, these are reviewed and addressed manually by the maintainers. The resolution time may vary depending on administrator availability.

During this period:

* **Bug fixes and patches** may be rolled out.
* Compatibility notes or temporary workarounds may be posted on the repository or documentation site.

Best Practices for Users
==============================

To ensure smooth use of `apsimNGpy`, users are strongly encouraged to:

* **Check the documentation homepage** to confirm the current `latestunit apsimNGpy::version`.
* **Stay updated** with the most recent version of `apsimNGpy` to benefit from patches, improvements, and compatibility updates.
* If encountering issues with a new APSIM version, **fall back to a previously tested version** that is known to work with your current `apsimNGpy` setup.

Using version control wisely can save time, reduce debugging overhead, and ensure reproducibility in modeling workflows.

