import asyncio
import random
from datetime import datetime

# -----------------------------------------------------------------
# EXAMPLE 1
async def pause():
    await asyncio.sleep(1)

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        await pause()
        f *= 1

loop = asyncio.get_event_loop()
tasks = [
    asyncio.ensure_future(factorial('A', 3)),
    asyncio.ensure_future(factorial('B', 4))
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# -----------------------------------------------------------------
# EXAMPLE 2
x = 1
async def main():
    x += 1
    await asyncio.sleep(1)
    if x < 10:
        return main()

asyncio.run(main())

# -----------------------------------------------------------------
# EXAMPLE 3  (my favorite)
def await_click(xpath, i=0):
    if i > 60:
        return 'Failed after 60 seconds.  Aborting.'

    try:
        driver.find_element_by_xpath('//' + xpath).click()
    except:
        return await_click(xpath, i+1)
