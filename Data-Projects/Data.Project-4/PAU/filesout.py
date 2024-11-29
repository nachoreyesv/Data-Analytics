import os
import shutil

def move_files(source_folders, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Move files from source folders to the destination folder
    for folder in source_folders:
        for file_name in os.listdir(folder):
            source_file = os.path.join(folder, file_name)
            if os.path.isfile(source_file):
                shutil.move(source_file, destination_folder)

# Define source folders and destination folder
for i in range(0,22):
    source_folders = [f"../GABRIELA/train_modificado_jpg/{i}"]
    destination_folder = "../train_clean"
    # Move files from source folders to destination folder
    move_files(source_folders, destination_folder)
