import os
import shutil
import filecmp
import json

def list_files(directory):
    files = []
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        if os.path.isfile(full_path):
            files.append(file)
    return files

def compare_directories(dir1, dir2):
    
    dcmp = filecmp.dircmp(dir1, dir2)
    return dcmp.diff_files, dcmp.common_files, dcmp.left_only, dcmp.right_only

def copy_file(src, dest):
    shutil.copy2(src, dest)

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File not found: {file_path}")
    except PermissionError as e:
        print(f"PermissionError: {e}. Unable to delete file: {file_path}")

def synchronize(source_dir, target_dir):
    diff_files, common_files, left_only, right_only = compare_directories(source_dir, target_dir)

    [copy_file(os.path.join(source_dir, file), os.path.join(target_dir, file)) for file in diff_files + common_files]

    [copy_file(os.path.join(source_dir, file), os.path.join(target_dir, file)) for file in left_only]

    [delete_file(os.path.join(target_dir, file)) for file in right_only]

def read_config(file_path = "config.json"):
    with open(file_path, "r") as config_file:
        config_data = json.load(config_file)
    return config_data

def synchronize_from_config():
    config = read_config()
    source_directory = config["source_directory"]
    target_directory = config["target_directory"]
    synchronize(source_directory, target_directory)

if __name__ == "__main__":
    synchronize_from_config()
