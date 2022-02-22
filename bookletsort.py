from os import listdir
from shutil import copyfile

def formatbook(pages: list[int], signatures: int) -> list[list[int]]:
    '''
    Formats page numbers into the order in which they should be printed to be bound in as many signatures as desired. 
    
    Signatures follow the order [front-left, front-right, back-left, back-right], such that for [4,1,2,3], 2,3 is printed on the reverse of 4,1, with 2 directly behind 1 and 3 directly behind 4. 
    [a,b,c,d,e,f,g,h] represents a signature containing two leafs nested within each other, with c,d on the reverse of a,b, then [e,f,g,h] printed on a seperate sheet in a similar fashion, nested inside the first leaf. 
    [[a,b,c,d], [e,f,g,h]] represents two seperate signatures, each with only one leaf, NOT nested within each other.

    If number of pages is not a multiple of four, or number of signatures exceeds number of pages divided by four, blank pages, represented by zeros, will be added to fill up space. Signatures  are front-loaded (blanks are added to the end of the booklet, with no blanks until given page numbers run out.)

    May require some trial-and-error to get the ideal number of signatures without producing excess blank pages and depending on your needs.

    >>> formatbook([1,2,3,4],1)
    >>> [[4,1,2,3]]
    A single signature printed on one leaf. The trivial example.

    >>> formatbook([1,2,3,4,5], 2)
    >>> [[4,1,2,3], [0,5,0,0]]
    From 5 pages, a total 8-page book split into two 4-page signatures, with three blank pages at the end. The best choice for number of signatures to minimize blanks for this many pages.

    >>> formatbook([1,2,3,4,5,6,7,8,9,10,11,12], 2)
    >>> [[8,1,2,7,6,3,4,5], [0,9,10,0,0,11,12,0]]
    From 12 pages, a total 16-page book split into two 8-page signatures, with four blank pages added at the end. A bad choice for number of signatures. 3 signatures would not have needed the addition of any blank pages at all.

    >>> formatbook([1,2,3,4,5,6,7,8,9,10,11,12], 3)
    >>> [[4,1,2,3], [8,5,6,7], [12,9,10,11]]
    From 12 pages, a total 12-page booklet split into three 4-page signatures. Ideal form.
    '''
    book = []
    while (len(pages) % 4 != 0) or ( (signatures*4) > len(pages)) or len(pages) % signatures != 0 or (len(pages) // signatures) % 4 != 0:
        pages.append(0)

    pages_per_signature = len(pages) // signatures
    for signature in range(signatures):
        book.append([])
        for i in range(pages_per_signature):
            book[signature].append(pages[(i + pages_per_signature*signature)])
        book[signature] = bookletsort(book[signature])

    return book


def bookletsort(pages:list[int]) -> list[int]:
    '''
    Takes an array of page numbers and reorders them as if they are to be printed on double sided pages bound as a booklet with a single signature. Length of input array must be a multiple of 4 (that is, front and back of one leaf folded in half.)
    >>> bookletsort([1, 2, 3, 4])
    >>> [4, 1, 2, 3]
    >>> bookletsort([1, 2, 3, 4, 5, 6, 7, 8])
    >>> [8, 1, 2, 7, 6, 3, 4, 5]
    '''
    result = []
    elem = 0
    i = 0
    while (len(result) < len(pages)):
        if i % 2 == 0:
            result.append(pages[-(elem + 1)])
            result.append(pages[elem])
        else:
            result.append(pages[elem])
            result.append(pages[-(elem + 1)])
        i += 1
        elem += 1
    return result

def pageorder_to_bookorder(inputdir: str, outputdir: str, fileextension: str, signatures: int) -> None:
    '''
    Converts a directory of files named 1, 2, 3, ..., n into their respective reordering for the purpose of printing and binding in double-sided signatures, and places the result into the specified output directory. Output files are named with (new order number)-(old page number).fileextension.

    Input and output are used as relative paths. Fileextension should not include a dot.

    Signatures specifies the number of signatures the pages should be split into. See formatbook().

    0.fileextension is used as a placeholder for blank pages in the case that pages must be added to make valid signatures when number of given pages is not a multiple of four. It MUST be included in the input folder in the correct file format, but it need not be blank if you wish to include your own custom placeholder page. See formatbook().

    input/
        0.jpg
        1.jpg
        2.jpg
        3.jpg
        4.jpg
    output/
        <empty>
    >>> pageorder_to_bookorder("input", "output", "jpg", 1)
    input/
        <inputdir remains unchanged>
    output/
        1-4.jpg
        2-1.jpg
        3-2.jpg
        4-3.jpg
    '''
    pages = listdir(inputdir)
    pagenums = extract_pagenums(pages)
    pagenums.sort()
    book_ordered_pages = flatten( formatbook(pagenums, signatures) )

    for i in range(len(book_ordered_pages)):
        filename = book_ordered_pages[i]
        copyfile(f"./{inputdir}/{filename}.{fileextension}", f"./{outputdir}/{i}-{filename}.{fileextension}")

def extract_pagenums(pages) -> list:
    '''
    For files named {number}.{extension}, returns list of their numbers.
    dir/
        1.txt
        2.txt
        3.txt
    >>> pages = listdir(dir)
    >>> extract_pagenums(pages)
    >>> [1,2,3]
    '''
    pagenums = []
    for filename in pages:
        filename = filename.split('.')[0] 
        if isValidName(filename):
            page_number = int(filename)
            pagenums.append(page_number)
    return pagenums


def generate_page_list(num_pages: int) -> list:
    '''
    Generates a list of page numbers num_pages long.
    >>> generate_page_list(7)
    >>> [1,2,3,4,5,6,7]
    '''
    pages = []
    for i in range(num_pages):
        pages.append(i+1)
    return pages

def flatten(ls: int):
    '''
    Flattens a list up to two levels deep. Preserves order.
    >>> flatten( [[1,2,3],4,[5,6,7],8] )
    >>> [1,2,3,4,5,6,7,8]

    >>> flatten( [[1,2,3]] )
    >>> [1,2,3]

    >>> flatten( [[[a,b]],[c,d],[e],f] )
    >>> [[a,b],c,d,e,f]
    >>> flatten( [[a,b],c,d,e,f] )
    >>> [a,b,c,d,e,f]
    An example of running repeatedly until done.
    '''
    flatlist = []
    for item in ls:
        if type(item) !=  list:
            flatlist.append(item)
        else:
            for subitem in item:
                flatlist.append(subitem)
    return flatlist

def isValidName(filename: str)-> bool:
    '''
    Checks whether filename is a nonempty, nonzero string representing an integer.
    '''
    if filename.isdigit() and filename != "0" and filename != "":
        return True
    else:
        return False