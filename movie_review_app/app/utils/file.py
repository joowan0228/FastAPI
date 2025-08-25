import os

async def upload_file(file, folder: str):
    path = f"{folder}/{file.filename}"
    os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as f:
        f.write(await file.read())
    return path

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)
