import os


def relative_file(file_obj, *paths):
    path_to_file = os.path.dirname(os.path.abspath(file_obj))
    return os.path.abspath(os.path.join(path_to_file, *paths))
