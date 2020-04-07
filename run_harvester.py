from DataHarvester.dhav_core.run_updates import run_me
import time

while True:
    try:
        run_me()
    except:
        pass

    time.sleep(100)