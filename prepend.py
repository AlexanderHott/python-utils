# -*- coding: utf-8 -*-
# License: MIT
"""This script adds or replaces a header in a type of file.

WARNING: If you have any comments in the beginning of your file, they will be replaced
with the header.

Example:
```
# Bad header
'''Module level docstring'''

print("Hello World!")
# More comments

```
gets converted to:

```
# New header
# That can be on multiple lines
'''Module level docstring'''

print("Hello World!")
# More comments

```
"""
import os, sys

FILE_ENDING = ".py"
COMMENT = "#"
HEADER = """\
# -*- coding: utf-8 -*-
# Copyright (c) 2022-2023 Alexander Ott
"""


def split_buffer(buffer: list[str]) -> tuple[list[str], list[str]]:
    """Returns a tuple with the header section and the rest of the buffer."""
    comment_section = []
    code_section = []

    for i, line in enumerate(buffer):
        if not line.startswith(COMMENT):
            code_section = buffer[i:]
            break
        comment_section.append(line)

    return comment_section, code_section


def main():
    if len(sys.argv) < 2:
        print("Usage: python prepend.py <folder>")
        sys.exit(1)

    file_list = []
    for path, _, files in os.walk(sys.argv[1]):
        if f"{os.sep}." not in path:  # hidden files or folders
            for file in files:
                if file.endswith(FILE_ENDING):
                    file_list.append(path + os.sep + file)

    for filename in file_list:
        try:
            inbuffer = open(filename, "r").readlines()

            # create a list of lines of the header including the \n
            # Note: the last item in the list is a single \n so we don't need to add it
            header_list = [line + "\n" for line in HEADER.split("\n")][:-1]

            comment_section, code_section = split_buffer(inbuffer)
            outbuffer = header_list + code_section

            # if the file is empty add the header
            if not inbuffer:
                open(filename, "w").writelines(outbuffer)
                print(f"Header is added to the file: '{filename}'.")

            # if the file has an old header replace it
            elif header_list != comment_section:
                outbuffer = header_list + code_section
                open(filename, "w").writelines(outbuffer)
                print(f"Header replaced in the file: '{filename}'.")

        except IOError:
            print(
                f"Please check the files, there was an error when trying to open {filename}..."
            )
        except Exception as e:
            print("Unexpected error ocurred while processing files...")
            print(e)


if __name__ == "__main__":
    main()
