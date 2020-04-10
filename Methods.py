from class_def import *

def gather_info(filename):
    f = open(filename, 'w')
    flag = 1
    f.write("Course Code,Course Name,Course Instructor,Location,Duration,Priority,Class\n")
    while flag:
        course_code = input("Please enter the course code: ")
        course_name = input("Please enter the course name: ")
        course_instructor = input("Please enter the name of the instructor: ")
        priority = input("Please enter the priority: ")
        student_class = input("Please enter the class taking this exam: ")
        f.write(course_code+','+course_name+','+course_instructor+', , ,'+priority+','+student_class+"\n")
        a = input("More exams to enter (enter Yes or No): ").lower()
        flag = 0 if a == "no" else 1
        if flag:
            print("\nNext exam... \n")
        else:
            print("\nFinished logging exams...\n")
    f.close()

def create_exam_list(filename):
    print("\nCreating exam list...\n")
    f = open(filename, 'r')
    content, exam_heap = [], MinHeap()
    lines = f.readlines()
    for line in lines[1:]:
        content = line.strip().split(',')
        exam_heap.enqueue(Exam(content[0],content[1], content[2],content[6], int(content[5])))
    f.close()
    return exam_heap.heap


# Sorting the priority queue in place in descending order
def heap_sort_in_place(arr):
    size = len(arr)
    while size:
        arr[0], arr[size - 1] = arr[size - 1], arr[0]
        size -= 1
        curr, left, right, last = 0, 1, 2, size - 1
        while right <= last or left <= last:
            if right <= last:
                min_child = arr[left] if arr[left].priority > arr[right].priority else arr[right]
                swap = left if min_child == arr[left] else right
            else:
                min_child = arr[left]
                swap = left

            if arr[curr].priority < min_child.priority:
                arr[swap], arr[curr] = arr[curr], arr[swap]
                curr = swap
                left, right = 2 * curr + 1, 2 * curr + 2
            else:
                break
def sort(arr):
    return arr[::-1]


# All specified exams are placed in the front of the partitioned list, whose elements are of the same priority
def prioritize_specified_exam(arr):
    length = len(arr)
    start, curr = 0, 0
    new_arr = []

    d = dict()
    d[arr[0].priority] = [arr[0]]

    while curr < length:
        if arr[curr].priority != arr[start].priority:
            start = curr
            d[arr[curr].priority] = [arr[curr]]
        else:
            d[arr[curr].priority].append(arr[curr])

    for key in d:
        specified, unspecified = [], []
        for exam in d[key]:
            if exam.location or exam.start_time != 0:
                specified.append(exam)
            else:
                unspecified.append(exam)
        new_arr.extend(specified + unspecified)

    return new_arr


# Create the adjacency matrix whose rows conform the descending order
def create_adjacency_matrix(arr):
    length = len(arr)
    matrix = []

    # initialize the matrix
    for i in range(length):
        row = []
        for j in range(length):
            row.append(0)
        matrix.append(row)

    # add edges i.e. exams share the same class
    for i in range(length):
        k = i + 1
        while k < length:
            if arr[i].student_class == arr[k].student_class:
                matrix[i][k], matrix[k][i] = 1, 1
            k += 1

    return matrix


def create_graph(arr):
    print("\nCreating conflict graph...\n")
    return Graph(arr, create_adjacency_matrix(arr))


def check_conflict(exam_a, exam_list):
    for exam in exam_list:
        if exam.student_class == exam_a.student_class:
            return 0
    return 1  # no conflict with all exams


def swap_adjacency_mtx(mtx, idx_a, idx_b):
    mtx[idx_a], mtx[idx_b] = mtx[idx_b], mtx[idx_a]

def assign_start_time(exam, label):
    if label%3 == 0:
        exam.start_time = 930
    elif label%3 == 1:
        exam.start_time = 1400
    elif label%3 == 2:
        exam.start_time = 1830

def labelling_without_specified(graph, location_list):
    label, idx, exam_num, d, location_num = -1, 0, len(graph.exams), dict(), len(location_list)
    color_list = [1] * exam_num

    for i in range (0, exam_num, 1):
        if not color_list[i]:
            continue
        else:
            label += 1
            idx = i
            while graph.exams[idx].student_class in d.get(label-1, [[], set()])[1] and graph.exams[idx].student_class in d.get(label-2, [[], set()])[1]:
                idx += 1
                if idx == len(graph.exams):
                    print("Unable to schedule due to overload issue")
                    print("Class " +graph.exams[i].student_class + " is overloaded inevitably")
                    return {"Failure": "Failure"}
            graph.exams[idx], graph.exams[i] = graph.exams[i], graph.exams[idx]
            swap_adjacency_mtx(graph.adjacency_mtx, idx, i)
            assign_start_time(graph.exams[i], label)
            d.update({label: [[graph.exams[i]], {graph.exams[i].student_class}]})

        for j in range(0, exam_num, 1):
            if len(d[label][0]) >= location_num:
                break
            else:
                if graph.adjacency_mtx[i][j] == 0 and i != j and color_list[j]:
                    if check_conflict(graph.exams[j], d[label][0]):
                        if not (graph.exams[j].student_class in d.get(label-1, [[], set()])[1] and graph.exams[j].student_class in d.get(label-2, [[], set()])[1]):
                            d[label][0].append(graph.exams[j])
                            d[label][1].add(graph.exams[j].student_class)
                            color_list[j] = 0
                            assign_start_time(graph.exams[j], label)
    if label > 45:
        print("Cannot arrange all exams in 15 days due to limited number of exam center")
    return d

def assign_location(d, location_list):
    for key in d:
        for i in range(0, len(d[key][0]), 1):
            d[key][0][i].location = location_list[i]


def create_day_list(d):
    day_list = []
    count, FLAG = 0, True
    for key in d:
        if FLAG:
            day = Day(key//3 + 1)
            FLAG = False
        day.examList.extend(d[key][0])
        count += 1
        if count % 3 == 0:
            FLAG = True
            day_list.append(day)
    return day_list

def create_schedule(day_list, arr):
    return Schedule(day_list, len(arr))

def search_exam_by_class(schedule, student_class):
    class_list = []
    for day in schedule.day_list:
        for exam in day.examList:
            if exam.student_class == str(student_class):
                class_list.append(exam)
    print("Class: "+ str(student_class) +" has following exams")
    for a in class_list:
        print("\n\t"+str(a))
    return class_list




'''    
    for i in range(0, length, 1):
        if not color_list[i]:
            continue
        else:
            if check_conflict(graph.exams[i], d[label]):
                if len(d[label][0]) < location_num:
                    d[label][0].append(graph.exams[i])
                    d[label][1].append(graph.exams[i].student_class)
                    color_list[i] = 0
                else:
                    label += 1
                    d[label] = [graph.exams[i]]
        for j in range(0, length, 1):
            if graph.adjacency_mtx[i][j] == 0 and i != j:
                if color_list[j]:
                    if check_conflict(graph.exams[j], d[label]):
                        if len(d[label]) < location_num:
                            d[label].append(graph.exams[j])
                            color_list[j] = 0
    '''