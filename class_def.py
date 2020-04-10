class Exam:
    def __init__(self, cC, cN, instructor, sC, p, d=2.5):
        self.course_code = cC  # course code
        self.course_Name = cN  # course name
        self.instructor = instructor  # instructor
        self.student_class = sC  # student class
        self.priority = p  # priority
        self.duration = d  # duration
        self.start_time = 0  # start time
        self.location = ""  # location

    def __str__(self):
        return "Course code: "+ self.course_code + "\tPriority: " + str(self.priority) + "\tStart time & Location: " + str(self.start_time) + " " + self.location


class Day:
    def __init__(self, dNum, dName=None):
        self.day_num = dNum  # day #
        self.examList = [] # list of exam instances
        self.day_name = dName  # Name of the day


class Schedule:
    def __init__(self, dL, nE):
        self.day_list = dL  # list of day instances
        self.num_exams = nE  # number of exams
    def __str__(self):
        content = ""

        for day in self.day_list:
            content += "Day " + str(day.day_num) + "\n"
            for exam in day.examList:
                content += "\t" + str(exam) + "\n"
        return content

class Graph:
    def __init__(self, arr, mtx):
        self.exams = arr
        self.adjacency_mtx = mtx
        self.exam_dict = {}

        for i, exam in enumerate(self.exams):
            self.exam_dict[exam] = i


class MinHeap:
    def __init__(self):
        self.heap = []

    def size(self):
        return len(self.heap)

    def enqueue(self, exam):
        self.heap.append(exam)
        curr_idx = len(self.heap) - 1
        while curr_idx > 0:
            parent_idx = (curr_idx - 1) // 2
            if self.heap[parent_idx].priority < self.heap[curr_idx].priority:
                # swap until max heap properties satisfied
                self.heap[parent_idx], self.heap[curr_idx] = self.heap[curr_idx], self.heap[parent_idx]
                curr_idx = parent_idx
            else:
                return

    def dequeue(self):
        if self.size == 0:
            print("Dequeue Error: Empty Heap")
            return None

        removed = self.heap[0]  # instance being returned
        self.heap[0] = self.heap.pop()  # place the last node onto the root

        last_idx = self.size() - 1
        curr_idx = 0
        left_idx, right_idx = 1, 2

        # go through the heap from top to bottom
        while left_idx <= last_idx or right_idx <= last_idx:
            # existence of right_idx guarantees existence of two children
            if right_idx <= last_idx:
                max_child = self.heap[left_idx] if self.heap[left_idx].priority > self.heap[right_idx].priority else \
                    self.heap[right_idx]
                swap_idx = left_idx if max_child == self.heap[left_idx] else right_idx
            else:
                max_child = self.heap[left_idx]
                swap_idx = left_idx

            # swap if property isn't satisfied
            if self.heap[curr_idx].priority < max_child.priority:
                self.heap[swap_idx], self.heap[curr_idx] = self.heap[curr_idx], self.heap[swap_idx]
                curr_idx = swap_idx
                left_idx = curr_idx * 2 + 1
                right_idx = curr_idx * 2 + 2
            else:
                break
        return removed
