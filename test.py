import os
import csv
import sys
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

def load_student_ai(student_id: str, src_path: str):
    """Load the student's AI setup function."""
    sys.path.insert(0, src_path)
    try:
        student_module = __import__('agent', fromlist=['setup_ai'])
        return student_module.setup_ai
    except ImportError:
        print(f'Error importing setup_ai for {student_id}')
        sys.exit(1)
    finally:
        sys.path.pop(0)

def read_existing_results() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Read existing results from the CSV file."""
    existing_results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                student_dir, opponent, games_won, points_earned = row
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
    decks = build_decks()

    for j in range(num_games):
        config = setup_config(max_round=MAX_ROUNDS, initial_stack=INITIAL_STACK, small_blind_amount=SMALL_BLIND_AMOUNT)
        if j % 2:
            config.register_player(name=student_id, algorithm=student_ai())
            config.register_player(name=opponent_name, algorithm=opponent_ai())
        else:
            config.register_player(name=opponent_name, algorithm=opponent_ai())
            config.register_player(name=student_id, algorithm=student_ai())
        
        game_result = start_poker(config, verbose=0, decks=decks[j])
        print(f'{student_id} vs {opponent_name} - Game {j+1}: {game_result}')

        if game_result['players'][0]['stack'] > game_result['players'][1]['stack']:
            student_points += 1
        else:
            opponent_points += 1
        
        if student_points == 3 or opponent_points == 3:
            break

    return {'games_won': student_points, 'opponent_games_won': opponent_points}

def calculate_points(games_won: int, is_baseline: bool) -> float:
    """Calculate points based on games won and opponent type."""
    if games_won >= 3:
        return 5 if is_baseline else 2
    return games_won * 1.5 if is_baseline else 0

def main(student_id: str):
    student_src_info = read_student_src_info()
    src_path = student_src_info.get(student_id)

    if not src_path or not os.path.exists(src_path):
        print(f'Skipping {student_id} (src directory not found)')
        sys.exit(1)

    student_ai = load_student_ai(student_id, src_path)
    existing_results = read_existing_results()

    if student_id in existing_results:
        print(f'Skipping {student_id} (already tested)')
        sys.exit(0)

    results = {}

    # Play against each baseline AI
    for i in range(1, 8):
        baseline_ai = globals()[f'baseline{i}_ai']
        game_results = play_games(student_id, student_ai, f'baseline{i}', baseline_ai)
        points_earned = calculate_points(game_results['games_won'], is_baseline=True)
        results[f'baseline{i}'] = {
            'games_won': game_results['games_won'],
            'points_earned': points_earned
        }
        print(f'{student_id} vs baseline{i} - Match Result: {game_results["games_won"]} games won, {points_earned} points earned')

    # Play against each unseen strong AI
    for i in range(1, 6):
        strong_ai = globals()[f'strong{i}_ai']
        game_results = play_games(student_id, student_ai, f'strong{i}', strong_ai)
        points_earned = calculate_points(game_results['games_won'], is_baseline=False)
        results[f'strong{i}'] = {
            'games_won': game_results['games_won'],
            'points_earned': points_earned
        }
        print(f'{student_id} vs strong{i} - Match Result: {game_results["games_won"]} games won, {points_earned} points earned')

    # Write results to CSV file
    with open(RESULTS_FILE, 'a', newline='') as f:
        fieldnames = ['student_dir', 'opponent', 'games_won', 'points_earned']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        for opponent, result in results.items():
            writer.writerow({
                'student_dir': student_id,
                'opponent': opponent,
                'games_won': result['games_won'],
                'points_earned': result['points_earned']
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run poker AI tests for a student.")
    parser.add_argument("student_id", help="The student ID to test")
    args = parser.parse_args()
    main(args.student_id)
