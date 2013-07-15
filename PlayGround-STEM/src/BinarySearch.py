'''
Created on Jul 15, 2013

@author: Minh
'''



def binarySearch(target,data_list):
    left = 0
    right = len(data_list) - 1
    while right >= left:
        mid = (left + right) / 2 #compute one time
        elem = data_list[mid]
        if elem == target:
            return mid
        elif elem < target:
            left = mid + 1
        elif elem > target:
            right = mid - 1
        print(left, right, mid)
    return -1