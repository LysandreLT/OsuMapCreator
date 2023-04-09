import os
import shutil
import zipfile
import librosa as librosa



def readZip(file: str):
    with zipfile.ZipFile(file, mode="r") as archive:
        return archive.namelist()


def isArchive(file: str):
    return zipfile.is_zipfile(file)


def isOSZFile(file: str):
    # return file.split(".")[-1] != "osz"
    name = file.split(".")
    if name[-1] != "osz":
        print(f"File '{file}' is not an .osz file")
        return False
    else:
        return True

    # if zipfile.is_zipfile(fileName):
    #     with zipfile.ZipFile(fileName, "r") as archive:
    #         archive.printdir()
    # else:
    #     print("File is not an .osz file")


def extractAll(file: str, dirPath: str):
    """
    :param file: file path of the zip to extract
    :param dirPath: directory in which the zip will be extracted
    """
    with zipfile.ZipFile(file, 'r') as zip:
        # extracting all the files
        zip.extractall(path=dirPath)


def extract(file: str, zip_path: str, destDirPath: str):
    """
    :param file: file in the zipfile to extract
    :param zip_path : file path of the zip
    :param destDirPath: directory in which the zip will be extracted
    """
    with zipfile.ZipFile(zip_path, 'r') as zip:
        # extracting all the files
        zip.extract(member=file, path=destDirPath)


# def deleteFileAfterExtraction(file):
#     if os.path.exists(file):
#         os.remove(file)
#     else:
#         print("The file does not exist")
#
#
def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths


def write_archive(file_paths, name: str):
    """
    :param file_paths: list of files to zip
    :param name: name of the zip file
    """
    # writing files to a zipfile
    with zipfile.ZipFile(f'{name}.osz', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
    print('All files zipped successfully!')


def write_osz_archive(directory: str, name: str):
    """
    :param directory: directory in which the zip will be created
    :param name: name of the zip file
    """
    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
    write_archive(file_paths, name)


# def write(content, path: str, name: str, type: Type):
#     with open(f'{os.path.join(path, name)}.{type.value}', 'w') as f:
#         f.write(json.dumps(content, indent=2))


def selectList(list):
    new_list = []
    for item in list:
        ext = item.split(".")
        if ext[-1] == "osu" or ext[-1] == "mp3" or ext[-1] == "ogg":
            new_list.append(item)

    return new_list


def get_duration(path):
    y, sr = librosa.load(path, sr=44100)
    return librosa.get_duration(y=y, sr=sr)


def post_treatment(path: str):
    if os.path.isdir(path):
        list = os.listdir(path)
        for file in list:
            if file.split(".")[-1] != "osu":
                duration = get_duration(os.path.join(path, file))
                if duration < 20:
                    delete_tree(os.path.join(path, file))
    else:
        if path.split(".")[-1] != "osu":
            duration = get_duration(os.path.realpath(path))
            if duration < 20:
                delete_tree(path)


def clean_archive_folder(path: str, dest: str) -> None:
    for entry in os.scandir(path):
        # if file go to clean archive else clean folder again
        if entry.is_file():
            if dest.find("/temp"):
                dest = dest.replace("/temp", "/maps")
            clean_archive(entry.path, dest)
        else:
            clean_archive_folder(entry.path, dest)


def delete_tree(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    else:
        print("path doesn't exists")


def clean_archive(path: str, dest: str):
    if isArchive(path) and isOSZFile(path):
        dir_path = dest + "/maps/" + ".".join(os.path.basename(path).split(".")[:-1])
        if dest.find("/maps/maps") or dest.find("/maps//maps"):
            dir_path = dir_path.replace("/maps//maps", "/maps").replace("/maps/maps", "/maps")

        clean_list = selectList(readZip(path))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            # os.makedirs(dir_path)
        for items in clean_list:
            extract(items, path, dir_path)
        post_treatment(dir_path)
    elif isArchive(path):
        temp_path = dest + "/temp/"
        extractAll(path, temp_path)
        clean_archive_folder(temp_path, dest)


# def parse(path):
#     parser = beatmapparser.BeatmapParser()
#     parser.parseFile(path)
#     parser.build_beatmap()
#     return parser.beatmap
