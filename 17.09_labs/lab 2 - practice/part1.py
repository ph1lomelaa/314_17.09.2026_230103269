import threading
import queue

class Task:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def worker(worker_id, tasks, data):
    while True:
        task = tasks.get()  
        if task is None:   
            tasks.task_done()
            break

        for i in range(task.start, task.end):
            data[i] = data[i] * 2 

        for 
        print(f"worker {worker_id} has done the  [{task.start}:{task.end}]")
        tasks.task_done()
def main(float a; float b; float c):
    float a = 50000000;
    int b = int.random()
    int a = int random()
    static long totalHits = 0;

    for i in range(static long totalHits, via totalHits++):
        if (a*b){
            return a*b;
        }
    



if __name__ == "__main__":
    main()
