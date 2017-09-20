import os, shutil

#Get current working directory.
root_path = os.path.dirname(os.path.realpath(__file__))
# print(root_path)

#use one iteration of os.walk() to get lists of directories and files.
dir_names = []
file_names = []

for (dirpath, dirnames, filenames) in os.walk(root_path):
    dir_names.extend(dirnames)
    file_names.extend(filenames)
    break

#If there is already a sorted directory, dont plan on moving it.
if "Sorted" in dir_names:
    dir_names.remove("Sorted")

print(dir_names)
print(file_names)

file_ext_list = []
#Create a list of file extensions encountered.

#for each file:

file_name_ext_link = []

for file_name in file_names:
    file_ext = ""

    #for each character in the file name.
    for char in file_name:

        #handle files with internal periods.
        if char == '.':
            file_ext = ''
        else:
            file_ext += char

    print(file_ext)
    file_name_ext_link.append((file_name , file_ext))

    #If we haven't seen this extension yet, add it to list.
    if file_ext not in file_ext_list:
        file_ext_list.append(file_ext)

#add a file extension for folders.
file_ext_list.append('Folders')

print(file_ext_list)
print(file_name_ext_link)

#Create a "Sorted" directory and create subdirectories according to file_ext_list
sorted_directory = root_path + "/Sorted/"
# print(sorted_directory)

#if the "Sorted" directory does not exist, create it.
if not os.path.exists(sorted_directory):
    try:
        os.makedirs(sorted_directory)
    except Exception as e:
        print("Error created sorted directory: " + str(e))

#Now loop through file_ext_list and create subdirectories.
for folder in file_ext_list:

    path = sorted_directory + folder + '/'

    #if subdirectory does not exist, create it.
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print("Error created sorted subdirectory: " + str(e) )

#for files in file_names move to correct directory
for move_file in file_name_ext_link:

    file_name = move_file[0]
    file_ext = move_file[1]

    #dont move the python script
    if file_name == __file__:
        continue

    source = root_path + "/" + file_name
    destination = sorted_directory + file_ext + "/" + file_name
    # print(source)
    try:
        shutil.move(source,destination)
        #add_to_log(source,destination)
    except Exception as e:
        print("Error moving files: " + str(e))

#now for directories, move to Sorted/Folders
folders_directory = sorted_directory + "Folders"
print(folders_directory)

for directory in dir_names:

    source = root_path + "/" + directory + "/"
    destination = folders_directory + "/" + directory + "/"
    # print(source)
    # print(destination)
    try:
        shutil.move(source,destination)
        #add_to_log(source,destination)
    except Exception as e:
        print("Error moving files: " + str(e))


#to revert, loop through log and:
#shutil.move(destination,source)
