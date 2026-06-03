"""Factory for the scientific figure generation task."""

from crewai import Agent, Task


def build_figure_task(agent: Agent, outline_task: Task) -> Task:
    return Task(
        description=(
            "Write and execute a Python script via python_runner_tool that saves"
            " latex_output/assets/attention_complexity.png at 300 dpi."
            " The plot must show three curves: O(n²) standard attention,"
            " O(n log n) linear attention, and O(n) recurrent."
            " x-axis: 'Sequence Length (n)', y-axis: 'Complexity', with legend."
            " Also write a TikZ scaled dot-product attention block to"
            " latex_output/figures/sdp_attention.tex via latex_writer_tool,"
            " with Q, K, V node labels."
        ),
        expected_output=(
            "attention_complexity.png and sdp_attention.tex"
            " both exist in their output directories."
        ),
        agent=agent,
        context=[outline_task],
    )
