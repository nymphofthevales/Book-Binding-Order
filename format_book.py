
from os import listdir
from shutil import copyfile
import bookletsort

def flattenBookSort(ls):
    flatlist = []
    for item in ls:
        if type(item) ==  int:
            flatlist.append(item)
        elif type(item) == list:
            for subitem in item:
                flatlist.append(subitem)
    return flatlist

SIGNATURES= 20

pages = listdir("./output/")
pagenums = []
for filename in pages:
    if filename != ".DS_Store" and filename != "0.jpg":
        pagenums.append(int(filename.split('.')[0]))
pagenums.sort()
book_ordered_pages = flattenBookSort(bookletsort.formatbook(pagenums, SIGNATURES))

for i in range(len(book_ordered_pages)):
    filename = book_ordered_pages[i]
    copyfile(f"./output/{filename}.jpg", f"./book_order/{i + 1}-{filename}.jpg")


def pageorder_to_bookorder(inputdir: str, outputdir: str, fileextension: str, signatures: int) -> None:
    '''
    '''
    pages = listdir(inputdir)
    pagenums = []
    for filename in pages:
        if isValid(filename):
            page_number = int( filename.split('.')[0] )
            pagenums.append(page_number)
    pagenums.sort()
    book_ordered_pages = flattenBookSort(formatbook(pagenums, signatures))

    for i in range(len(book_ordered_pages)):
        filename = book_ordered_pages[i]
        copyfile(f"./{inputdir}/{filename}.{fileextension}", f"./{outputdir}/{i}-{filename}.{fileextension}")