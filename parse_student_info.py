import os
import re
import zipfile
from tqdm import tqdm

# 列出目錄中的所有文件
directory = "1718886918_131___CSIE3005-01-Final_Project_submissions"
files = os.listdir(directory)

# 提取學號和名字
student_info = []
pattern = re.compile(r"^(.*?)#_(.*?) \((.*?)\)_")

for file in tqdm(files, desc="Processing files"):
    match = pattern.match(file)
    if match:
        student_id = match.group(1)
        student_name = match.group(2)
        student_english_name = match.group(3)
        student_info.append((student_id, student_name, student_english_name))

        # 解壓縮 .zip 文件到 ./submissions/{學號}/ 底下
        zip_path = os.path.join(directory, file)
        extract_path = os.path.join('submissions', student_id)
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

# 打印學號和名字
for info in student_info:
    print(f"學號: {info[0]}, 名字: {info[1]}, 英文名字: {info[2]}")

# 計算總共多少學生
total_students = len(student_info)
print(f"總共學生數: {total_students}")
