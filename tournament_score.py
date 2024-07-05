import pandas as pd
import csv
import subprocess


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

    # 打印每個學生的分數並保存到 pandas DataFrame
    print("PK 比賽結果:")
    student_scores = []
    for student_id in pk_resutls:
        score = pk_resutls[student_id]
        match_count = student_match_count[student_id]
        if match_count != 5:
            print(f"警告：{student_id} 只參加了 {match_count} 場比賽")
        print(f"{student_id}: {score} 分 ({match_count} 場比賽)")
        student_scores.append({"學號": student_id, "分數": score, "比賽場次": match_count})
    
    # 創建 pandas DataFrame
    scores_df = pd.DataFrame(student_scores)
    print("\n學生分數 DataFrame:")
    print(scores_df)
    print(scores_df.describe())
    
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

    if not missing_matches:
        print("所有比賽都已經進行")
    # 讀取 cool 格式的成績單
    cool_df = pd.read_csv('2024-07-05T0903_成績-人工智慧導論_(CSIE3005-01).csv')
    all_students = cool_df['SIS Login ID'].str.split('@').str[0]
    all_students = set(all_students)
    print(f"cool_df 中的學生數：{len(all_students)}")

    # 檢查所有 student_total_scores 是否都在 cool_df 中
    missing_students = []
    for student_id in scores_df['學號']:
        if student_id not in all_students:
            missing_students.append(student_id)

    if missing_students:
        print("以下學生不在 cool_df 中：")
        for student in missing_students:
            print(student)
    else:
        print("所有學生都在 cool_df 中。")

        # 將學號轉換為小寫以確保匹配
        cool_df['SIS Login ID'] = cool_df['SIS Login ID'].str.lower()
        scores_df['學號'] = scores_df['學號'].str.lower()

        # 創建一個字典，將學號映射到相應的分數
        score_dict = scores_df.set_index('學號')['分數'].to_dict()

        # 更新 cool_df 中的分數
        cool_df['Round-Robin Tournament (239009)'] = cool_df['SIS Login ID'].str.split('@').str[0].map(score_dict)

        # 將更新後的 cool_df 寫回 CSV 檔案
        cool_df.to_csv('2024-07-05T0903_成績-人工智慧導論_(CSIE3005-01)_updated.csv', index=False)

        print("分數已成功寫入 cool_df 並保存為新的 CSV 檔案。")

        # 單淘汰賽
        print("開始單淘汰賽")

        # 讀取 pk_results.csv
        pk_results = pd.read_csv('pk_results.csv')
        pk_results.columns = ['player1', 'player2', 'win1', 'win2', 'draw', 'stack1', 'stack2']

        # 計算每位玩家的總分（左邊的錢總和）
        player_scores = {}
        for _, row in pk_results.iterrows():
            player_scores[row['player1']] = player_scores.get(row['player1'], 0) + row['stack1']
            player_scores[row['player2']] = player_scores.get(row['player2'], 0) + row['stack2']

        # 選出前32名玩家
        top_32 = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)[:32]
        top_32_players = [player for player, _ in top_32]

        print(f"前32名玩家：{top_32_players}")
        # 印出前32名玩家及其堆疊
        print("前32名玩家及其堆疊：")
        for player, score in top_32:
            print(f"{player}: {score:.2f}")

        # 模擬單淘汰賽
        def simulate_match(player1, player2):
            # 重新讀取 pk_results.csv
            pk_results = pd.read_csv('single_elimination_pk_results.csv')
            
            # 找出最新的比賽結果
            try:
                latest_match = pk_results[(pk_results['student1_id'] == player1) & (pk_results['student2_id'] == player2)].iloc[-1]
            except IndexError:
                try:
                    latest_match = pk_results[(pk_results['student1_id'] == player2) & (pk_results['student2_id'] == player1)].iloc[-1]
                except IndexError:
                    print(f"python single_elimination.py {winners[i]} {winners[i+1]}")
                    return "PESUDO_WINNER"

            if latest_match['student1_wins'] > latest_match['student2_wins']:
                winner = latest_match['student1_id']
            elif latest_match['student2_wins'] > latest_match['student1_wins']:
                winner = latest_match['student2_id']
            else:
                # 如果平手，根據堆疊決定勝者
                winner = latest_match['student1_id'] if latest_match['student1_stack'] > latest_match['student2_stack'] else latest_match['student2_id']
            
            print(f"{player1} vs {player2} -> 勝者：{winner}")
            return winner

        # 進行單淘汰賽
        winners = top_32_players
        round_num = 1
        while len(winners) > 1:
            print(f"\n第 {round_num} 輪")
            next_round = []
            for i in range(0, len(winners), 2):
                if i + 1 < len(winners):
                    winner = simulate_match(winners[i], winners[i+1])
                    next_round.append(winner)
                else:
                    next_round.append(winners[i])
                    print(f"{winners[i]} 輪空")
            if len(next_round) <= 4:
                print(f"第 {round_num} 輪結束")
                print(f"對手：{next_round}")
            winners = next_round
            round_num += 1


if __name__ == '__main__':
    main()
