apsimNGpy: API Reference
========================

apsimNGpy.parallel.process
--------------------------

.. py:function:: apsimNGpy.parallel.process.custom_parallel(func, iterable: 'Iterable', *args, **kwargs)

   Run a function in parallel using threads or processes.

   Parameters
   ----------
   func : callable
       The function to run in parallel.
   iterable : iterable
       An iterable of items to be processed by ``func``.
   *args
       Additional positional arguments to pass to ``func``.

   Yields
   ------
   Any
       The result of ``func`` for each item in ``iterable``.

   Other Parameters
   ----------------
   use_thread : bool, optional, default=False
       If ``True``, use threads; if ``False``, use processes (recommended for CPU-bound work).
   ncores : int, optional
       Number of worker threads/processes. Defaults to ~50% of available CPU cores.
   verbose : bool, optional, default=True
       Whether to display a progress indicator.
   progress_message : str, optional
       Message shown alongside the progress indicator.
       Defaults to ``f"Processing multiple jobs via {func.__name__}, please wait!"``.
   void : bool, optional, default=False
       If ``True``, consume results internally (do not yield). Useful for
       side-effect–only functions.
   unit : str, optional, default="iteration"
       Label for the progress indicator (cosmetic only).

   Examples
   --------
   Run with processes (CPU-bound):

   >>> list(run_parallel(work, range(5), use_thread=False, ncores=4))

   Run with threads (I/O-bound):

   >>> for _ in run_parallel(download, urls, use_thread=True, verbose=True):
   ...     pass

.. py:function:: apsimNGpy.parallel.process.custom_parallel_chunks(func: 'Callable[..., Any]', jobs: 'Iterable[Iterable[Any]]', *args, **kwargs)

   Run a function in parallel using threads or processes.
   The iterable is automatically divided into chunks, and each chunk is submitted to worker processes or threads.

   Parameters
   ----------
   func : callable
       The function to run in parallel.

   iterable : iterable
       An iterable of items that will be processed by ``func``.

   *args
       Additional positional arguments to pass to ``func``.

   Yields
   ------
   Any
       The results of ``func`` for each item in the iterable.
       If ``func`` returns ``None``, the results will be a sequence of ``None``.
       Note: The function returns a generator, which must be consumed to retrieve results.

   Other Parameters
   ----------------
   use_thread : bool, optional, default=False
       If ``True``, use threads for parallel execution;
       if ``False``, use processes (recommended for CPU-bound tasks).

   ncores : int, optional
       Number of worker processes or threads to use.
       Defaults to 50% of available CPU cores.

   verbose : bool, optional, default=True
       Whether to display a progress bar.

   progress_message : str, optional
       Message to display alongside the progress bar.
       Defaults to ``f"Processing multiple jobs via {func.__name__}, please wait!"``.

   void : bool, optional, default=False
       If ``True``, results are consumed internally (not yielded).
       Useful for functions that operate with side effects and do not return results.

   unit : str, optional, default="iteration"
       Label for the progress bar unit (cosmetic only).

   n_chunks : int, optional
       Number of chunks to divide the iterable into.
       For example, if the iterable length is 100 and ``n_chunks=10``, each chunk will have 10 items.

   chunk_size : int, optional
       Size of each chunk.
       If specified, ``n_chunks`` is determined automatically.
       For example, if the iterable length is 100 and ``chunk_size=10``, then ``n_chunks=10``.

