import os, sys

FILE_ENDING = ".py"


def main():
    HEADER = """\
# -*- coding: utf-8 -*-
"""

    filelist = []
    for path, dir, files in os.walk(sys.argv[1]):
        if "/." not in path:
            for file in files:
                if file.endswith(FILE_ENDING):
                    filelist.append(path + os.sep + file)

    for filename in filelist:
        try:
            inbuffer = open(filename, "r").readlines()
            outbuffer = [HEADER] + inbuffer

            open(filename, "w").writelines(outbuffer)
            print(f"Header is added to the file: '{filename}'.")
        except IOError:
            print(
                "Please check the files, there was an error when trying to open %s..."
                % filename
            )
        except:
            print("Unexpected error ocurred while processing files...")


if __name__ == "__main__":
    main()
