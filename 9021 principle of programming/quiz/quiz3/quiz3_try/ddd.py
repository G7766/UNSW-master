'''
d={'N':(1,33),'S':[[3,3],[2,22]]}
print(d['N'])
d['N']=(1,35)
print(d['N'])
print(d.keys())
print(d.values())


a=d.get('S')
print(a)
print(a[1])
d.pop('S')
print(d)
'''





d={'N':[[1,33]],'S':[[3,0],[2,0],[6,0],[5,0]],'W':[[2,2],[3,0],[4,1],[5,5],[6,0]],'E':[[1,1],[2,8],[3,0]]}
'''
nn=d.get('N')
ss=d.get('S')
ee=d.get('E')
print('--------')
#ee.pop(1)

#print(len(d['E']))


for i in range(len(ee)):
	print(i)
	if ee[i][1]==0:
		ee.pop(i)
		i=i-1
print(ee)
#for i in range()
'''
'''
def dellist(ee):
	ee1=[]
	for i in range(len(ee)):
		print(i)
		if ee[i][1]==0:
			ee1.append(ee[i])
	print(ee1)
	for i in range(len(ee1)):
		ee.remove(ee1[i])
	print(ee)
	return ee

def delnumb(d):
	nn=d.get('N')
	ss=d.get('S')
	ww=d.get('W')
	ee=d.get('E')
	nn=dellist(nn)
	ss=dellist(ss)
	ww=dellist(ww)
	ee=dellist(ee)
	d['N']=nn
	d['S']=ss
	d['W']=ww
	d['E']=ee
	return d

d=delnumb(d)
print(d)
#q=delnumb(ee)
#print(q)

q={'A':[1,2]}
q['A']=[3,2,1]
print(q)
'''


#删除NSWE为0的
def dellist(ee):
	count=0
	if ee==[[0]]:
		ee=1
	for i in range(len(ee)):
		print(i)
		if ee[i][1]==0:
			count+=1
			if count==len(ee):
				ee=1

	return ee
#删除size为0

def dellist(ee):
	ee1=[]
	for i in range(len(ee)):
		print(i)
		if ee[i][1]==0:
			ee1.append(ee[i])
	print(ee1)
	for i in range(len(ee1)):
		ee.remove(ee1[i])
	print(ee)
	return ee


def delnumb(d):
	nn=d.get('N')
	ss=d.get('S')
	ww=d.get('W')
	ee=d.get('E')
	nn=dellist(nn)
	ss=dellist(ss)
	ww=dellist(ww)
	ee=dellist(ee)
	d['N']=nn
	d['S']=ss
	d['W']=ww
	d['E']=ee
	if d['N']==[]:
		d.pop('N')
	if d['S']==[]:
		d.pop('S')
	if d['W']==[]:
		d.pop('W')
	if d['E']==[]:
		d.pop('E')
	return d


q=delnumb(d)
print(q)



















