from zipfile import ZipFile
import os.path

DIR = os.path.dirname(__file__) + "/pictures"

while True:
    archive = input("Введите название архива .zip без расширения:\n") + ".zip"

    if os.path.isfile(os.path.dirname(__file__) + f"/{archive}"):
        with ZipFile(archive, "r") as zip_file:
            zip_file.extractall(DIR)
            print("Распаковка успешно завершена!")
            break
    else:
        print("Файла с таким названием не существует.")
