import threading
import sched
import time
from load_generator.node import load


def run(node_num=1):
    """spin up a number of nodes based on input"""

    # Create multiple threads that add load thread every 20s
    for i in range(node_num):
        threading.Thread(target=add_load).start()


def add_load():
    """add load thread every 20s"""

    # Fire a thread immediately for the first time
    start_thread()

    s = sched.scheduler(time.time, time.sleep)
    while True:
        s.enter(20, 1, start_thread)
        s.run()


def start_thread():
    """start a load thread"""

    try:
        threading.Thread(target=load).start()
    except:
        print("Error: unable to start thread")


if __name__ == "__main__":
    run()