import os
import shutil

def static_to_public(static_dir=os.path.join('.', 'static'), public_dir=os.path.join('.', 'public'), next_dir=None):
    if next_dir:
        static_dir = os.path.join(static_dir, next_dir)
        public_dir = os.path.join(public_dir, next_dir)
    directory_list = []

    static_list = os.listdir(static_dir)
    for file in static_list:
        file_static = os.path.join(static_dir, file)
        file_public = os.path.join(public_dir, file)
        if os.path.isfile(file_static):
            shutil.copy(file_static, public_dir)
        else:
            os.mkdir(file_public)
            directory_list.append(file)

    for directory in directory_list:
        static_to_public(static_dir, public_dir, directory)