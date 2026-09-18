import os


def load_documents(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".txt"):

            path = os.path.join(folder_path, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append({
                "file": file,
                "content": text
            })

    return documents