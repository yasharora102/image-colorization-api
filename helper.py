import os


def get_file_extension(file_with_extension: str) -> str:
    """

    :param file_with_extension: file name with extension. for ecxample image.png or image.jpeg

    :return: extenstion of image like png jpeg
    """
    list_of_filename_and_format = file_with_extension.split(".")
    file_name = list_of_filename_and_format[0]
    extenstion = list_of_filename_and_format[1]
    return extenstion


def does_file_exist(dir, prefix):
    """
    :param dir: path of directory for find if a file exists in that directory
    :param prefix: name of the file without extension

    :return: return False if the directory doesn't have the file and return True if finds it.
    """
    for s in os.listdir(dir):
        if os.path.splitext(s)[0] == prefix and os.path.isfile(os.path.join(dir, s)):
            return True

    return False


def get_file_with_extension(dir, prefix):
    for s in os.listdir(dir):
        if os.path.splitext(s)[0] == prefix and os.path.isfile(os.path.join(dir, s)):
            return s

    return None
