"""
Operating System Task Scheduler with Max-Heap Priority Queue
Course: Algorithms: Analysis and Design
Core Operations: INSERT, EXTRACT-MAX, PEEK, INCREASE-KEY
Features: Non-preemptive & Preemptive priority scheduling, Task Aging (anti-starvation), Metrics & Gantt chart
"""

import time
from typing import List, Optional, Tuple, Dict, Any

class Task:
    """Represents a process / task in the operating system."""
    def __init__(self, task_id: str, name: str, priority: int, arrival_time: int, burst_time: int):
        self.task_id = task_id
        self.name = name
        self.priority = priority          # Dynamic priority (can increase with aging)
        self.initial_priority = priority  # Base priority assigned upon creation
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time: Optional[int] = None
        self.completion_time: Optional[int] = None
        self.waiting_time: int = 0
        self.turnaround_time: int = 0

    def __lt__(self, other: 'Task') -> bool:
        # Max-heap comparison: higher priority > lower priority
        # If priorities are equal, earlier arrival time wins (FIFO tie-breaking)
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.arrival_time > other.arrival_time

    def __gt__(self, other: 'Task') -> bool:
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.arrival_time < other.arrival_time

    def __le__(self, other: 'Task') -> bool:
        return not (self > other)

    def __ge__(self, other: 'Task') -> bool:
        return not (self < other)

    def __repr__(self) -> str:
        return f"Task({self.task_id}: '{self.name}', prio={self.priority}, burst={self.burst_time}, arr={self.arrival_time})"


class MaxHeap:
    """
    Max-Heap implementation for Priority Queue based on CLRS algorithm specifications.
    Maintains max-heap property: parent >= children.
    """
    def __init__(self):
        self._heap: List[Task] = []

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    def peek(self) -> Task:
        """Returns the maximum priority task without removing it (O(1))."""
        if self.is_empty():
            raise IndexError("peek() called on an empty MaxHeap.")
        return self._heap[0]

    def insert(self, task: Task) -> None:
        """
        Inserts a new task into the max-heap (O(log n)).
        Appends to the bottom and sifts up (heap-increase-key).
        """
        self._heap.append(task)
        self._sift_up(len(self._heap) - 1)

    def extract_max(self) -> Task:
        """
        Removes and returns the task with the highest priority (O(log n)).
        Replaces root with the last element and max-heapifies down.
        """
        if self.is_empty():
            raise IndexError("extract_max() called on an empty MaxHeap.")
        
        max_task = self._heap[0]
        last_task = self._heap.pop()
        
        if not self.is_empty():
            self._heap[0] = last_task
            self._max_heapify(0)
            
        return max_task

    def increase_key(self, index: int, new_priority: int) -> None:
        """
        Increases the priority of the task at given index (O(log n)).
        Used by the OS scheduler's aging mechanism to prevent starvation.
        """
        if index < 0 or index >= len(self._heap):
            raise IndexError("Index out of bounds in increase_key.")
        if new_priority < self._heap[index].priority:
            raise ValueError("new_priority must be greater than current priority.")
        
        self._heap[index].priority = new_priority
        self._sift_up(index)

    def _sift_up(self, index: int) -> None:
        """Bubbles an element up to restore the max-heap invariant."""
        while index > 0 and self._heap[index] > self._heap[self._parent(index)]:
            p = self._parent(index)
            self._heap[index], self._heap[p] = self._heap[p], self._heap[index]
            index = p

    def _max_heapify(self, index: int) -> None:
        """
        Maintains max-heap property rooted at index (O(log n)).
        Recursively sinks smaller nodes down the tree.
        """
        left = self._left(index)
        right = self._right(index)
        largest = index
        heap_size = len(self._heap)

        if left < heap_size and self._heap[left] > self._heap[largest]:
            largest = left

        if right < heap_size and self._heap[right] > self._heap[largest]:
            largest = right

        if largest != index:
            self._heap[index], self._heap[largest] = self._heap[largest], self._heap[index]
            self._max_heapify(largest)

    def get_all_tasks(self) -> List[Task]:
        """Returns a shallow copy of tasks currently in the heap."""
        return list(self._heap)

    def rebuild_heap(self) -> None:
        """Re-heapifies the entire structure in O(n) time."""
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._max_heapify(i)


