import os
import csv
import sys
import random
import numpy as np
from pathlib import Path
from tqdm import tqdm
from contextlib import redirect_stdout, redirect_stderr

from deck_utils import build_decks
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai

from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai  
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai
from unseen_strong1 import setup_ai as strong1_ai
from unseen_strong2 import setup_ai as strong2_ai
from unseen_strong3 import setup_ai as strong3_ai
from unseen_strong4 import setup_ai as strong4_ai
from unseen_strong5 import setup_ai as strong5_ai


# 讀取 student_src_info.csv 文件
src_info_file = 'student_src_info.csv'
student_src_info = {}
if os.path.exists(src_info_file):
    with open(src_info_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src_path = Path(row['src目錄'])
            if row['src目錄'] and src_path.is_dir():
                student_src_info[row['學號']] = row['src目錄']
            else:
                # print(f"Skipping {row['學號']} (src directory not found)")
                pass

# Get student directory from command-line argument
if len(sys.argv) != 2:
    print("Usage: python test.py <student_dir>")
    sys.exit(1)

student_dir = sys.argv[1]

# Load existing results from CSV file if it exists
results_file = 'results.csv'
existing_results = {}
if os.path.exists(results_file):
    with open(results_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['student_dir'] not in existing_results:
                existing_results[row['student_dir']] = {}
            existing_results[row['student_dir']][row['opponent']] = {
                'games_won': int(row['games_won']),
                'points_earned': float(row['points_earned'])
            }

with open(results_file, 'a', newline='') as f:
    fieldnames = ['student_dir', 'opponent', 'games_won', 'points_earned']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if f.tell() == 0:  # Write header if file is empty
        writer.writeheader()

    if student_dir in existing_results:
        print(f'Skipping {student_dir} (already tested)')
        sys.exit(0)

    # 獲取學生的 src 目錄
    src_path = student_src_info.get(student_dir)
    if not src_path:
        print(f'Skipping {student_dir} (src directory not found)')
        sys.exit(1)

    # 將 src 目錄添加到 sys.path
    sys.path.insert(0, src_path)

    # Load student's setup_ai function
    try:
        student_module = __import__('agent', fromlist=['setup_ai'])
        student_ai = student_module.setup_ai
    except ImportError:
        print(f'Error importing setup_ai for {student_dir}')
        sys.exit(1)
    finally:
        # 從 sys.path 中移除 src 目錄
        sys.path.pop(0)
    
    results = {}

    # Create log directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_out_file = os.path.join(log_dir, f'{student_dir}.out')
    log_err_file = os.path.join(log_dir, f'{student_dir}.err')

    with open(log_out_file, 'w', buffering=1) as log_out_f, open(log_err_file, 'w', buffering=1) as log_err_f:  # Use buffering=0 for completely unbuffered
        with redirect_stdout(log_out_f), redirect_stderr(log_err_f):
            # Play against each baseline AI
            for i in range(1, 8):
                desc = f'{student_dir} vs baseline{i}'
                baseline_ai = globals()[f'baseline{i}_ai']
                
                student_points = 0
                baseline_points = 0

                # create deck for BO5
                decks = build_decks()
                # Play 5 games (BO5)
                for j in range(5):
                    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
                    if j % 2:
                        config.register_player(name=student_dir, algorithm=student_ai())
                        config.register_player(name=f'baseline{i}', algorithm=baseline_ai())
                    else:
                        config.register_player(name=f'baseline{i}', algorithm=baseline_ai())
                        config.register_player(name=student_dir, algorithm=student_ai())
                    game_result = start_poker(config, verbose=1, decks=decks[j])
                    print(f'{desc} - Game {j+1}: {game_result}')

                    # Determine game winner
                    if game_result['players'][0]['stack'] > game_result['players'][1]['stack']:
                        student_points += 1
                    else:
                        baseline_points += 1
                    
                    # Check if the student has won 3 games (he can get full points and thus we can break)
                    if student_points == 3:
                        break

                # Calculate total points earned
                if student_points >= 3:
                    student_total_points = 5
                else:
                    student_total_points = student_points * 1.5
                
                print(f'{desc} - Match Result: {student_dir} {student_points} games won, {student_total_points} points earned')

                # Save match result
                results[f'baseline{i}'] = {
                    'games_won': student_points,
                    'points_earned': student_total_points
                }

            # Play against each unseen strong AI  
            for i in range(1, 6):
                desc = f'{student_dir} vs strong{i}'
                strong_ai = globals()[f'strong{i}_ai']
                
                student_points = 0
                strong_points = 0

                # create deck for BO5
                decks = build_decks()
                # Play 5 games (BO5)
                for j in range(5):
                    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
                    if j % 2:
                        config.register_player(name=student_dir, algorithm=student_ai())
                        config.register_player(name=f'strong{i}', algorithm=strong_ai())
                    else:
                        config.register_player(name=f'strong{i}', algorithm=strong_ai())
                        config.register_player(name=student_dir, algorithm=student_ai())
                    game_result = start_poker(config, verbose=0, decks=decks[j])
                    print(f'{desc} - Game {j+1}: {game_result}')

                    # Determine game winner
                    if game_result['players'][0]['stack'] > game_result['players'][1]['stack']:
                        student_points += 1
                    else:
                        strong_points += 1
                    
                    # Check if a player has won 3 games (BO5)
                    if student_points == 3 or strong_points == 3:
                        break

                # Calculate total points earned
                if student_points >= 3:
                    student_total_points = 2
                else:
                    student_total_points = 0
                
                print(f'{desc} - Match Result: {student_dir} {student_points} games won, {student_total_points} points earned')

                # Save match result
                results[f'strong{i}'] = {
                    'games_won': student_points,
                    'points_earned': student_total_points
                }

            # Write all results for this student to CSV file
            for opponent, result in results.items():
                writer.writerow({
                    'student_dir': student_dir,
                    'opponent': opponent,
                    'games_won': result['games_won'],
                    'points_earned': result['points_earned']
                })
