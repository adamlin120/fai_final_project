# 🃏 Final Project 改作業 🃏
## 📋 Prerequisites

1. Create a new conda environment:
   ```
   mkdir -p ~/miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   rm -rf ~/miniconda3/miniconda.sh
   ~/miniconda3/bin/conda init bash
   conda create -n poker python=3.8.13 -y
   ```

2. Activate the conda environment:
   ```
   conda activate poker
   ```

3. Install the required packages:
   ```
   pip install -r requirement.txt
   pip install "stable-baselines3[extra]"
   pip install pandas tqdm
   ```

## 🗃️ Zip Student Files

Run the following command to process and zip student files:

```
python parse_student_info.py
python find_src_directories.py
python create_student_symlink.py
```

## 🚀 Run All Students Baseline

To run tests for all students in parallel, use the provided `run_all_students.sh` script. This script reads student directories from `student_src_info.csv` and runs tests for each student in parallel.

Run the following command to execute the script:

```
./run_all_students.sh
```


## 🏆 Run Round-Robin Tournament

To run a round-robin tournament where each student's AI plays against every other student's AI, use the following command:

```
python make_group.py
```