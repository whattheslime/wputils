from asyncio import Queue, get_event_loop, create_task, gather
from functools import partial
from inspect import iscoroutinefunction


class AsyncQueue:
    """AsyncIO object aims to run functions concurrently using Async Queues."""
    def __init__(self, max_workers: int):
        #: Number of workers.
        self.max_workers = max_workers
        #: Jobs queue.
        self.queue = Queue()
        #: Jobs results queue.
        self.results = Queue()

    def enqueue(self, job: callable, *args, **kwargs):
        """Add a job in the jobs queue."""
        _job = partial(job, *args, **kwargs)
        self.queue.put_nowait(_job)

    async def worker(self):
        """Worker method will get a job from the queue and execute it.
        It will be canceled by the dequeue method."""
        while True:
            # Get a job from the queue.
            job = await self.queue.get()

            # Execute the job in the asyncio event loop.
            if iscoroutinefunction(job):
                result = await job()
            else:
                loop = get_event_loop()
                result = await loop.run_in_executor(None, job)

            # Put job results in the results queue.
            self.results.put_nowait(result)

            # Indicate that the jobs is done.
            self.queue.task_done()

    async def dequeue(self):
        """Async generator which execute asyncronousely and yield results for
        each job."""
        #: Workers list.
        workers = []
        #: Pending jobs counter.
        pending = self.queue.qsize()

        # Create asyncio tasks for each workers.
        for _ in range(self.max_workers):
            task = create_task(self.worker())
            workers.append(task)

        # Yield results while there is pending jobs.
        while pending:
            result = await self.results.get()
            yield result
            pending -= 1

        # Wait until queues are fully processed.
        await self.queue.join()

        # Cancel our worker tasks.
        for worker in workers:
            worker.cancel()

        # Wait until all worker tasks are cancelled.
        await gather(*workers, return_exceptions=True)