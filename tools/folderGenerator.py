import os
import argparse

def generateFolders(startIndex, endIndex, forceMakeDirectory=False):
    maxIndex = 999
    minIndex = 0
    includeUpperBound = 1
    
    # check that startIndex and endIndex are positive integers
    if not (isinstance(startIndex, int) and isinstance(endIndex, int) and startIndex >= minIndex and endIndex > minIndex):
        raise ValueError("startIndex and endIndex must be positive integers")
    # check that startIndex and endIndex are less than or equal to maxIndex
    if startIndex > maxIndex or endIndex > maxIndex:
        raise ValueError(f"startIndex and endIndex must be less than or equal to {maxIndex}")
    # check that startIndex is less than endIndex
    if startIndex >= endIndex:
        raise ValueError("startIndex must be less than endIndex")
    
    for i in range(startIndex, endIndex + includeUpperBound):
        folder_name = "{:03d}".format(i)
        if os.path.exists(folder_name):
            if forceMakeDirectory:
                print(f"{folder_name} already exists. forceMakeDirectory is True. Directory will be deleted and recreated.")
                os.rmdir(folder_name)
                os.makedirs(folder_name)
            else:
                print(f"{folder_name} already exists.")
        else:
            os.makedirs(folder_name)
            print(f"{folder_name} directory created.")

def main():
    parser = argparse.ArgumentParser(description='Create folders between start and end')
    parser.add_argument('-start', type=int, default=0, help='The starting count for folders to create')
    parser.add_argument('-end', type=int, default=10, help='The ending count for folders to create')
    parser.add_argument('-force', action='store_true', help='if set, will delete folder if it exists and create a new folder')
    args = parser.parse_args()

    generateFolders(args.start, args.end, args.force)

"""
README
Written for Python 3.8

This script is useful for generating folder so you don't need to manually.

I generally split clips with multiple scenes I am processing into different folders to keep track of the work and avoid large render cycles.
This makes it easier for me to parrelize workstreams vs doing everything at once. This does not apply to clips with one scene.
"""
if __name__ == '__main__':
    main()
