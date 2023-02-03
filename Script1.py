import os

My_files_path=os.path.join(os.getcwd(),'My_files')

for i in range(10):
	with open(My_files_path'/a{i}.txt','w') as f:
		f.write('hello world')
