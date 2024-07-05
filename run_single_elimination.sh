#!/bin/bash


# 創建日誌目錄
mkdir -p single_elimination_logs

# # 第 1 輪
# python single_elimination.py b10401008 b11902114 > single_elimination_logs/b10401008_vs_b11902114.log 2>&1 &
# python single_elimination.py b11902072 b06401151 > single_elimination_logs/b11902072_vs_b06401151.log 2>&1 &
# python single_elimination.py b11705011 b10902015 > single_elimination_logs/b11705011_vs_b10902015.log 2>&1 &
# python single_elimination.py b10902072 b08705058 > single_elimination_logs/b10902072_vs_b08705058.log 2>&1 &
# python single_elimination.py b11902087 b10902101 > single_elimination_logs/b11902087_vs_b10902101.log 2>&1 &
# python single_elimination.py b10902071 b10201026 > single_elimination_logs/b10902071_vs_b10201026.log 2>&1 &
# python single_elimination.py b10902003 b10902079 > single_elimination_logs/b10902003_vs_b10902079.log 2>&1 &
# python single_elimination.py b10902127 b10902070 > single_elimination_logs/b10902127_vs_b10902070.log 2>&1 &
# python single_elimination.py b11902138 b11902043 > single_elimination_logs/b11902138_vs_b11902043.log 2>&1 &
# python single_elimination.py b10902017 b10902118 > single_elimination_logs/b10902017_vs_b10902118.log 2>&1 &
# python single_elimination.py b09901142 b09303016 > single_elimination_logs/b09901142_vs_b09303016.log 2>&1 &
# python single_elimination.py b10902086 b09705002 > single_elimination_logs/b10902086_vs_b09705002.log 2>&1 &
# python single_elimination.py b11505050 b09902122 > single_elimination_logs/b11505050_vs_b09902122.log 2>&1 &
# python single_elimination.py b11902027 b10902125 > single_elimination_logs/b11902027_vs_b10902125.log 2>&1 &
# python single_elimination.py b10902121 b09203001 > single_elimination_logs/b10902121_vs_b09203001.log 2>&1 &
# python single_elimination.py b10902042 b10902002 > single_elimination_logs/b10902042_vs_b10902002.log 2>&1 &

# # 等待所有比賽完成
# wait

# echo "第 1 輪比賽已完成！"

# # 第 2 輪
# python single_elimination.py b11902114 b11902072 > single_elimination_logs/b11902114_vs_b11902072.log 2>&1 &
# python single_elimination.py b10902015 b10902072 > single_elimination_logs/b10902015_vs_b10902072.log 2>&1 &
# python single_elimination.py b10902101 b10902071 > single_elimination_logs/b10902101_vs_b10902071.log 2>&1 &
# python single_elimination.py b10902003 b10902127 > single_elimination_logs/b10902003_vs_b10902127.log 2>&1 &
# python single_elimination.py b11902138 b10902017 > single_elimination_logs/b11902138_vs_b10902017.log 2>&1 &
# python single_elimination.py b09901142 b10902086 > single_elimination_logs/b09901142_vs_b10902086.log 2>&1 &
# python single_elimination.py b11505050 b10902125 > single_elimination_logs/b11505050_vs_b10902125.log 2>&1 &
# python single_elimination.py b09203001 b10902042 > single_elimination_logs/b09203001_vs_b10902042.log 2>&1 &

# # 等待所有比賽完成
# wait

# echo "第 2 輪比賽已完成！"

# # 第 3 輪
# python single_elimination.py b11902114 b10902015 > single_elimination_logs/b11902114_vs_b10902015.log 2>&1 &
# python single_elimination.py b10902101 b10902127 > single_elimination_logs/b10902101_vs_b10902127.log 2>&1 &
# python single_elimination.py b11902138 b10902086 > single_elimination_logs/b11902138_vs_b10902086.log 2>&1 &
# python single_elimination.py b10902125 b09203001 > single_elimination_logs/b10902125_vs_b09203001.log 2>&1 &

# # 等待所有比賽完成
# wait

# echo "第 3 輪比賽已完成！"

# # 第 4 輪
# python single_elimination.py b10902015 b10902127 > single_elimination_logs/b10902015_vs_b10902127.log 2>&1 &
# python single_elimination.py b10902086 b10902125 > single_elimination_logs/b10902086_vs_b10902125.log 2>&1 &

# # 等待所有比賽完成
# wait

# echo "第 4 輪比賽已完成！"

# 第 5 輪
python single_elimination.py b10902015 b10902125 > single_elimination_logs/b10902015_vs_b10902125.log 2>&1 &

# 等待比賽完成
wait

echo "第 5 輪比賽已完成！"

# 3、4 名決賽
python single_elimination.py b10902127 b10902086 > single_elimination_logs/b10902127_vs_b10902086.log 2>&1 &

# 等待比賽完成
wait

echo "3、4 名決賽已完成！"

echo "單淘汰賽全部完成！"