class TaskScheduler:
    """
    Operating System Task Scheduler Simulator.
    Simulates CPU scheduling with a Max-Heap Priority Ready Queue.
    Supports:
      - Non-preemptive and Preemptive Priority Scheduling
      - Aging Mechanism (periodically increments priority of waiting tasks to prevent starvation)
      - Metrics calculation (Waiting Time, Turnaround Time, Throughput, CPU Utilization)
      - Execution Gantt Chart timeline logging
    """
    def __init__(self, preemptive: bool = False, aging_interval: int = 5, aging_increment: int = 1):
        self.preemptive = preemptive
        self.aging_interval = aging_interval      # Cycles before waiting tasks age
        self.aging_increment = aging_increment    # Priority boost per aging cycle
        self.ready_queue = MaxHeap()
        self.completed_tasks: List[Task] = []
        self.gantt_chart: List[Dict[str, Any]] = []  # [{task_id, name, start, end, priority}]
        self.logs: List[str] = []

    def _log(self, time_step: int, message: str) -> None:
        entry = f"[Time {time_step:03d}] {message}"
        self.logs.append(entry)

    def apply_aging(self, current_time: int) -> None:
        """Applies aging to tasks in ready queue to prevent starvation."""
        if self.aging_interval <= 0:
            return
        
        aged_any = False
        for task in self.ready_queue.get_all_tasks():
            time_in_queue = current_time - task.arrival_time
            if time_in_queue > 0 and time_in_queue % self.aging_interval == 0:
                old_prio = task.priority
                task.priority += self.aging_increment
                self._log(current_time, f"AGING: {task.task_id} ('{task.name}') priority boosted from {old_prio} -> {task.priority}")
                aged_any = True
                
        if aged_any:
            self.ready_queue.rebuild_heap()

    def run_simulation(self, task_list: List[Task]) -> Dict[str, Any]:
        """Runs the CPU discrete-event scheduling simulation."""
        # Reset state
        self.ready_queue = MaxHeap()
        self.completed_tasks = []
        self.gantt_chart = []
        self.logs = []

        # Sort tasks by arrival time
        incoming_tasks = sorted(task_list, key=lambda t: t.arrival_time)
        current_time = 0
        total_tasks = len(incoming_tasks)
        task_idx = 0
        current_task: Optional[Task] = None
        current_slice_start: Optional[int] = None
        idle_time = 0

        self._log(current_time, f"Scheduler started (Mode: {'Preemptive' if self.preemptive else 'Non-Preemptive'}).")

        while len(self.completed_tasks) < total_tasks:
            # 1. Admit incoming tasks whose arrival_time <= current_time
            while task_idx < total_tasks and incoming_tasks[task_idx].arrival_time <= current_time:
                arriving = incoming_tasks[task_idx]
                self.ready_queue.insert(arriving)
                self._log(current_time, f"ARRIVED: {arriving.task_id} ('{arriving.name}', prio={arriving.priority}, burst={arriving.burst_time}) inserted into Ready Queue.")
                task_idx += 1

            # 2. Check for preemption if in preemptive mode
            if self.preemptive and current_task is not None and not self.ready_queue.is_empty():
                highest_ready = self.ready_queue.peek()
                if highest_ready > current_task:
                    # Record Gantt slice for preempted task
                    duration = current_time - current_slice_start
                    if duration > 0:
                        self.gantt_chart.append({
                            "task_id": current_task.task_id,
                            "name": current_task.name,
                            "start": current_slice_start,
                            "end": current_time,
                            "priority": current_task.priority
                        })
                    self._log(current_time, f"PREEMPTION: {highest_ready.task_id} (prio={highest_ready.priority}) preempts {current_task.task_id} (prio={current_task.priority}, remaining={current_task.remaining_time}).")
                    self.ready_queue.insert(current_task)
                    current_task = None

            # 3. If CPU is idle, dispatch next task
            if current_task is None:
                if not self.ready_queue.is_empty():
                    current_task = self.ready_queue.extract_max()
                    current_slice_start = current_time
                    if current_task.start_time is None:
                        current_task.start_time = current_time
                    self._log(current_time, f"DISPATCHED: {current_task.task_id} ('{current_task.name}', prio={current_task.priority}) allocated CPU.")
                else:
                    # CPU is idle
                    idle_time += 1
                    current_time += 1
                    continue

            # 4. Advance time by 1 unit (or full burst in non-preemptive mode)
            step = 1 if self.preemptive else current_task.remaining_time
            
            # In non-preemptive mode, check if any tasks arrive during execution
            if not self.preemptive:
                current_time += step
                current_task.remaining_time = 0
                current_task.completion_time = current_time
                current_task.turnaround_time = current_task.completion_time - current_task.arrival_time
                current_task.waiting_time = current_task.turnaround_time - current_task.burst_time
                self.completed_tasks.append(current_task)
                self.gantt_chart.append({
                    "task_id": current_task.task_id,
                    "name": current_task.name,
                    "start": current_slice_start,
                    "end": current_time,
                    "priority": current_task.priority
                })
                self._log(current_time, f"COMPLETED: {current_task.task_id} ('{current_task.name}') finished execution (Wait={current_task.waiting_time}, TAT={current_task.turnaround_time}).")
                current_task = None
            else:
                # Preemptive step
                current_time += 1
                current_task.remaining_time -= 1
                
                # Check completion
                if current_task.remaining_time == 0:
                    current_task.completion_time = current_time
                    current_task.turnaround_time = current_task.completion_time - current_task.arrival_time
                    current_task.waiting_time = current_task.turnaround_time - current_task.burst_time
                    self.completed_tasks.append(current_task)
                    self.gantt_chart.append({
                        "task_id": current_task.task_id,
                        "name": current_task.name,
                        "start": current_slice_start,
                        "end": current_time,
                        "priority": current_task.priority
                    })
                    self._log(current_time, f"COMPLETED: {current_task.task_id} ('{current_task.name}') finished execution (Wait={current_task.waiting_time}, TAT={current_task.turnaround_time}).")
                    current_task = None
                
                # Apply aging to waiting tasks
                self.apply_aging(current_time)

        total_sim_time = current_time
        total_waiting_time = sum(t.waiting_time for t in self.completed_tasks)
        total_turnaround_time = sum(t.turnaround_time for t in self.completed_tasks)
        avg_waiting = total_waiting_time / total_tasks
        avg_turnaround = total_turnaround_time / total_tasks
        cpu_busy_time = total_sim_time - idle_time
        cpu_utilization = (cpu_busy_time / total_sim_time) * 100.0 if total_sim_time > 0 else 0.0

        return {
            "total_time": total_sim_time,
            "avg_waiting_time": avg_waiting,
            "avg_turnaround_time": avg_turnaround,
            "cpu_utilization": cpu_utilization,
            "completed_tasks": self.completed_tasks,
            "gantt_chart": self.gantt_chart,
            "logs": self.logs
        }


