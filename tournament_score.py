import pandas as pd
import csv


def main():
    df = pd.read_csv("results.csv")
    all_student_id_have_baseline_scores = set(df['student_dir'])

    """Tour rule
    Round-Robin Tournament
    Each player is randomly assigned into a group of 6 people
    5 opponents in total
    Winners for the matches will get 2 points. E.g. You can get maximum 10 points if you win all matches
    If there's a tie in match wins, the winner is determined based on the result of the match between the tied participants.
    """
    pk_df = pd.read_csv("pk_results.csv")
    """
    student1_id,student2_id,student1_wins,student2_wins,num_ties,student1_stack,student2_stack
    b12902098,b09602017,1,4,0,1840,8160
    b10902025,b10902100,2,3,0,4288.9765625,5700
    b09902122,b10902076,1,4,0,2000,7995
    b09902122,b10902075,3,2,0,6390,3610
    b09902018,b10902004,1,4,0,4900,5100
    """
    # for each student, calculate the total score
    pk_resutls = {}
    student_match_count = {}
    total_matches = 0
    
    for _, row in pk_df.iterrows():
        student1_id = row['student1_id']
        student2_id = row['student2_id']
        student1_wins = row['student1_wins']
        student2_wins = row['student2_wins']
        
        # 初始化學生分數和比賽次數
        for student_id in [student1_id, student2_id]:
            if student_id not in pk_resutls:
                pk_resutls[student_id] = 0
            if student_id not in student_match_count:
                student_match_count[student_id] = 0
        
        # 計算並加上分數
        if student1_wins > student2_wins:
            pk_resutls[student1_id] += 2
        elif student2_wins > student1_wins:
            pk_resutls[student2_id] += 2
        
        # 增加學生的比賽次數
        student_match_count[student1_id] += 1
        student_match_count[student2_id] += 1
        
        # 增加總比賽次數
        total_matches += 1

    # 打印結果
    print("PK 比賽結果:")
    for student_id in pk_resutls:
        score = pk_resutls[student_id]
        match_count = student_match_count[student_id]
        if match_count != 5:
            print(f"警告：{student_id} 只參加了 {match_count} 場比賽")
        # print(f"{student_id}: {score} 分 ({match_count} 場比賽)")
    print(f"Number of students in results.csv: {len(all_student_id_have_baseline_scores)}")
    print(f"參與 PK 比賽的學生數量: {len(pk_resutls)}")
    print(f"總共有 {total_matches} 場比賽")
    
    # 檢查總比賽場次是否符合預期
    expected_total_matches = 33 * 15 + 3
    if total_matches != expected_total_matches:
        print(f"警告：總比賽場次 ({total_matches}) 與預期 ({expected_total_matches}) 不符, 還少 {expected_total_matches - total_matches} 場比賽")
    
    # 檢查每位學生的比賽場次
    students_with_incorrect_matches = [student_id for student_id, count in student_match_count.items() if count != 5]
    if students_with_incorrect_matches:
        print(f"警告：以下學生的比賽場次不是 5 場：{', '.join(students_with_incorrect_matches)}")
    
    # 讀取學生分組資訊
    student_groups = {}
    with open('student_groups.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            group = row['Group']
            students = [s.strip() for s in row['Student IDs'].split(',')]
            for student in students:
                student_groups[student] = group

    # 初始化每個學生的對手列表
    student_opponents = {student: set() for student in student_groups.keys()}

    # 計算每個學生的比賽次數和對手
    for _, row in pk_df.iterrows():
        student1_id = row['student1_id']
        student2_id = row['student2_id']
        
        if student1_id in student_opponents and student2_id in student_opponents:
            student_opponents[student1_id].add(student2_id)
            student_opponents[student2_id].add(student1_id)

    # 檢查缺少的比賽
    missing_matches = []
    for student, group in student_groups.items():
        group_members = [s for s, g in student_groups.items() if g == group and s != student]
        for opponent in group_members:
            if opponent not in student_opponents[student]:
                missing_matches.append((student, opponent))

    # 打印缺少的比賽
    print("缺少的比賽：")
    for match in missing_matches:
        print(f"{match[0]} vs {match[1]}")

    print(f"總共缺少 {len(missing_matches)} 場比賽")

if __name__ == '__main__':
    main()
