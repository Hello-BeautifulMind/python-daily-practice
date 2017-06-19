import string
import random
import pymysql
import os
import re
from PIL import Image
import xlwt

ALLOW_CHAR = string.ascii_letters + string.digits

# 002
def gen_copon_code(quantity, code_length):
	'''
	生成指定数量和长度的不重复的优惠码，优惠码由数字和字母组成
	'''
	copon_code_set = set()
	shuffle_char = list(ALLOW_CHAR)
	random.shuffle(shuffle_char)			# 注意打乱顺序是改变对象自身，因此对象必须可变，而且返回值为None

	while len(copon_code_set) < quantity:
		copon_code = random.sample(shuffle_char, code_length)
		copon_code = ''.join(copon_code)			# 转为不可变对象，因为集合元素需要是不可变对象
		if copon_code not in copon_code_set:
			copon_code_set.add(copon_code)			# 注意update和add的区别：一个是将可迭代对象的每一个元素加到集合里，一个是添加一个不可变元素到集合里

	return copon_code_set

# 003
def sotred_in_mysql(copon_codes):
	'''
	将生成的优惠码存储到mysql数据库
	1、连接数据库，获取游标
	2、创建sql语句，执行sql语句
	3、提交到数据库保存
	4、关闭游标
	5、关闭数据库连接
	'''
	connect = pymysql.Connect(
			host='localhost',
			port = 3306,
			user = 'python',
			passwd = '123456',
			db = 'python_practice',
			charset = 'utf8'
		)
	cursor = connect.cursor()
	sql = "INSERT INTO copon_code (code) VALUES (%s)"
	for code in copon_codes:
		cursor.execute(sql, code)	# cursor.execute(sql % code) 这样的话sql中的%s要加入'' >> '%s'
	#parms = tuple((code for code in copon_codes))
	#print(parms)
	#cursor.executemany(sql, parms)	# 返回插入的数据数，与execute区别是execute只返回一条
	try:
		print('成功插入%d 条数据' % cursor.rowcount)
		cursor.execute(sql, 'abc')
	except pymysql.err.IntegrityError:
		print('不能重复')
	connect.commit()			# commit将数据保存到数据库
	print('成功插入%d 条数据' % cursor.rowcount)
	cursor.close()
	connect.close()

# 004
def word_count(file_name):
	'''
	词频统计
	1、打开文件，拆分字符串(可以把不是单词的去掉:re.sub())
	2、遍历每个不重复单词单词（集合去重），这样每次统计只对没被统计过的进行统计，统计结果加入到列表中
	3、返回统计结果
	'''
	word_set = set()
	word_list = list()
	word_count_result = list()
	with open(file_name, 'r') as f:
		for line in f:
			word_list.extend(line.split())	# split不指定分隔符意味着所有空白符都可作为分隔符，并且空字符串被从结果中除去
		# 词频统计
		word_set.update(word_list)			# 先去掉重复的单词
		for word in word_set:
				count = word_list.count(word)
				word_count_result.append((word, count))
	return word_count_result

# 005
def image_processing(img_dir, width, height):
	'''
	批量修改图片的尺寸
	1、安装pillow库，导入Image类
	2、获取所有图片的名称
	3、遍历每张图片，使用Image类打开头像
	4、获取当前图片大小，修改图片尺寸
	5、保存图片
	'''
	img_list = os.listdir(img_dir)
	for img in img_list:
		img_path = os.path.join(img_dir, img)
		with Image.open(img_path) as im:
			print(im.format, im.size, im.mode)
			#out = im.resize((width, height))		# 返回新的图片对象，im还是指向原图片对象
			im.thumbnail((width, height))			# 返回None，im指向改变尺寸的图片对象
			im.save(img)			# 如果使用resize方法则必须是要out.save()
			print(im.format, im.size, im.mode)

# 006
def diary_analysis(file_dir, imp_word):
	'''
	分析一个目录下的所有日记，统计每篇日记认为最重要的单词
	1、获取目录下的所有日记的文件名
	2、遍历每一篇日记，做如下处理
	3、打开日记，拆分成每一个单词并统计认为最重要的单词，结果保存到列表里
	4、返回结果
	'''
	diary_list = os.listdir(file_dir)			# 获取所有日记名
	word_list, count_result = list(), list()	# 一个存放日记单词，一个统计结果
	for diary in diary_list:				# 遍历每篇日记
		diary_path = os.path.join(file_dir, diary)			# 构建日记路径
		with open(diary_path, "r") as f:
			for line in f:
				word_list.extend(line.split())			# 拆分单词
			count = word_list.count(imp_word)
			count_result.append((diary, imp_word, count))
			word_list.clear()			# 没分析完一篇日记都要清空该篇日记的单词，避免对下篇日记产生影响
	return count_result

