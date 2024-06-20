# 🃏 Final Project 改作業 🃏
## 📋 Prerequisites

1. Create a new conda environment:
   ```
   conda create -n poker python=3.8.13 -y
   ```

2. Activate the conda environment:
   ```
   conda activate poker
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   pip install pandas tqdm
   ```

## 🗃️ Zip Student Files

Run the following command to process and zip student files:

```
python parse_student_info.py
python find_src_directories.py
```

## 🚀 Run All Students Baseline

To run tests for all students in parallel, use the provided `run_all_students.sh` script. This script reads student directories from `student_src_info.csv` and runs tests for each student in parallel.

Run the following command to execute the script:

```
./run_all_students.sh
```

