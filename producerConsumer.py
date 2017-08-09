"""multi-threading producer/consumer examples"""

import threading
import random
import time

producer_is_ready = threading.Event()
producer_must_start = threading.Event()

print_lock = threading.Lock()

def my_print(msg):
    """Print using a lock.

    Without the lock, newlines randomly disappear on Windows.
    """
    with print_lock:
        print(msg)

def consumer_thread_proc():
    """Consumer thread procedure."""
    rnd = random.Random()
    rnd.seed()
    for i in range(5):

        # simulate other work
        time.sleep(rnd.random())

        # signal producer to start
        my_print('  consumer: signaling producer start')
        producer_must_start.set()

        # simulate other work
        time.sleep(rnd.random())

        # wait for producer to signal ready.
        my_print('    consumer: waiting')
        producer_is_ready.wait()
        producer_is_ready.clear()
        my_print('    consumer: wait done\nconsumer: start consuming')

        # simulate time consuming
        time.sleep(rnd.random())
        my_print('consumer: consumption complete')

def producer_thread_proc():
    """Producer thread procedure."""
    rnd = random.Random()
    rnd.seed()
    for i in range(5):

        # simulate other work
        time.sleep(rnd.random())

        # wait for consumer to signal start.
        my_print('  producer: waiting')
        producer_must_start.wait()
        producer_must_start.clear()
        my_print('  producer: wait done\nproducer: start producing')

        # simulate time producing
        time.sleep(rnd.random())
        my_print('producer: production complete\n    producer: signaling ready')
        producer_is_ready.set()

def main():
    """Execute the multi-thread producer/consumer example.

    Create 2 threads, start them, then wait for both to complete.

    From the output, even with the random delays,
    producer producing and comsumer consuming are
    interleaved, starting with producer producing.
    Also, there is no overlap between producing and consuming.
    """
    consumer_thread = threading.Thread(target = consumer_thread_proc, args = ())
    producer_thread = threading.Thread(target = producer_thread_proc, args = ())

    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()

main()
