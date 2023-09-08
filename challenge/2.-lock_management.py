import multiprocessing
import time

stdout_lock = multiprocessing.Lock()


def addCount():
    with stdout_lock:
        try:
            file = open("demofile.txt", "r")
            content = file.read()
            file.close()
            count = int(content.strip())
            file = open("demofile.txt", "w")
            file.write(str(count + 1))
            file.close()
        except Exception as e:
            pass


if __name__ == "__main__":
    with multiprocessing.Pool(processes=50) as pool:
        jobs = []
        for _ in range(100):
            jobs.append(pool.apply_async(addCount))
        for job in jobs:
            job.wait()

    ## Checking the final count
    file = open("demofile.txt", "r")
    content = file.read()
    print("Final Count: ", content)
    file.close()
