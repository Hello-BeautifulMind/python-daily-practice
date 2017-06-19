import random

# Bubble Sort
def bubble_sort1(sorted_data):
	'''
	冒泡排序
	1、确定需冒泡次数
	2、根据冒泡方向确定待排序的初始位置和最终位置
	3、在待排序数据中两两比较，将待排序数据中的最值冒到合适的位置
	4、重复2
	'''
	i = 1
	length = len(sorted_data)
	while i < length:
		for j in range(length-i):			# 冒泡方向是从头冒到尾部
			if sorted_data[j] > sorted_data[j+1]:		# 如果需要按由大到小改变比较符号就行
				sorted_data[j], sorted_data[j+1] = sorted_data[j+1], sorted_data[j]			# 两两交换
		i += 1			# 下一轮冒泡
	return sorted_data

def bubble_sort2(sorted_data):
	'''
	冒泡方向由底到顶
	'''
	i = 1
	length = len(sorted_data)
	while i < length:
		for j in range(length-1, i-1, -1):			# 从底往上冒
			if sorted_data[j-1] > sorted_data[j]:
				sorted_data[j-1], sorted_data[j] = sorted_data[j], sorted_data[j-1]
		i += 1
	return sorted_data

# Quick sort
def quick_sort(sorted_data, left, right):
	'''
	快速排序--基本思想是每一轮排序将待排序数据分成独立的两部分：
		a、以一个基准值分界，左边部分都比右边部分小
		b、然后对左右部分进行相同的操作，当左右部分数据个数都为1时排序结束
	1、选择一个基准值
	'''
	if left >= right:			# 待处理数据只为一个返回
		return sorted_data
	benchmark = sorted_data[left]			# 基准值
	i, j = left+1, right			# 待比较数据旗标

	while i <= j:
		while j >= i and sorted_data[j] >= benchmark:			# 跳出循环说明位置j的值小于基准值，>= benchmark 而不是>benchmark是避免两个数都相等时跳不出循环
			j -= 1												# 或者最左边的值都还大于等于基准值		
		while i <= j and sorted_data[i] <= benchmark:			# 跳出循环说明位置i的值大于于基准值
			i += 1												# 或者最右边的值都还小于等于基准值					
		if i < j:
			sorted_data[i], sorted_data[j] = sorted_data[j], sorted_data[i]
			j -= 1
			i += 1
	#print(left, right, left, j)
	sorted_data[left], sorted_data[j] = sorted_data[j], sorted_data[left]

	quick_sort(sorted_data, left, j-1)
	quick_sort(sorted_data, j+1, right)
	return sorted_data



if __name__ == '__main__':
	sorted_data = list(range(10, 10))			# 待排序数据，数据量大的话可以明显看出区别
	random.shuffle(sorted_data)			# 打乱顺序
	print('排序前：', sorted_data)
	sort_results = bubble_sort2(sorted_data.copy())
	#sort_results = quick_sort(sorted_data, 0, len(sorted_data) - 1)
	print('排序后：', sort_results)
