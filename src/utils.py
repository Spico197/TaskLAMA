import matplotlib.pyplot as plt
import networkx as nx


class Step:
    def __init__(self, sid: int, content: str) -> None:
        self.sid = sid
        self.content = content
        self.children = []
        self.parents = []

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parents.append(parent)

    def __str__(self) -> str:
        return f"{self.sid} - {self.content} - {len(self.children)} children - {len(self.parents)} parents"

    def __repr__(self) -> str:
        return f"<{self.sid} - {self.content}>"


class Task:
    def __init__(self, task, assumption) -> None:
        self.task = task
        self.assumption = assumption
        self.steps = []
        self._str2step = {}
        self.root = Step(-1, "root")

    def add_steps(self, steps: list[dict]):
        for step in steps:
            step_obj = Step(step["stepId"], step["step"])
            self.steps.append(step_obj)
            self._str2step[step["step"]] = step_obj

    def build_dag(self, rels: list[dict]):
        self.steps.sort(key=lambda x: x.sid)
        for rel in rels:
            before = rel["subtask1"]
            after = rel["subtask2"]
            if before != after:
                self._str2step[before].add_child(self._str2step[after])
                self._str2step[after].add_parent(self._str2step[before])
        for step in self.steps:
            if not step.parents:
                step.add_parent(self.root)
                self.root.add_child(step)

    def get_dag_root(self):
        return self.root

    def get_dag_width(self):
        root = self.get_dag_root()
        queue = [root]
        visited = set()
        width = 0
        while queue:
            width = max(width, len(queue))
            for _ in range(len(queue)):
                cur = queue.pop(0)
                for child in cur.children:
                    if child not in queue and child not in visited:
                        queue.append(child)
                        visited.add(child)
        return width

    def get_dag_depth(self):
        root = self.get_dag_root()
        queue = [(root, 0)]
        visited = set()
        depth = 0
        while queue:
            cur, cur_depth = queue.pop(0)
            depth = max(depth, cur_depth)
            for child in cur.children:
                if (child, cur_depth + 1) not in queue and child not in visited:
                    queue.append((child, cur_depth + 1))
                    visited.add(child)
        return depth - 1

    def visualize(self):
        G = nx.DiGraph(name=f"{self.task} - {self.assumption}")
        for step in self.steps:
            G.add_node(step.content)
        for step in self.steps:
            for child in step.children:
                G.add_edge(step.content, child.content)
        nx.draw(G, with_labels=True)
        plt.show()

    def __str__(self) -> str:
        return f"{self.task} - {self.assumption} - {len(self.steps)} steps"
