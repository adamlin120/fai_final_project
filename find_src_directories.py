import os
import pandas as pd
from tqdm import tqdm

# 列出 submissions 目錄中的所有學生目錄
# submissions_dir = 'submissions'
submissions_dir = 're-submissions'
student_dirs = [d for d in os.listdir(submissions_dir) if os.path.isdir(os.path.join(submissions_dir, d))]

# 查找每個學生的 src 目錄
student_src_info = []

for student_id in tqdm(student_dirs, desc="Finding src directories"):
    src_path = None
    for root, dirs, files in os.walk(os.path.join(submissions_dir, student_id)):
        if 'agent.py' in files:
            src_path = root
            break
    
    student_src_info.append((student_id, src_path))
# 將結果保存成 CSV 文件
df = pd.DataFrame(student_src_info, columns=['學號', 'src目錄'])
df.to_csv('student_src_info.csv', index=False)

# 打印結果
for info in student_src_info:
    print(f"學號: {info[0]}, src目錄: {info[1]}")
