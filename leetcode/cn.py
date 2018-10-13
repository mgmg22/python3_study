#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cn.py
# @Author: sxs
# @Date  : 2018/10/13
# @Desc  :
import copy


class Solution:

    def flipAndInvertImage(self, A):
        """
    832. 翻转图像
    """
        print(A)
        for index in range(len(A)):
            A[index].reverse()
            print(A[index])
        for index in range(len(A)):
            for index_chlid in range(len(A[index])):
                A[index][index_chlid] = int(not bool(A[index][index_chlid]))
        return A

    """
    162. 寻找峰值
    """

    def findPeakElement(self, nums):
        left = copy.deepcopy(nums)
        left.pop(0)
        print(left)
        print(nums)
        if (len(left) == 0):
            return 0
        if (len(left) == 1):
            return int(left[0] > nums[0])
        if left[0] < nums[0]:
            return 0
        if left[len(left) - 1] > nums[len(left) - 1]:
            return len(left)
        for index in range(len(left)):
            left_num = nums[index]
            middle_num = left[index]
            print(index, left_num)
            print(index, middle_num)
            if len(nums) > (index + 2):
                right_num = nums[index + 2]
                if middle_num > left_num and middle_num > right_num:
                    return index + 1


print(Solution.findPeakElement("", [1, 2, 3, 1]))
