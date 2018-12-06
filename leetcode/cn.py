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

    """
       5. 最长回文子串—Manacher算法
       """

    def longestPalindrome(self, s):
        arr = ["#"]
        for item in list(s):
            arr.append(item)
            arr.append("#")
        print(arr)
        result = ""
        max_result = ""
        size = arr.__len__()
        for i in range(1, size - 1):
            step = 0
            middle = arr[i]
            while middle != result:
                step += 1
                if i - step < 0 or i + step == size:
                    break
                if step != 1:
                    middle = result
                low = arr[i + step]
                high = arr[i - step]
                if low == high:
                    result = low + middle + high
                else:
                    break
                print(step, result)
            if len(result) > len(max_result):
                max_result = result
            if i + step == size:
                print(i + step, "遍历结束")
                break
        return max_result.replace("#", "")

    """
         820. 单词的压缩编码
         """

    def minimumLengthEncoding(self, words):
        list1 = sorted(list(words), key=lambda i: len(i), reverse=True)
        print(list1)
        str = ""
        arr = []
        for item in list1:
            # print(str.find(item))
            pos = str.find(item)
            if pos < 0:
                arr.append(len(str))
                str = str + item + "#"
            else:
                arr.append(pos)
        print(arr)
        print(str)
        return len(str)

    """
     3. 无重复字符的最长子串
     """

    def lengthOfLongestSubstring(self, s):
        string_arr = list(s)
        # 保存每个不重复字符最后出现的位置
        char_dist = {}
        # 保存循环到当前位置时的最长子串 TODO 优化算法
        size_arr = [0] * s.__len__()
        max_save = 0
        for i in range(len(string_arr)):
            last_char = char_dist.get(string_arr[i])
            size_arr[i] = i + 1 - max(int(last_char or 0), i - size_arr[i - 1])
            # 更新当前位置的最长子串
            char_dist[string_arr[i]] = i + 1
        # print(size_arr)
        result = 0
        for item in size_arr:
            if item > result:
                result = item
        return result

    """
         101. 对称二叉树
         """

    def isSymmetric(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        def isSameTree(p, q):
            if not p and not q:  # 两二叉树皆为空，递归边界，两者皆为空返回真
                return True
            if p and q and p.val == q.val:
                l = isSameTree(p.left, q.right)  # ，与leetcode100有区别。递归，每次重新从函数入口处进行，每次进行递归边界判断
                r = isSameTree(p.right, q.left)
                return l and r  # and操作，需要l与r皆为true时，才返回真。只用最后一次递归边界return值
            else:
                return False

        if not root:
            return True
        else:
            # p=root.left;q=root.right
            return isSameTree(root.left, root.right)


if __name__ == '__main__':
    x = Solution
    # print(Solution.findPeakElement("", [1, 2, 3, 1]))
    # print(Solution.maxIncreaseKeepingSkyline("", [[3, 0, 8, 4], [2, 4, 5, 7], [9, 2, 6, 3], [0, 3, 1, 0]]))
    # print(x.longestPalindrome("", "cbbd"))
    # print(x.minimumLengthEncoding("", ["time", "me", "bell"]))
    # print(x.lengthOfLongestSubstring("", "abcabcbb"))
    print(x.isSymmetric("", [1, 2, 2, 3, 4, 4, 3]))
