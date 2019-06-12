import re
def ReadQuery_file(file):
	query_content = []
	with open(file) as f:
		for line in f:
			z = []
			line = re.split('([,\(\)\/\-\&\s])',line)
			for i in line:
				if i.isspace() == False and i!="\n" and i !="":
					z.append(i)
			query_content.append(z)
		#print(query_content)
	return query_content
	
	
query_content = ReadQuery_file('dev_set/Query_File')
print(len(query_content[0]))


print(query_content)


z = '8/23-35 Barker St., Kingsford, NSW 2032'
l = z.split(' ')
print(l)
k = re.split('([,|\(|\)|\/|\-|\&|\s])',z)
kk = re.split('([,\(\)\/\-\&\s])',z)
print(k)
print(kk)

z = []
for i in kk:
	if i.isspace() == False and i!="\n" and i !="":
		z.append(i)
print(z)
print(len(z))
observation_new = []
for term in kk:
	if (term.isspace()==False and term !="\n" and term!=""):
	   observation_new.append(term)
print(observation_new)
#print(query_content)