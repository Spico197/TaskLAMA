from collections import Counter

import matplotlib.pyplot as plt
from rex.utils.io import load_jsonlines
from tqdm import tqdm

from src.utils import Task

if __name__ == "__main__":
    data = load_jsonlines("resources/test.jsonl")

    tree_num = 0
    step_num = []
    for ins in data:
        step_num.append(len(ins["substeps"]))
        steps2id = {step["step"]: step["stepId"] for step in ins["substeps"]}
        for rel in ins["dependencies"]:
            before = rel["subtask1"]
            after = rel["subtask2"]
            if steps2id[before] > steps2id[after]:
                tree_num += 1
                break

    print(len(data))
    print("tree_num: ", tree_num)
    print("step_num: ", Counter(step_num).most_common())

    plt.hist(step_num)
    plt.title("Number of steps per task")
    plt.show()

    no_assumption = 0
    widths = []
    depths = []
    root_num = []
    for ins in tqdm(data):
        if not ins["assumptions"]:
            no_assumption += 1
            assumption = None
        else:
            assumption = ins["assumptions"][0]["assumption"]
        task = Task(ins["task"], assumption)
        task.add_steps(ins["substeps"])
        task.build_dag(ins["dependencies"])
        widths.append(task.get_dag_width())
        depths.append(task.get_dag_depth())
        root_num.append(len(task.root.children))
        if len(task.steps) == 15:
            print(task)
            task.visualize()

    print("no_assumption: ", no_assumption)
    root_num = Counter(root_num).most_common()
    print("root_num: ", root_num)
    width_num = Counter(widths).most_common()
    print("widths: ", width_num)
    depth_num = Counter(depths).most_common()
    print("depths: ", depth_num)

    root_num.sort(key=lambda x: x[0])
    plt.bar([x[0] for x in root_num], [x[1] for x in root_num])
    plt.title("DAG Roots")
    plt.show()

    width_num.sort(key=lambda x: x[0])
    plt.bar([x[0] for x in width_num], [x[1] for x in width_num])
    plt.title("DAG width")
    plt.show()

    plt.hist(depths)
    plt.title("DAG depths")
    plt.show()
