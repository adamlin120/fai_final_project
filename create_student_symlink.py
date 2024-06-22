import os
import csv
from pathlib import Path

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def create_symlinks(student_data):
    current_dir = Path.cwd()
    for student in student_data:
        student_id = student['學號']
        src_dir = student['src目錄']
        
        if src_dir:
            src_path = Path(src_dir)
            
            if src_path.exists() and src_path.is_dir():
                symlink_path = current_dir / student_id
                
                # Remove existing symlink if it exists
                if symlink_path.exists():
                    symlink_path.unlink()
                
                # Create new symlink
                os.symlink(src_path, symlink_path, target_is_directory=True)
                print(f"Created symlink for {student_id}")
            else:
                print(f"Skipping {student_id} (src directory not found)")
        else:
            # Remove existing symlink if it exists
            symlink_path = current_dir / student_id
            if symlink_path.exists():
                if symlink_path.is_symlink():
                    symlink_path.unlink()
                    print(f"Removed existing symlink for {student_id}")
                else:
                    print(f"Warning: {student_id} exists but is not a symlink. Skipping removal.")
            print(f"Skipping {student_id} (src directory is None or invalid)")

if __name__ == "__main__":
    student_file_path = 'student_src_info.csv'
    student_data = read_csv(student_file_path)
    create_symlinks(student_data)
