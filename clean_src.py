import pandas as pd

df = pd.read_csv("student_src_info.csv")
# 如果有重複的學號，保留最後一個出現的記錄
df = df.drop_duplicates(subset='學號', keep='last')

# 將處理後的資料寫回CSV檔案
df.to_csv("student_src_info_cleaned.csv", index=False)

print("已移除重複學號，並保留最後一個記錄。結果已保存到 student_src_info_cleaned.csv")