# 007
def code_count(code_file):
	'''
	统计一段代码中的行数，包括空行和注释，但是要标明出来
	1、打开代码文件，遍历每一行
	2、判断该行是何种类型(代码，注释，空行)
		解决代码和注释同一行情况，判断是否有注释可以先去掉引号之间的内容
	3、更新该类型统计数
	4、返回结果
	'''
	count_result = dict(code=0, blank_line=0, annotations=0)
	in_annotation = False			# 是否还在注释里边，用于在多行注释情况
	with open(code_file, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()			# 去掉两头空白符
			if line.startswith("'''") or line.startswith('"""'):
				if not in_annotation:			# 多行注释的开始
					in_annotation = True		# 进入到多行注释里了
					if line[3:]:				# 注释紧接在引号后面注释行加1
						count_result['annotations'] += 1
				else:			# 否则这是多行注释的结尾
					in_annotation = False
			else:
				if not line:			# 空行
					count_result['blank_line'] += 1
				else:			# 非空行
					if in_annotation:			# 该行还在多行注释里，注释计数加1
						count_result['annotations'] += 1
					else:
						if not line.startswith('#'):			# 不以‘#’开头，说明该行包含代码
							count_result['code'] += 1
						if '#' in line:				# ‘#’位于行里边并且不在引号里，说明该行包含注释
								count_result['annotations'] += 1

	return count_result

# 11
def filter_words(filter_file):
	'''
	用户输入的词语在过滤文件中则给出“Freedom”，否则给出“Human Rights”
	1、打开过滤文件，将过滤词语加载到内存
	2、用户输入语句，判断过滤词语是否在语句中
	3、返回不同提示
	'''
	with open(filter_file, 'r') as f:
		filter_words = f.read().split()
		#filter_words_set = set(filter_words)
	words = input('Input：')
	#words_set = set(words.split())fds
	#if words_set & filter_words_set:
	res = 'Human Rights!'
	for word in filter_words:
		if word in words:
			res = 'Freedom'
			break
	return res

# 12
def replace_sensitive_words(filter_file):
	'''
	在filter_file中的词出现用户输入句子中时使用‘*’替换
	1、打开过滤文件,载入敏感词语
	2、用户输入一段话，如果出现敏感词则用‘*’替换
	3、返回替换结果
	'''
	r1 = re.compile(r'[\u4E00-\u9FA5]')			# 汉字
	r2 = re.compile(r'[a-zA-Z]')			# 单词
	n = 1			# ‘*’替换个数，默认是1
	with open(filter_file, 'r') as f:
		filter_words = f.read().split()
	user_input = input('Input：')
	for word in filter_words:
		if word in user_input:			# 有敏感词，分析是汉字还是单词类型
			if r1.search(word):			# 汉字，计算长度
				n = len(word)
			elif r2.search(word):			# 单词，长度为1
				n = 1
			user_input = user_input.replace(word, '*'*n)			# 使用相应长度的‘*’替换
	return user_input

# 14
def save_to_xls(text_file):
	'''
	将students.txt中的学生信息(字典)保存到xls中
	1、构建excel工作表
		1）导入xlwt模块，创建工作簿
		2）创建工作表并格式化
	2、打开文本文件，将内容写入到构建的工作表中
	'''
	w = xlwt.Workbook()
	ws = w.add_sheet('Students', cell_overwrite_ok=True)

	row0 = ['ID', '姓名', '语文', '数学', '英语']
	for col, value in enumerate(row0):
		ws.col(col).width = 256 * 20			# 表格宽度
		ws.write(0, col, value, set_style('Times New Roman', 270))			# 填写表格内容并应用样式

	with open(text_file, 'r') as f:
		row = 1
		style = set_style('Times New Roman', 270)			# 设置表格样式
		for line in f:	
			line = line.strip()
			if line not in ['{', '}']:			# 取“{}”里的内容，
				stu_infos = line.split(':')			# 将ID和其他信息分离
				ID = stu_infos[0].strip('"')			# 去掉ID两头的引号
				s = eval(stu_infos[1].rstrip(','))			# 其他信息转成列表对象：name, chinese, math, english
				ws.write(row, 0, ID, style)			# 先写入ID，然后遍历其他信息并写入表格
				for col, item in enumerate(s):
					ws.write(row, col+1, item, style)
				row += 1			# 换到下一行
		w.save('students.xls')			# 保存到excel中
		print('保存成功')

def set_style(name, height, bold=False):
	'''
	设置excel表格的基本样式，包括字体、表格高度、是否加粗、表格颜色，内容水平且垂直居中
	'''
	style = xlwt.XFStyle()	# 初始化样式
	font = xlwt.Font()
	font.name = name
	font.height = height
	font.bold = bold
	font.color_index = 4
	style.font = font

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER		# 水平居中
	alignment.vert = xlwt.Alignment.VERT_CENTER		# 再垂直居中
	style.alignment = alignment
	return style



if __name__ == '__main__':
	#copon_codes = gen_copon_code(200, 5)
	#sotred_in_mysql(copon_codes)
	#res = word_count('words.txt')
	#res = diary_analysis('diary/', 'and')			# [('01.txt', 'a', 0), ('02.txt', 'a', 3), ('03.txt', 'a', 1)]
	#image_processing('images/', 128, 128)
	#res = code_count('code_count.py')
	# res = filter_words('filtered_words.txt')
	# print(res)
	# res = replace_sensitive_words('filtered_words.txt')
	# print(res)
	save_to_xls('students.txt')

	