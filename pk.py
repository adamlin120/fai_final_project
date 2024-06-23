import os
import csv
import sys
import argparse
from typing import Dict, Any

from deck_utils import build_decks
from game.game import setup_config, start_poker

RESULTS_FILE = 'pk_results.csv'
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

def play_games(student1_id: str, student1_ai, student2_id: str, student2_ai, num_games: int = 5) -> Dict[str, Any]:
    """Play a series of games between two student AIs."""
    student1_points = 0
    student2_points = 0
    decks = build_decks()

    for j in range(num_games):
        config = setup_config(max_round=MAX_ROUNDS, initial_stack=INITIAL_STACK, small_blind_amount=SMALL_BLIND_AMOUNT)
        if j % 2:
            config.register_player(name=student1_id, algorithm=student1_ai())
            config.register_player(name=student2_id, algorithm=student2_ai())
        else:
            config.register_player(name=student2_id, algorithm=student2_ai())
            config.register_player(name=student1_id, algorithm=student1_ai())
        
        game_result = start_poker(config, verbose=0, decks=decks[j])
        print(f'{student1_id} vs {student2_id} - Game {j+1}: {game_result}')

        if game_result['players'][0]['stack'] > game_result['players'][1]['stack']:
            student1_points += 1
        else:
            student2_points += 1
        
        if student1_points == 3 or student2_points == 3:
            break

    return {'student1_wins': student1_points, 'student2_wins': student2_points}

def main(student1_id: str, student2_id: str):
    student_src_info = read_student_src_info()
    
    for student_id in [student1_id, student2_id]:
        src_path = student_src_info.get(student_id)
        if not src_path or not os.path.exists(src_path):
            print(f'Skipping {student_id} (src directory not found)')
            sys.exit(1)

    student1_ai = load_student_ai(student1_id)
    student2_ai = load_student_ai(student2_id)

    game_results = play_games(student1_id, student1_ai, student2_id, student2_ai)
    
    print(f'Final Result: {student1_id} won {game_results["student1_wins"]} games, {student2_id} won {game_results["student2_wins"]} games')

    # Write results to CSV file
    with open(RESULTS_FILE, 'a', newline='') as f:
        fieldnames = ['student1_id', 'student2_id', 'student1_wins', 'student2_wins']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'student1_id': student1_id,
            'student2_id': student2_id,
            'student1_wins': game_results['student1_wins'],
            'student2_wins': game_results['student2_wins']
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run poker AI tests for two students.")
    parser.add_argument("student1_id", help="The first student ID to test")
    parser.add_argument("student2_id", help="The second student ID to test")
    args = parser.parse_args()
    main(args.student1_id, args.student2_id)
