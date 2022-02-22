
from os import listdir
from shutil import copyfile
from bookletsort import isValidName

compiledpages = {}
orderedpages = []
extension = '.jpg'

def trim_extension(filename:str) -> str:
    extension = filename.split('.')[1]
    return filename.split('.')[0]

def add_pages_to_data(directorypath) -> None:
    directorylist = listdir(directorypath)
    pagenums_in_directory = []
    for i in range(len(directorylist)):
        filename = directorylist[i]
        pagenum = trim_extension(filename)
        if isValidName(pagenum):
            pagenums_in_directory.append(int(pagenum))
    pagenums_in_directory.sort()
    for i in range(len(pagenums_in_directory)):
        path = directorypath + str(pagenums_in_directory[i]) + extension
        orderedpages.append(path)

add_pages_to_data("./frontmatter/")
add_pages_to_data("./comic/")
add_pages_to_data("./extras/")

for i in range(len(orderedpages)):
    filepath = orderedpages[i]
    copyfile(filepath, "./compiledbook/" + str(i + 1) + extension)