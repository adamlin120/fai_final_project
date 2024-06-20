import os
import json
import random
import numpy as np
from tqdm import tqdm, trange

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

import csv

SEEDS = (0, 0, 1, 1, 2)

# Get list of student submission directories
submissions_dir = 'submissions'
student_dirs = [d for d in os.listdir(submissions_dir) if os.path.isdir(os.path.join(submissions_dir, d))]

# Load existing results from CSV file if it exists
results_file = 'results.csv'
existing_results = {}
if os.path.exists(results_file):
    with open(results_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_dir = row['student_dir']
            if student_dir not in existing_results:
                existing_results[student_dir] = {}
            existing_results[student_dir][row['opponent']] = {
                'games_won': int(row['games_won']),
                'points_earned': float(row['points_earned'])
            }

with open(results_file, 'a', newline='') as f:
    fieldnames = ['student_dir', 'opponent', 'games_won', 'points_earned']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if f.tell() == 0:  # Write header if file is empty
        writer.writeheader()

    for student_dir in tqdm(student_dirs, desc='Testing student submissions'):
        if student_dir in existing_results:
            print(f'Skipping {student_dir} (already tested)')
            continue

        # Load student's setup_ai function
        student_module = __import__(f'submissions.{student_dir}.src.agent', fromlist=['setup_ai'])
        student_ai = student_module.setup_ai
        
        results = {}

        # Play against each baseline AI
        for i in range(8):
            desc = f'{student_dir} vs baseline{i}'
            baseline_ai = globals()[f'baseline{i}_ai']
            
            student_points = 0
            baseline_points = 0

            # Play 5 games (BO5)
            for j, seed in zip(range(5), SEEDS):
                random.seed(seed)
                np.random.seed(seed)
                config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
                if j % 2:
                    config.register_player(name=student_dir, algorithm=student_ai())
                    config.register_player(name=f'baseline{i}', algorithm=baseline_ai())
                else:
                    config.register_player(name=f'baseline{i}', algorithm=baseline_ai())
                    config.register_player(name=student_dir, algorithm=student_ai())
                game_result = start_poker(config, verbose=0)
                print(f'{desc} - Game {j+1}: {game_result}')

                # Determine game winner
                if game_result['players'][0]['stack'] > game_result['players'][1]['stack']:
                    student_points += 1
                else:
                    baseline_points += 1
                
                # Check if a player has won 3 games (BO5)
                if student_points == 3 or baseline_points == 3:
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

            # Play 5 games (BO5)
            for j, seed in zip(range(5), SEEDS):
                random.seed(seed)
                np.random.seed(seed)
                config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
                if j % 2:
                    config.register_player(name=student_dir, algorithm=student_ai())
                    config.register_player(name=f'strong{i}', algorithm=strong_ai())
                else:
                    config.register_player(name=f'strong{i}', algorithm=strong_ai())
                    config.register_player(name=student_dir, algorithm=student_ai())
                game_result = start_poker(config, verbose=0)
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
