import os

def load_documents(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path):
            files.append(path)
    return files