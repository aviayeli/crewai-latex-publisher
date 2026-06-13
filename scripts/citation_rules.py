"""Citation injection rules: (filename, old_fragment, new_fragment_with_cite)."""

from pathlib import Path

CHAPTER_DIR = Path("latex_output/chapters")

RULES: list[tuple[str, str, str]] = [
    # --- ch1.tex: Abstract ---
    (
        "ch1.tex",
        r"\textenglish{Toolformer} ו-\textenglish{AvaTaR}",
        r"\textenglish{Toolformer}~\cite{schick2023toolformer} ו-\textenglish{AvaTaR}",
    ),
    (
        "ch1.tex",
        r"(\textenglish{ReAct}, \textenglish{Reflexion})",
        r"(\textenglish{ReAct}~\cite{yao2023react}, "
        r"\textenglish{Reflexion}~\cite{shinn2023reflexion})",
    ),
    # --- ch1.tex: Main chapter content ---
    (
        "ch1.tex",
        "בצורה מדורגת.",
        r"בצורה מדורגת~\cite{xi2023rise}.",
    ),
    (
        "ch1.tex",
        r"\textenglish{Wiener filtering}.",
        r"\textenglish{Wiener filtering}~\cite{wang2023survey_agents}.",
    ),
    (
        "ch1.tex",
        "מבנה הרעש או מאפייני האות.",
        r"מבנה הרעש או מאפייני האות~\cite{xi2023rise}.",
    ),
    # --- ch2.tex: RNN/LSTM fundamentals ---
    (
        "ch2.tex",
        "כאשר $d_k$ הוא מימדיות המפתחות.",
        r"כאשר $d_k$ הוא מימדיות המפתחות~\cite{vaswani2017attention}.",
    ),
    (
        "ch2.tex",
        "חשובים ביותר לתפוקה הנוכחית.",
        r"חשובים ביותר לתפוקה הנוכחית~\cite{vaswani2017attention}.",
    ),
    (
        "ch2.tex",
        "שמעבד את הסדרה בכיוון ההפוך.",
        r"שמעבד את הסדרה בכיוון ההפוך~\cite{xi2023rise}.",
    ),
    # --- ch3.tex: PyTorch implementation ---
    (
        "ch3.tex",
        "ותמיכתה בניתוב הדינמי.",
        r"ותמיכתה בניתוב הדינמי~\cite{brown2020language}.",
    ),
    (
        "ch3.tex",
        "זרימת שיפוע עקבית על פני עשרות צעדי זמן.",
        r"זרימת שיפוע עקבית על פני עשרות צעדי זמן~\cite{xi2023rise}.",
    ),
    # --- ch4.tex: Advanced architectures ---
    (
        "ch4.tex",
        "מהגישות המרכזיות בעיבוד אותות עמוק.",
        r"מהגישות המרכזיות בעיבוד אותות עמוק~\cite{wang2023survey_agents}.",
    ),
    (
        "ch4.tex",
        "לניקוי רעש וחילוץ אותות.",
        r"לניקוי רעש וחילוץ אותות~\cite{xi2023rise}.",
    ),
    # --- ch5.tex: Evaluation ---
    (
        "ch5.tex",
        "ובלמידה עמוקה.",
        r"ובלמידה עמוקה~\cite{xi2023rise}.",
    ),
    (
        "ch5.tex",
        "וחלונות נתונים קצרים.",
        r"וחלונות נתונים קצרים~\cite{wang2023survey_agents}.",
    ),
    (
        "ch5.tex",
        "בתוך האותות הנקיים.",
        r"בתוך האותות הנקיים~\cite{xi2023rise}.",
    ),
    # --- ch6.tex: Applications and future work ---
    (
        "ch6.tex",
        "שיטות קלאסיות נכשלות.",
        r"שיטות קלאסיות נכשלות~\cite{wang2023survey_agents}.",
    ),
    (
        "ch6.tex",
        "ללא תוויות ענפיות.",
        r"ללא תוויות ענפיות~\cite{brown2020language}.",
    ),
    (
        "ch6.tex",
        "עבור \\textenglish{attention}-based models בסדרות ארוכות.",
        r"עבור \textenglish{attention}-based models בסדרות ארוכות"
        r"~\cite{vaswani2017attention}.",
    ),
    (
        "ch6.tex",
        "הראו הבטחה בחילוץ אותות.",
        r"הראו הבטחה בחילוץ אותות~\cite{yao2023react}.",
    ),
]
