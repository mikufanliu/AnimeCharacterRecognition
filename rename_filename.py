# -*- coding:utf-8 -*-
import os

PATH = "C:\\Users\\LMonster\\Desktop\\test"
FILE_TYPE = ".jpg"


def rename_file(path, new_name="", start_num=0, file_type=""):
    if not os.path.exists(path):
        print("folder %s is not exist" % path)
        return

    count = start_num
    files = os.listdir(path)
    for file in files:
        old_path = os.path.join(path, file)
        if os.path.isfile(old_path):
            if file_type == "":
                file_type = os.path.splitext(old_path)[1]
            new_path = os.path.join(path, new_name + str(count) + file_type)
            print(new_path)
            print(file_type)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                count = count + 1
    print("Renamed %d file(s)" % (count - start_num))


def main():
    rename_file(PATH, file_type=FILE_TYPE)


if __name__ == '__main__':
    main()

