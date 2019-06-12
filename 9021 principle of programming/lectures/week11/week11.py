from random import randrange
class PriorityQueue:
	def __init__(self,capacity=20):
		self.pq=[None]*(capacity+1)
		self.size=0

	def insert(self,value):
		self.size +=1
		# If self.size < self.capacity
		# otherwise, self.pq needs to be extended
		self.pq[self.size] = value
		self._bubble_up(self.size)


	def _bubble_up(self,position):
		if position ==1:
			return
		parent_position = position//2
		if self.pq[parent_position] < self.pq[position]:
			self.pq[parent_position] , self.pq[position] = self.pq[position] , self.pq[parent_position]
			self._bubble_up(parent_position)


	def process_top_element(self):
		element_being_process = self.pq[1]
		self.pq[1] , self.pq[self.size]==self.pq[self.size] , self.pq[1]
		self.size -=1
		self._bubble_down(1)
		return element_being_process

	def _bubble_down(self,position):
		position_of_largest_child= 2*position
		# if there is a right child (and then also a left child) and right child holds
		# largest value, then need to bubble down with right child
		if 2 * position + 1 <= self.size and self.pq[2*position +1] > self.pq[2*position]:
			position_of_largest_child +=1
		if 2 * position + 1 <= self.size and self.pq[position_of_largest_child] > self.pq[position]:
			self.pq[position_of_largest_child] , self.pq[position] = self.pq[position] , self.pq[position_of_largest_child]
			self._bubble_dwon(position_of_largest_child)






pq=PriorityQueue()
pq.insert(2)
pq.insert(10)
pq.insert(5)
pq.insert(12)
pq.insert(7)
pq.insert(11)

print(pq.pq)
print(pq.process_top_element())



pq=PriorityQueue()
L=[randrange(100) for _ in range(20)]
print(L)
for e in L:
	pq.insert(e)
for e in L:
	print(pq.process_top_element())






