"""multi-threading producer/consumer examples"""

import threading
import random
import time
import queue

producer_is_ready = queue.Queue(maxsize = 1)
producer_must_start = queue.Queue(maxsize = 1)

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

    # simulate other work
    time.sleep(rnd.random())

    # signal producer to start first time
    my_print('  consumer: signaling producer start')
    producer_must_start.put(1)

    for i in range(10):

        # wait for producer to signal ready.
        my_print('    consumer: waiting')
        val = producer_is_ready.get()
        producer_is_ready.task_done()
        my_print('    consumer: wait done {0}'.format(val))

        # signal producer to re-start
        my_print('  consumer: signaling producer start')
        producer_must_start.put(1)

        # simulate time processing
        my_print('consumer: start processing')
        time.sleep(rnd.random())
        my_print('consumer: processing complete')

    # wait for producer to signal ready last time
    my_print('    consumer: waiting')
    val = producer_is_ready.get()
    producer_is_ready.task_done()
    my_print('    consumer: wait done {0}'.format(val))

    # signal producer to end
    my_print('      consumer:  signaling producer end')
    producer_must_start.put(None)

    # simulate time processing
    my_print('consumer: start processing')
    time.sleep(rnd.random())
    my_print('consumer: processing complete')

def producer_thread_proc():
    """Producer thread procedure."""
    rnd = random.Random()
    rnd.seed()

    # simulate other work
    time.sleep(rnd.random())

    while True:

        # wait for consumer to signal start.
        my_print('  producer: waiting')
        item = producer_must_start.get()
        my_print('  producer: wait done')
        if item is None:
            my_print('      producer: ending')
            break
        producer_must_start.task_done()

        # simulate time producing
        my_print('producer: start producing')
        time.sleep(rnd.random())
        val = rnd.randrange(10)
        my_print('producer: production complete {0}'.format(val))
        producer_is_ready.put(val)

def main():
    """Execute the multi-thread producer/consumer example.

    Create 2 threads, start them, then wait for both to complete.

    From the output, even with the random delays,
    producer producing and comsumer processing are
    interleaved, starting with producer producing.
    Also, with queues, there is overlap between
    producing the next item and processing the current item.
    """
    consumer_thread = threading.Thread(target = consumer_thread_proc, args = ())
    producer_thread = threading.Thread(target = producer_thread_proc, args = ())

    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()

main()
