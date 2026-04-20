import re
import os
import time

def clean_gcode(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        line = line.split(";")[0]

        line = re.sub(r'\(.*\)', '', line)

        line = line.strip()

        if line:
            clean_lines.append(line)

    with open(output_file, 'w') as f:
        f.write('\n'.join(clean_lines))

if not os.path.exists("data_cleaned"):
    os.makedirs("data_cleaned")

for i in range(0, 1418):
    clean_gcode(f'data_raw/gcode_{i}.gcode', f'data_cleaned/cleaned_gcode_{i}.gcode')
    print(f"File nr {i} cleaned")
    time.sleep(0.1)
