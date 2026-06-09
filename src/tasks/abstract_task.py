"""Dedicated task: prepend a Hebrew abstract to ch1 after bidi validation."""

from crewai import Agent, Task

_ABSTRACT_CONTENT = (
    "\\\\section*{תקציר}\\n\\n"
    "מחקר זה עוסק בהתפתחות מנגנוני תיאום כלים מרובים בסוכני"
    " \\\\textenglish{LLM}."
    " בעשור האחרון הפכו מודלי שפה למרכיב מרכזי במערכות בינה מלאכותית,"
    " ועלה הצורך לתאם ביניהם לבין כלים חיצוניים כגון מנועי חיפוש,"
    " מחשבונים ובסיסי נתונים."
    " המחקר בוחן שלוש גישות עיקריות: שיטות היוריסטיות מבוססות-דמיון;"
    " מסגרות למידה מפוקחת כגון \\\\textenglish{Toolformer}"
    " ו-\\\\textenglish{AvaTaR}; וארכיטקטורות רב-סוכניות."
    " בנוסף נבחן \\\\textenglish{Model Context Protocol} (\\\\textenglish{MCP})"
    " כתקן פתוח לממשק כלים."
    " הממצאים מצביעים כי מסגרות המשלבות לולאות חשיבה-פעולה"
    " (\\\\textenglish{ReAct}, \\\\textenglish{Reflexion})"
    " עם תכנון מודע-תלויות (\\\\textenglish{DEPS})"
    " משפרות משמעותית את יכולת ההרחבה, הביצועים והתחזוקה"
    " של מערכות סוכנים ייצורניות.\\n\\n"
)


def build_abstract_task(agent: Agent, bidi_task: Task) -> Task:
    return Task(
        description=(
            "BiDi validation is complete. ch1.tex is in its final state.\n"
            "Your ONLY job: prepend a Hebrew abstract section to ch1.tex.\n\n"
            "Call latex_writer_tool EXACTLY ONCE:\n"
            "  path='chapters/ch1.tex'\n"
            "  mode='prepend'\n"
            f"  content='{_ABSTRACT_CONTENT}'\n\n"
            "After the single tool call, emit:"
            " [CHECKPOINT] Abstract prepended to ch1.tex."
        ),
        expected_output=(
            "ch1.tex begins with \\\\section*{תקציר} followed by the chapter."
        ),
        agent=agent,
        context=[bidi_task],
    )
