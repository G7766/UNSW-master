class Tree:
	def __init__(self,value=None):
		self.value=value
		if value is None:
			self.left_subtree=None
			self.right_subtree=None
		else:
			self.left_subtree=Tree()
			self.right_subtree=Tree()

	def insert_in_bst(self,value):
		if self.value is None:
			self.value=value
			self.left_subtree=Tree()
			self.right_subtree=Tree()
			return True
		if value==self.value:
			return False
		if value<self.value:
			return self.left_subtree.insert_in_bst(value)
		return self.right_subtree.insert_in_bst(value)

	def height(self):
		if self.value is None:
			return 0
		return max(self.left_subtree._height(),self.right_subtree._height())
	
	def _height(self):
		if self.value is None:
			return 0
		return max(self.left_subtree._height(),self.right_subtree._height())+1


	def display(self):
		self._display(0,self.height())

	def _display(self,level,height):
		if level>height:
			return
		if level==height:
			#print(self.value)
			print('    '* level, self.value,sep='')
			return
		if self.left_subtree.value is not None:
			self.left_subtree._display(level+1,height)
		else:
			print('\n' * (2**(height-level)-1))
		print('    '* level, self.value,sep=' ')
		if self.right_subtree.value is not None:
			self.right_subtree._display(level+1,height)
		else:
			print('\n' * (2**(height-level)-1))

	def is_bst(self):
		if self.value is None:
			return True
		if self.left_subtree.value is not None:
			largest_smaller_value=self.left_subtree
			while largest_smaller_value.right_subtree.value:
				largest_smaller_value=largest_smaller_value.right_subtree
				if largest_smaller_value.value>=self.value:
					return False
		if self.right_subtree.value is not None:
			largest_smaller_value=self.left_subtree
			while largest_smaller_value.left_subtree.value:
				largest_smaller_value=largest_smaller_value.left_subtree
				if largest_smaller_value.value<=self.value:
					return False
		return self.left_subtree.is_bst() and self.right_subtree.is_bst()








		

t_1=Tree(2)
print(t_1.value)
print(t_1.left_subtree)
print(t_1.right_subtree)
print(t_1.left_subtree.left_subtree)
print(t_1.right_subtree.right_subtree)
t_2=Tree(0)
t=Tree(4)
t_1.left_subtree=t_2
t_1.right_subtree=t
print(t_1.left_subtree)
print(t_1.right_subtree)
print(t_1.left_subtree.value)
print(t_1.right_subtree.value)


t=Tree()
t.insert_in_bst(2)
t.insert_in_bst(6)

t=Tree()
t.insert_in_bst(6)
print(t.height())
t.insert_in_bst(10)
print(t.height())
t.insert_in_bst(14)
print(t.height())
t.insert_in_bst(2)
print(t.height())
print('-------------')
t=Tree()
t.insert_in_bst(6)
print(t.display())
t.insert_in_bst(10)
print(t.display())
t.insert_in_bst(4)
print(t.display())
t.is_bst()
t=Tree(10)
t_1=Tree(5)
t_2=Tree(10)
t3=Tree(15)
