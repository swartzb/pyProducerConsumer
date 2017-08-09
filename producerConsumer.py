import threading
import random
import time

producer_is_ready = threading.Semaphore(value = 0)
producer_must_start = threading.Semaphore(value = 0)

print_lock = threading.Lock()

def my_print(msg):
    with print_lock:
        print(msg)

def consumer_thread_proc():
    rnd = random.Random()
    rnd.seed()
    for i in range(5):

        # simulate other work
        time.sleep(rnd.random())
        my_print('  consumer: signaling producer start')
        producer_must_start.release()

        # simulate other work
        time.sleep(rnd.random())
        my_print('    consumer: waiting')
        producer_is_ready.acquire()
        my_print('    consumer: wait done\nconsumer: start consuming')

        # simulate time consuming
        time.sleep(rnd.random())
        my_print('consumer: consumption complete')

def producer_thread_proc():
    rnd = random.Random()
    rnd.seed()
    for i in range(5):

        # simulate other work
        time.sleep(rnd.random())
        my_print('  producer: waiting')
        producer_must_start.acquire()
        my_print('  producer: wait done\nproducer: start producing')

        # simulate time producing
        time.sleep(rnd.random())
        my_print('producer: production complete\n    producer: signaling ready')
        producer_is_ready.release()

def main():
    consumer_thread = threading.Thread(target = consumer_thread_proc, args = ())
    producer_thread = threading.Thread(target = producer_thread_proc, args = ())

    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()

main()
