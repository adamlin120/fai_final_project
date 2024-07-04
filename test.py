import os
import csv
import sys
import math
import random
import argparse
from typing import Dict, Any

from deck_utils import build_decks
from game.game import setup_config, start_poker

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

RESULTS_FILE = 'results.csv'
MAX_ROUNDS = 20
INITIAL_STACK = 1000
SMALL_BLIND_AMOUNT = 5

def read_student_src_info() -> Dict[str, str]:
    """Read student_src_info.csv and return a dictionary of student IDs and their source directories."""
    src_info = {}
    with open('student_src_info.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src_info[row['學號']] = row['src目錄']
    return src_info

def load_student_ai(student_id: str):
    """Load the student's AI setup function."""
    try:
        sys.path.insert(0, './')
        student_module = __import__(f'{student_id}.agent', fromlist=['setup_ai'])
        return student_module.setup_ai
    except ImportError:
        try:
            sys.path.insert(0, f'./{student_id}')
            student_module = __import__('agent', fromlist=['setup_ai'])
            return student_module.setup_ai
        except ImportError as e:
            print(f'Error importing setup_ai for {student_id}: {e}')
            sys.exit(1)
    finally:
        sys.path.pop(0)
        if len(sys.path) > 0 and sys.path[0].endswith(student_id):
            sys.path.pop(0)

def read_existing_results() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Read existing results from the CSV file."""
    existing_results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                student_dir, opponent, games_won, _, _, _, points_earned = row
                if student_dir == "student_dir":
                    continue
                if student_dir not in existing_results:
                    existing_results[student_dir] = {}
                existing_results[student_dir][opponent] = {
                    'games_won': int(games_won),
                    'points_earned': float(points_earned)
                }
    return existing_results

def play_games(student_id: str, student_ai, opponent_name: str, opponent_ai, num_games: int = 5) -> Dict[str, Any]:
    """Play a series of games between the student AI and an opponent AI."""
    student_points = 0
    opponent_points = 0
    tie_count = 0
    student_stacks, opponent_stacks = 0, 0

    decks = build_decks()
    # random select which player goes first
    student_first = (random.uniform(0, 1) <= 0.5)
    if student_first:
        players = [
            {"name": student_id, "algorithm": student_ai()},
            {"name": opponent_name, "algorithm": opponent_ai()}
        ]
    else:
        players = [
            {"name": opponent_name, "algorithm": opponent_ai()},
            {"name": student_id, "algorithm": student_ai()}
        ]

    for j in range(num_games):
        config = setup_config(max_round=MAX_ROUNDS, initial_stack=INITIAL_STACK, small_blind_amount=SMALL_BLIND_AMOUNT)
        config.register_player(**players[0])
        config.register_player(**players[1])
        
        game_result = start_poker(config, verbose=1, decks=decks[j])
        print(f'{student_id} vs {opponent_name} - Game {j+1}: {game_result}')

        student_stack = game_result['players'][0]['stack'] if players[0]['name'] == student_id else game_result['players'][1]['stack']
        opponent_stack = game_result['players'][0]['stack'] if players[0]['name'] == opponent_name else game_result['players'][1]['stack']

        student_stacks += student_stack
        opponent_stacks += opponent_stack

        if math.isclose(student_stack, opponent_stack):
            tie_count += 1
        elif student_stack > opponent_stack:
            student_points += 1
        else:
            opponent_points += 1
        
        if student_points == 3:
            break
        
        # swap the order
        players[0], players[1] = players[1], players[0]

    return {
        'games_won': student_points, 
        'opponent_games_won': opponent_points, 
        'num_ties': tie_count,
        'student_stacks': student_stacks,
        'opponent_stacks': opponent_stacks
    }

def calculate_points(game_results: dict, is_baseline: bool) -> float:
    """Calculate points based on games won and opponent type."""
    student_games_won = game_results['games_won']
    student_stacks = game_results['student_stacks']
    opponent_games_won = game_results['opponent_games_won']
    opponent_stacks = game_results['opponent_stacks']

    if student_games_won >= 3:
        return 5 if is_baseline else 2
    elif student_games_won == opponent_games_won:
        if student_stacks > opponent_stacks:
            return 5 if is_baseline else 2
        else:
            return student_games_won * 1.5 if is_baseline else 0
    else:
        return student_games_won * 1.5 if is_baseline else 0

def main(student_id: str):
    student_src_info = read_student_src_info()
    src_path = student_src_info.get(student_id)

    if not src_path or not os.path.exists(src_path):
        print(f'Skipping {student_id} (src directory not found)')
        sys.exit(1)

    student_ai = load_student_ai(student_id)
    existing_results = read_existing_results()

    if student_id in existing_results:
        print(f'Skipping {student_id} (already tested)')
        sys.exit(0)

    results = {}

    # Play against each baseline AI
    for i in range(1, 8):
        baseline_ai = globals()[f'baseline{i}_ai']
        game_results = play_games(student_id, student_ai, f'baseline{i}', baseline_ai)
        points_earned = calculate_points(game_results, is_baseline=True)
        results[f'baseline{i}'] = {
            'games_won': game_results['games_won'],
            'num_ties': game_results['num_ties'],
            'student_stacks': game_results['student_stacks'],
            'opponent_stacks': game_results['opponent_stacks'],
            'points_earned': points_earned
        }
        print(f'{student_id} vs baseline{i} - Match Result: {game_results["games_won"]} games won, {game_results["num_ties"]} ties, student gets {game_results["student_stacks"]} stacks, opponent gets {game_results["opponent_stacks"]} stacks, {points_earned} points earned')

    # Play against each unseen strong AI
    for i in range(1, 6):
        strong_ai = globals()[f'strong{i}_ai']
        game_results = play_games(student_id, student_ai, f'strong{i}', strong_ai)
        points_earned = calculate_points(game_results, is_baseline=False)
        results[f'strong{i}'] = {
            'games_won': game_results['games_won'],
            'num_ties': game_results['num_ties'],
            'student_stacks': game_results['student_stacks'],
            'opponent_stacks': game_results['opponent_stacks'],
            'points_earned': points_earned
        }
        print(f'{student_id} vs strong{i} - Match Result: {game_results["games_won"]} games won, {game_results["num_ties"]} ties, student gets {game_results["student_stacks"]} stacks, opponent gets {game_results["opponent_stacks"]} stacks, {points_earned} points earned')

    # Write results to CSV file
    with open(RESULTS_FILE, 'a', newline='') as f:
        fieldnames = ['student_dir', 'opponent', 'games_won', 'num_ties', 'student_stacks', 'opponent_stacks', 'points_earned']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        for opponent, result in results.items():
            writer.writerow({
                'student_dir': student_id,
                'opponent': opponent,
                'games_won': result['games_won'],
                'num_ties': result['num_ties'],
                'student_stacks': result['student_stacks'],
                'opponent_stacks': result['opponent_stacks'],
                'points_earned': result['points_earned']
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run poker AI tests for a student.")
    parser.add_argument("student_id", help="The student ID to test")
    args = parser.parse_args()
    main(args.student_id)
