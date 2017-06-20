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
		for j in range(length-i):		# 冒泡方向是从头冒到尾部
			if sorted_data[j] > sorted_data[j+1]:		# 如果需要按由大到小改变比较符号就行
				sorted_data[j], sorted_data[j+1] = sorted_data[j+1], sorted_data[j]		# 两两交换
		i += 1		# 下一轮冒泡
	return sorted_data

def bubble_sort2(sorted_data):
	'''
	冒泡方向由底到顶
	'''
	i = 1
	length = len(sorted_data)
	while i < length:
		for j in range(length-1, i-1, -1):		# 从底往上冒
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
	2、确定左右旗标，左右旗标分别用于从左和从右扫描时定位
	3、如果左旗标不大于右旗标
		从右往左扫描，找到小于基准值的位置
		从左往右扫描，找到大于基准值的位置
		交换两个位置的值
	4、一轮结束后位于右旗标左边的数据(包括右旗标)都不大于右边的数
	5、最后就可以将基准值与右旗标的值交换位置
	'''
	if left >= right:			# 待处理数据只为一个返回
		return sorted_data
	benchmark = sorted_data[left]			# 基准值
	i, j = left+1, right			# 待比较数据旗标

	while i <= j:
		while j >= i and sorted_data[j] >= benchmark:		# 跳出循环说明位置j的值小于基准值，>= benchmark 而不是>benchmark是避免两个数都相等时跳不出循环
			j -= 1		# 或者最左边的值都还大于等于基准值		
		while i <= j and sorted_data[i] <= benchmark:		# 跳出循环说明位置i的值大于于基准值
			i += 1			# 或者最右边的值都还小于等于基准值					
		if i < j:
			sorted_data[i], sorted_data[j] = sorted_data[j], sorted_data[i]
			j -= 1
			i += 1
	#print(left, right, left, j)
	sorted_data[left], sorted_data[j] = sorted_data[j], sorted_data[left]

	quick_sort(sorted_data, left, j-1)
	quick_sort(sorted_data, j+1, right)
	return sorted_data

# Insert sort
def insert_sort(sorted_data):
	'''
	直接插入排序--基本思想：在一个有序序列中从后向前扫描，将未排序数据插入到有序序列中合适的位置
	1、第一个数作为初始的有序序列（因为只有一个数，所以肯定是有序的）
	2、取未排序数据的第一个作为待排序数据
	3、在有序序列从后向前扫描找到待排序数据的位置，该位置后的有序数据都往后挪位，为待排序数据提供插入空间
	4、重复2
	'''
	for pos, sort_data in enumerate(sorted_data[1:]):
		insert_pos = pos
		while insert_pos >= 0 and sorted_data[insert_pos] > sort_data:
			sorted_data[insert_pos + 1] = sorted_data[insert_pos]		# 往后挪位
			insert_pos -= 1
		sorted_data[insert_pos+1] = sort_data

	return sorted_data

# Binary insert sort
def binary_insert_sort(sorted_data):
	'''
	二分插入排序---与直接插入排序最大区别在于查找插入位置时使用的是二分查找的方式，
	效率主要提高在待插入位置查找速度上
	'''
	for pos, sort_data in enumerate(sorted_data[1:]):
		left, right = 0, pos
		while left <= right:
			middle = (right + left) // 2
			if sort_data > sorted_data[middle]:		# 待插入数据在有半部分
				left = middle + 1
			else:		# 待插入数据在左半部分
				right = middle - 1
		while pos >= left:			# 往后挪位
			sorted_data[pos+1] = sorted_data[pos]
			pos -= 1
		sorted_data[left] = sort_data 		# 最终left位置就为待插入数据位置

	return sorted_data

# Shell sort
def shell_sort(sorted_data, dk):
	'''
	希尔排序--直接插入排序的改进
	基本思想
		设置一个递减增量对数据进行分组，在组内进行直接插入排序，
		当增量为1也既最后只剩下一组并进行直接插入排序。
	希尔排序较直接插入排序效率高的原因：
		当n值很大时数据项每一趟排序需要移动的个数很少，但数据项的距离很长；
		当n值减小时每一趟需要移动的数据增多，此时已经接近于它们排序后的最终位。
	主要步骤
	1、确定增量序列，本例使用hibbard增量，它是1, 3, 7, .......2^k - 1，这个序列可以在实践和理论上给出更好的结果
	2、
	'''
	for d in dk:
		for i in range(d):		#  给0...d的元素组队，间隔是d，然后对每一组进行直接插入排序
			s = sorted_data[i::d]
			for j, sort_data in enumerate(s[1:]):		# 对组进行直接插入排序
				insert_pos = i + j * d;		# 组中元素在待排序数据中间隔是d
				while insert_pos >= i and sorted_data[insert_pos] > sort_data:		# 直接插入排序
					sorted_data[insert_pos+d] = sorted_data[insert_pos]
					insert_pos -= d;
				sorted_data[insert_pos+d] = sort_data
	return sorted_data

def get_dk(data_length):
	'''
	根据数据长度生成增量序列
	'''
	dk_list = list()
	k = 1
	while True:
		dk = 2**k - 1
		if dk < data_length:
			dk_list.append(dk)
			k += 1
		else:
			break
	return reversed(dk_list)

# Selection sort
def select_sort(sorted_data):
	'''
	选择排序---在未排序序列中选择最值，然后将其插入到已排序序列之后
	1）从左往右遍历数据，找到最值
	2）将最值插入到已排序序列之后（首次遍历已排序序列还没有，最值插入到首位）
	'''
	data_length = len(sorted_data)
	for insert_pos in range(data_length):		# 当前待插入位置
		min_value_pos = insert_pos		# 保存最小值位置
		for i in range(insert_pos+1, data_length):		# 在当前位置后寻找是否还有较待插入位置还小的值
			if sorted_data[i] < sorted_data[min_value_pos]:		# 更新最小值位置
				min_value_pos = i
		if min_value_pos != insert_pos:		# 将最值放到待插入位置
			sorted_data[insert_pos], sorted_data[min_value_pos] = sorted_data[min_value_pos], sorted_data[insert_pos]
	return sorted_data	

if __name__ == '__main__':
	sorted_data = list(range(-100, 100))		# 待排序数据，数据量大的话可以明显看出区别
	random.shuffle(sorted_data)			# 打乱顺序
	print('排序前：', sorted_data)
	# sort_results = bubble_sort2(sorted_data.copy())
	# sort_results = quick_sort(sorted_data, 0, len(sorted_data) - 1)
	# sort_results = insert_sort(sorted_data)
	# sort_results = binary_insert_sort(sorted_data)
	# sort_results = shell_sort(sorted_data, get_dk(len(sorted_data)))
	sort_results = select_sort(sorted_data)
	print('排序后：', sort_results)
