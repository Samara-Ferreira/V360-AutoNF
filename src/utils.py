from config import SAMPLES_DIR

def choose_file():
    """
    Function able to user choose the file to be processed, PDF or image.
    """
    available_files = [
        f for f in SAMPLES_DIR.iterdir() 
        if f.is_file()
    ]

    for i, file in enumerate(available_files, start=1):
        print(f"[{i}] {file.name}")
        i += 1

    choice = int(input("Enter the number of the file to process: ")) - 1

    if 0 <= choice < len(available_files):
        return available_files[choice]
    else:
        print("Invalid choice. Please try again.")
        return None
    