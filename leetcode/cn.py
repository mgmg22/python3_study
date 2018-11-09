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

    """
    807. 保持城市天际线
    """

    def maxIncreaseKeepingSkyline(self, grid):
        size = grid.__len__()
        line_max = [0] * size
        raw_max = [0] * size
        for i in range(0, size):
            print(grid[i])
            for j in range(0, size):
                if grid[i][j] > raw_max[i]:
                    raw_max[i] = grid[i][j]
                if grid[j][i] > line_max[i]:
                    line_max[i] = grid[j][i]
        result = 0
        for x in range(0, size):
            for y in range(0, size):
                result += min(line_max[x], raw_max[y]) - grid[x][y]
        # print(raw_max, line_max)
        return result


if __name__ == '__main__':
    # print(Solution.findPeakElement("", [1, 2, 3, 1]))
    print(Solution.maxIncreaseKeepingSkyline("", [[3, 0, 8, 4], [2, 4, 5, 7], [9, 2, 6, 3], [0, 3, 1, 0]]))
