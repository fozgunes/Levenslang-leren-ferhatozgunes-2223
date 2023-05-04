import os
from os import path

def main():
    # src = path.realpath("challenge_files.py")
    # root_dir, tail = path.split(src)

    # lijstvancontents = os.listdir(root_dir)
    # os.mkdir("result")

    # totaalbytesize = 0


    # for x in lijstvancontents:
    #     file_stats = os.stat(x)    
    #     totaalbytesize = file_stats.st_size

    # myfile = open("result.txt", "w+")
    # myfile = open("result.txt", "a")
    
    # myfile.write("Total bytecount:")
    # myfile.write(str(totaalbytesize))
    # myfile.write("\nFiles list:\n---------\n")



    # for x in lijstvancontents:
    #     myfile.write(x + "\n")
    
    # myfile.close()

    totaalbytesize = 0
    dirlist = os.listdir()
    
    for entry in dirlist:
        if os.path.isfile(entry):
            filesize = os.path.getsize(entry)
            totaalbytesize += filesize

    os.mkdir("result")

    resultsfile = open("result/result.txt", "w+")
    if resultsfile.mode == "w+":
        resultsfile.write("Total bytecount:" + str(totaalbytesize) + "\n")
        resultsfile.write("Files list:")
        resultsfile.write("-------------\n")


        for entry in dirlist:
            if os.path.isfile(entry):
                resultsfile.write(entry + "\n")

    resultsfile.close()

if __name__ == "__main__":
    main()