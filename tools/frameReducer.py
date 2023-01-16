import argparse
import os
import shutil
from typing import Optional

def copy_images(src_dir: str, dest_dir: str, n: Optional[int] = 2):
    if not os.path.exists(src_dir):
        raise ValueError(f"Source directory {src_dir} does not exist.")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Destination directory {dest_dir} created.")
        
    print(f"Copy Started. N is {n}.")

    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = [file for file in os.listdir(src_dir) if file.endswith(image_extensions)]

    for i, image_file in enumerate(image_files):
        if (i + 1) % n == 0:
            shutil.copy2(os.path.join(src_dir, image_file), os.path.join(dest_dir, image_file))
    
    print(f"Copy completed.")

"""
README
Written for Python 3.8

This script is useful for copying images from one directory to another with the ability to skip certain number of images. 
With this script, you can easily copy a subset of images from one directory to another.

You can run the script by running the command:
    python scriptname.py -src /path/to/src/dir -dest /path/to/dest/dir -n 2

It will copy every Nth image from the source directory to the destination directory, where N is the number of images to skip. 

If the destination directory doesn't exist, it will be created.
"""
def main():
    parser = argparse.ArgumentParser(description='Copy every N image from a source directory to a destination directory.')
    parser.add_argument('-src', type=str, help='The source directory of images')
    parser.add_argument('-dest', type=str, help='The destination directory of images')
    parser.add_argument('-n', '--skip', type=int, default=2, help='The number of images to skip')
    args = parser.parse_args()

    copy_images(args.src, args.dest, args.skip)

if __name__ == '__main__':
    main()
