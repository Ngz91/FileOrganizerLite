import shutil, os, sys

print(8*"*"+ "File Organizer Lite v.0.1" + 8*"*")

location = input('Directory to organize (E.g example/directory/: ')
extension = input('Extention of files to organize (E.g .txt): ')
directory = input('Name of the directory to move the files (Exclude / or \\): ')

if location == "" or extension == "" or directory == "":
	input("Something was not specified. Press enter to exit.")
else:
	if not os.path.exists(location):
		input(f"\n{location} does not exist. Press enter to exit.")
		sys.exit()
	else:
		f = os.listdir(location)
		directory_path = os.path.join(location + directory)
		if not os.path.exists(directory_path):
			os.makedirs(directory_path, exist_ok=True)
		for filename in f:
			if not filename.endswith(extension):
				continue
			else:
				shutil.move('' + filename, directory_path)
	
	print(f'\n{extension} files have been moved to {directory_path}.')