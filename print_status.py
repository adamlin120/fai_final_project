import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import os

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def read_scores(file_path):
    scores = defaultdict(list)
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == 'student_dir':  # Ensure the header row is skipped
                continue
            student_id, _, _, points_earned = row
            scores[student_id].append(float(points_earned))
    return scores

def calculate_statistics(data, scores):
    total_students = len(data)
    completed_students = sum(1 for row in data if row['學號'] in scores)
    incomplete_students = total_students - completed_students

    return {
        'total_students': total_students,
        'completed_students': completed_students,
        'incomplete_students': incomplete_students,
        'completion_rate': (completed_students / total_students) * 100
    }

def calculate_score_distribution(scores):
    distribution = defaultdict(int)
    for student_id, points in scores.items():
        total_score = sum(points)
        distribution[total_score] += 1
    return distribution

def count_students_in_logs():
    log_files = os.listdir('logs')
    student_ids = set()
    for file in log_files:
        if file.endswith('.log'):
            student_ids.add(file.split('.')[0])
    return len(student_ids)

def print_statistics(stats, score_distribution, logs_count):
    print(f"Total Students: {stats['total_students']}")
    print(f"Completed Students: {stats['completed_students']}")
    print(f"Incomplete Students: {stats['incomplete_students']}")
    print(f"Completion Rate: {stats['completion_rate']:.2f}%")
    print(f"Students in logs: {logs_count}")

def plot_score_distribution(score_distribution):
    scores = list(score_distribution.keys())
    counts = list(score_distribution.values())

    plt.figure(figsize=(12, 6))
    plt.bar(scores, counts)
    plt.xlabel('Score')
    plt.ylabel('Number of Students')
    plt.title('Score Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('score_distribution.png')
    plt.close()

if __name__ == "__main__":
    student_file_path = 'student_src_info.csv'
    scores_file_path = 'results.csv'

    student_data = read_csv(student_file_path)
    scores = read_scores(scores_file_path)
    stats = calculate_statistics(student_data, scores)
    score_distribution = calculate_score_distribution(scores)
    logs_count = count_students_in_logs()

    print_statistics(stats, score_distribution, logs_count)
    plot_score_distribution(score_distribution)
    print("Score distribution plot saved as 'score_distribution.png'")
