import csv
import random
from typing import List, Dict

def read_student_ids(file_path: str) -> List[str]:
    student_ids = set()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_ids.add(row['student_dir'])
    return sorted(list(student_ids))  # Sort the list to ensure consistent order

def create_groups(student_ids: List[str], group_size: int = 6) -> List[List[str]]:
    random.seed(42)  # Set a fixed seed for reproducibility
    shuffled_ids = student_ids.copy()
    random.shuffle(shuffled_ids)
    groups = [shuffled_ids[i:i+group_size] for i in range(0, len(shuffled_ids), group_size)]
    return groups

def write_groups_to_file(groups: List[List[str]], output_file: str):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Group', 'Student IDs'])
        for i, group in enumerate(groups, 1):
            writer.writerow([f'Group {i}', ', '.join(group)])

def main():
    input_file = 'results.csv'
    output_file = 'student_groups.csv'
    group_size = 6

    student_ids = read_student_ids(input_file)
    groups = create_groups(student_ids, group_size)
    write_groups_to_file(groups, output_file)

    total_students = sum(len(group) for group in groups)
    print(f"總共有 {total_students} 名學生")
    print(f"學生已被分成 {len(groups)} 組，每組 {group_size} 人")
    for group in groups:
        if len(group) < group_size:
            print(f"注意：有一組人數不足 {group_size} 人")
            break
    print(f"分組結果已寫入 {output_file}")

if __name__ == "__main__":
    main()