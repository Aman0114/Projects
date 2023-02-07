import os
current_folder_path=os.getcwd()
My_files_path=os.path.join(current_folder_path,'My_files')

def lst_of_file_types():
	lst=[]
	for dirpath,dirname,filename in os.walk(current_folder_path):
		for i in filename:
			lst.append(os.path.splitext(i)[-1])
			lst=list(set(lst))
	return lst		

def arrange_files(lst):
	for d in lst:
		if d=='.py':
			pass
		else:
			for dirpath,dirname,filename in os.walk(current_folder_path):
				for i in filename:
					if os.path.splitext(i)[-1]== d:
						if not os.path.exists(f'{My_files_path}/{d[1:]}'):
							os.makedirs(f'{My_files_path}/{d[1:]}')
						os.rename(f'{dirpath}/{i}',f'{My_files_path}/{d[1:]}/{i}')

list_of_file_types=lst_of_file_types()
arrange_files(list_of_file_types)



