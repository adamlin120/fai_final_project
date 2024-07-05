import pandas as pd

# 讀取 results.csv 檔案
results_df = pd.read_csv('results.csv')

# 為欄位命名
results_df.columns = ['學號', 'opponent', '勝場數', '平局數', '我方分數', '對方分數', '積分']

# 計算每個學生的baseline* as new column: "Baseline Competition (239007)"
# 計算每個學生的baseline*分數
baseline_scores = results_df[results_df['opponent'].str.startswith('baseline')].groupby('學號')['積分'].sum()

# 計算每個學生的strong*分數
strong_scores = results_df[results_df['opponent'].str.startswith('strong')].groupby('學號')['積分'].sum()

# 創建新的DataFrame，包含學號、baseline*分數和strong*分數
student_total_scores = pd.DataFrame({
    '學號': baseline_scores.index,
    'Baseline Competition (239007)': baseline_scores.values,
    'Unseen Agent Competition (239008)': strong_scores.values
})

# 將新列加入原始DataFrame
results_df = results_df.merge(student_total_scores, on='學號', how='left')

# 顯示結果
print(student_total_scores)

# print minimum and maximum of each column
print(student_total_scores.describe())

cool_df = pd.read_csv('2024-07-05T0903_成績-人工智慧導論_(CSIE3005-01).csv')
all_students = cool_df['SIS Login ID'].str.split('@').str[0]
all_students = set(all_students)
print(f"cool_df 中的學生數：{len(all_students)}")

# 檢查所有 student_total_scores 是否都在 cool_df 中
missing_students = []
for student_id in student_total_scores['學號']:
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
    student_total_scores['學號'] = student_total_scores['學號'].str.lower()

    # 創建一個字典，將學號映射到相應的分數
    score_dict = student_total_scores.set_index('學號').to_dict()

    # 更新 cool_df 中的分數
    cool_df['Baseline Competition (239007)'] = cool_df['SIS Login ID'].str.split('@').str[0].map(score_dict['Baseline Competition (239007)'])
    cool_df['Unseen Agent Competition (239008)'] = cool_df['SIS Login ID'].str.split('@').str[0].map(score_dict['Unseen Agent Competition (239008)'])

    # 將更新後的 cool_df 寫回 CSV 檔案
    cool_df.to_csv('2024-07-05T0903_成績-人工智慧導論_(CSIE3005-01)_updated.csv', index=False)

    print("分數已成功寫入 cool_df 並保存為新的 CSV 檔案。")
