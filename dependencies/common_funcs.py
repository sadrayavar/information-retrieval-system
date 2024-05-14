import os


def delete_files(directory):
    for filename in os.listdir(directory):
        # Create the full path to the file
        filepath = os.path.join(directory, filename)
        os.remove(filepath)
