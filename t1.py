import numpy as np  

data = np.load('bins/bd_tb.npy',allow_pickle=True)


n2=59172578050
a=np.where(data == n2)

print(len(a[0]))


if (len(a[0])==0):
  	print('no')
else:
 	print('si')