from class_def import *
from Methods import *

filename = "eng_exam.txt"
storage = "exam_info.txt"
location_list = ['BA-2185', 'MY-380', 'HA-403', 'BA-1130', 'MS-2172', 'BA-2175', 'EX-320', 'MY-150', 'WB-219', 'BA-1180', 'BN-2N', 'EX-300', 'ZZ-VLAD', 'HA-316', 'APSCDept-ComputerLab', 'HA-410', 'MS-3153', 'MY-315', 'EX-100', 'BA-2165', 'MY-360', 'SF-3202', 'BA-2159', 'GB-304', 'WB-130', 'HI-CART', 'BA-2195', 'MP-102', 'BA-1170', 'HA-401', 'MY-330', 'WB-116', 'GB-303', 'WB-119', 'WY-119', 'ZZ-KNOX', 'BA-1160', 'EX-310', 'EX-200', 'SF-2202']
test_location_list = ['BA-2185']

print("\nThanks for choosing Lucas's and Stephen's scheduler \n")
# gather_info(storage)
exam_list = create_exam_list(storage)
heap_sort_in_place(exam_list)
exam_list = exam_list[::-1]
graph = create_graph(exam_list)
day_dict = labelling_without_specified(graph, location_list)

if day_dict.get("Failure", True) == True:
    assign_location(day_dict, location_list)
    day_list = create_day_list(day_dict)
    schedule = create_schedule(day_list, exam_list)

    print(schedule)
    #exam_23 = search_exam_by_class(schedule, 23)


