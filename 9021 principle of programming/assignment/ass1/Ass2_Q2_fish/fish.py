import sys
import copy

a=input('Which data file do you want to use?')
directory='/Users/g/Desktop/'
l=[]
try:
  with open(directory+a,'r') as file:
  #with open(a,'r') as file:
    for line in file:
      line=line.strip()
      line=line.split()
      #print(line)
      for element in line:
        l.append(element)
    #print(l)
except ValueError:
  print('Incorrect input, giving up!')
  sys.exit()
except IOError:
  print('Incorrect input, giving up!')
  sys.exit

distance=[]
fish=[]
for element in range(len(l)):
  if element%2==0:
    distance.append(int(l[element]))
  else:
    fish.append(int(l[element]))
print('distance:',distance,'fish:',fish)
'''

distance=[20,40,340,360]
fish=[300,400,700,600]
'''
dis_len=len(distance)
fish_len=len(fish)
#print('dis_len:',dis_len,'fish:',fish_len)

#average(fish)
q=0
for i in fish:
  q=q+i
#print(q)

fish_min=min(fish)
fish_max=int(q/fish_len)
fish_try=(fish_min+fish_max)/2
print('fish_min:',fish_min,'fish_max:',fish_max,'fish_try:',fish_try)


distance_copy=copy.deepcopy(distance)
fish_copy=copy.deepcopy(fish)
print('distance_copy:',distance_copy,'fish_copy:',fish_copy)

max_kilo_fish=0
while max_kilo_fish!=fish_try:
  print('fish_try:',fish_try)
  for a in range(fish_len-1):
    if fish[a]<fish_try:
    #直接从后一个拿，假如后一个是0，减完以后是负数，负数也没关系，总会从再后一个数补给负数
    #因为只检测第a+1个数，最后刀最后一个数，看他能否等于fish_max
      fish[a+1]=fish[a+1]-(fish_try-fish[a])-(distance[a+1]-distance[a])

    elif fish[a]>fish_try:
      if (fish[a]-fish_try)<=(distance[a+1]-distance[a]):
        pass
      else:
        fish[a+1]=fish[a+1]+(fish[a]-fish_try)-(distance[a+1]-distance[a])
    
    elif fish[a]==fish_try:
      pass

  print(fish)

  if fish[-1]>fish_try:
    if abs(fish[-1]-fish_try)<0.01:
      max_kilo_fish=fish_try
    else:
      fish_min=fish_try
      fish_try=(fish_min+fish_max)/2
      print('fish_max:',fish_max,'fish_min:',fish_min)
      fish=copy.deepcopy(fish_copy)
      print('1',max_kilo_fish)
  
  elif fish[-1]<fish_try:
    if abs(fish[-1]-fish_try)<0.01:
      print('fish[-1]',fish[-1],'fish_try:',fish_try)
      max_kilo_fish=fish_try
      print('aaaaaa:',max_kilo_fish)
    else:
      fish_max=fish_try
      fish_try=(fish_max+fish_min)/2
      fish=copy.deepcopy(fish_copy)
      print('fish_max:',fish_max,'fish_min:',fish_min)


  elif fish[-1]==fish_try:
    max_kilo_fish=fish_try
    print('3',max_kilo_fish)

  else:
    max_kilo_fish=0


  print('???',max_kilo_fish)

max_kilo_fish=int(max_kilo_fish)
print('max_kilo_fish:',max_kilo_fish)





















