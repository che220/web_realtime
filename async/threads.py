import asyncio
import threading
import traceback


async def get_exception():
    raise RuntimeError("created error")


async def sleep_some(secs):
    for i in range(secs):
        print(f'{secs}:', threading.current_thread().ident)
        await asyncio.sleep(1)  # only sleep the current task
    return f'done-{secs}'


async def run_multiple_tasks():
    """
    all tasks are on the same thread! But they run parallel, no longer sequential!

    :return:
    """
    tasks = []
    for i in range(5,2,-1):
        tasks.append(asyncio.create_task(sleep_some(i)))

    for t in tasks:
        await t
    print('all done')


async def run_with_gather():
    """
    all coros are on the same thread! But they run parallel, not sequential!

    :return:
    """
    # the following are executed sequentially

    # timeout will generate concurrent.futures._base.TimeoutError, which kills the process
    try:
        await asyncio.wait_for(sleep_some(7), timeout=1)
    except BaseException as ex:
        print('timeout exception:', type(ex), traceback.format_exc())

    await asyncio.gather(sleep_some(5), sleep_some(4), sleep_some(3))
    await sleep_some(2)


async def run_with_gather_and_loop(loop):
    """
    all coros are on the same thread! But they run parallel, not sequential!

    :return:
    """
    # the following are executed sequentially

    # timeout will generate concurrent.futures._base.TimeoutError, which kills the process
    try:
        t = await loop.create_task(sleep_some(7), timeout=3)
        await t
    except BaseException as ex:
        print('timeout exception:', type(ex), traceback.format_exc())

    await asyncio.gather(sleep_some(5), sleep_some(4), sleep_some(3))
    await sleep_some(2)


async def run_with_exception(return_exceptions):
    """
    if return_exceptions=False, one exception will kill the whole gather and kill the thread (process)

    :return:
    """
    try:
        rs = await asyncio.gather(sleep_some(2), sleep_some(3), get_exception(),
                                  return_exceptions=return_exceptions)
        print(rs)
    except BaseException as ex:
        # if the exception is caught, it will allow other tasks in the same gather to finish
        # otherwise, the exception will kill the process which kills all other tasks
        print("gather exception:", str(ex))

    print(await asyncio.shield(sleep_some(5)))
    try:
        print(await get_exception())  # this kills the process
    except BaseException as ex:
        print('Exception:', str(ex))

    print(await asyncio.shield(sleep_some(6)))


if False:
    # sequential
    asyncio.run(sleep_some(5))
    asyncio.run(sleep_some(4))
    asyncio.run(sleep_some(3))

if False:
    asyncio.run(run_multiple_tasks())

if True:
    asyncio.run(run_with_gather())
    print('run_coroutine_threadsafe:')
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(run_with_gather(), loop = loop)

if False:
    asyncio.run(run_with_exception(True))
    print('----- return_exceptions=False -----')
    asyncio.run(run_with_exception(False))
