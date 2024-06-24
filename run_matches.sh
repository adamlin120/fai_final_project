#!/bin/bash

# 檢查 student_groups.csv 文件是否存在
if [ ! -f "student_groups.csv" ]; then
    echo "Error: student_groups.csv file not found!"
    exit 1
fi

# 創建日誌目錄
mkdir -p pk_logs

# 跳過標題行，讀取每一組
tail -n +2 student_groups.csv | while IFS=',' read -r group students; do
    echo "Processing $group"
    
    # 將學生 ID 轉換為數組
    IFS=', ' read -ra student_array <<< "$students"
    
    # 獲取組內學生數量
    num_students=${#student_array[@]}
    
    # 對組內學生進行兩兩配對
    for ((i=0; i<num_students; i++)); do
        for ((j=i+1; j<num_students; j++)); do
            sid1=$(echo ${student_array[i]} | tr -d '"')
            sid2=$(echo ${student_array[j]} | tr -d '"')
            log_file="pk_logs/${sid1}_vs_${sid2}.log"
            echo "Running: python pk.py $sid1 $sid2 > $log_file 2>&1"
            python pk.py "$sid1" "$sid2" > "$log_file" 2>&1 &
        done
    done
    
    echo "Finished processing $group"
    echo "------------------------"
done

# 等待所有後台任務完成
wait

echo "All matches completed!"