def create_sample_os_workload() -> List[Task]:
    """Generates a realistic OS workload with diverse task types, priorities, and burst times."""
    return [
        Task(task_id="T1", name="Kernel Interrupt Handler", priority=95, arrival_time=0, burst_time=3),
        Task(task_id="T2", name="Audio Stream Buffer",      priority=80, arrival_time=1, burst_time=4),
        Task(task_id="T3", name="Disk I/O Flush",           priority=60, arrival_time=2, burst_time=6),
        Task(task_id="T4", name="UI Compositor / Display",  priority=85, arrival_time=4, burst_time=5),
        Task(task_id="T5", name="Network Packet Receive",   priority=90, arrival_time=7, burst_time=2),
        Task(task_id="T6", name="Background Backup Daemon", priority=20, arrival_time=0, burst_time=8),
        Task(task_id="T7", name="Virus Scanner Background", priority=30, arrival_time=3, burst_time=7),
        Task(task_id="T8", name="Browser JavaScript Worker",priority=70, arrival_time=5, burst_time=4),
    ]

if __name__ == "__main__":
    print("=" * 70)
    print("OPERATING SYSTEM TASK SCHEDULER SIMULATION (MAX-HEAP)")
    print("=" * 70)

    # 1. Non-Preemptive Simulation
    scheduler_np = TaskScheduler(preemptive=False)
    tasks_np = create_sample_os_workload()
    results_np = scheduler_np.run_simulation(tasks_np)

    print("\n--- NON-PREEMPTIVE PRIORITY SCHEDULING RESULTS ---")
    print(f"Total Simulation Time: {results_np['total_time']} units")
    print(f"Average Waiting Time:    {results_np['avg_waiting_time']:.2f} units")
    print(f"Average Turnaround Time: {results_np['avg_turnaround_time']:.2f} units")
    print(f"CPU Utilization:         {results_np['cpu_utilization']:.1f}%")
    print("\nExecution Order (Gantt Blocks):")
    for b in results_np['gantt_chart']:
        print(f"  [{b['start']:02d} -> {b['end']:02d}] {b['task_id']} ({b['name']}) [Priority: {b['priority']}]")

    # 2. Preemptive Simulation with Aging
    scheduler_p = TaskScheduler(preemptive=True, aging_interval=6, aging_increment=5)
    tasks_p = create_sample_os_workload()
    results_p = scheduler_p.run_simulation(tasks_p)

    print("\n--- PREEMPTIVE PRIORITY SCHEDULING (WITH AGING) RESULTS ---")
    print(f"Total Simulation Time: {results_p['total_time']} units")
    print(f"Average Waiting Time:    {results_p['avg_waiting_time']:.2f} units")
    print(f"Average Turnaround Time: {results_p['avg_turnaround_time']:.2f} units")
    print(f"CPU Utilization:         {results_p['cpu_utilization']:.1f}%")
    print("\nExecution Order (Gantt Blocks):")
    for b in results_p['gantt_chart']:
        print(f"  [{b['start']:02d} -> {b['end']:02d}] {b['task_id']} ({b['name']}) [Priority: {b['priority']}]")
