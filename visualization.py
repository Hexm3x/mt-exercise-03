import matplotlib.pyplot as plt
import re
from prettytable import PrettyTable

# files, file opener
log_path_baseline_file = "configs/baseline.log"
log_path_prenorm_file = "models/deen_transformer_pren/validations.txt"
log_path_postnorm_file = "models/deen_transformer_postn/validations.txt"

with open(log_path_baseline_file, "r") as f:
    log_path_baseline = f.read()
with open(log_path_prenorm_file, "r") as f:
    log_path_prenorm = f.read()
with open(log_path_postnorm_file, "r") as f:
    log_path_postnorm = f.read()

# initialize lists
steps_list = []
ppl_list_baseline = []
ppl_list_prenorm = []
ppl_list_postnorm = []

# extracting steps and ppl
# Got tip from Chatgpt to use grouping ()
logfile_pattern = r"Steps?:\s*(\d+).*?ppl:\s*(\d+\.\d+)"
logs = [log_path_prenorm, log_path_postnorm, log_path_baseline]
for log in logs:
    # prenorm - taking step data + ppl
    if log == log_path_prenorm:
        # Asked ChatGPT - Dotall allows newlines as well
        matching_prenorm = re.findall(logfile_pattern, log, re.DOTALL)
        for step, ppl in matching_prenorm:
            steps_list.append(step)
            ppl_list_prenorm.append(ppl)
    # only taking ppl
    if log == log_path_postnorm:
        matching_postnorm = re.findall(logfile_pattern, log, re.DOTALL)
        for step, ppl in matching_postnorm:
            ppl_list_postnorm.append(ppl)
    # only taking ppl
    if log == log_path_baseline:
        matching_baseline = re.findall(logfile_pattern, log, re.DOTALL)
        for step, ppl in matching_baseline:
            ppl_list_baseline.append(ppl)

# Initialize PrettyTable - a small introduction can be found here: https://www.geeksforgeeks.org/creating-tables-with-prettytable-library-python/
columns = [steps_list, ppl_list_baseline, ppl_list_prenorm, ppl_list_postnorm]
column_names = ["Steps", "Baseline", "Prenorm", "Postnorm"]

validation_ppl_table = PrettyTable()

# good idea of ChatGPT to use zip to reduce lines of codes and errors
for name, column in zip(column_names, columns):
    validation_ppl_table.add_column(name, column)

# save the data - discussion is found here: https://stackoverflow.com/questions/22431252/how-do-i-save-table-from-prettytable
validation_ppl_prettytable = str(validation_ppl_table)
with open('table_validation_perplexities.txt', 'w') as f:
    f.write(validation_ppl_prettytable)

# line chart
# ChatGPT's suggestion after getting faulty line chart (they were stacked on each other as the ppls were considered as strings)
ppl_list_baseline = [float(p) for p in ppl_list_baseline]
ppl_list_prenorm = [float(p) for p in ppl_list_prenorm]
ppl_list_postnorm = [float(p) for p in ppl_list_postnorm]

plt.figure(figsize=(20, 15))
plt.plot(steps_list, ppl_list_baseline, label="Baseline", color="Aqua")
plt.plot(steps_list, ppl_list_prenorm, label="Prenorm",
         linestyle="--", color="Gold")
plt.plot(steps_list, ppl_list_postnorm,
         label="Postnorm", linestyle=":", color="DeepPink")

plt.xlabel("Steps")
plt.ylabel("Validation Perplexity")
plt.title("Validation Perplexity per Step")
plt.xticks(rotation=90)
plt.legend(fontsize=20)
plt.tight_layout()
plt.savefig("linechart_validation_perplexities.png", dpi=300)
