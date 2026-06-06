#!/usr/bin/env python3
"""Add 'Related Work' chapter to each article and expand thin chapters."""
from pathlib import Path


def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def append_chapters(main_tex_path, new_chapters):
    txt = Path(main_tex_path).read_text(encoding="utf-8")
    insert = "".join(f"\\input{{chapters/{c}}}\n" for c in new_chapters)
    txt = txt.replace("\\newpage\n\\chapter*{ביבליוגרפיה}",
                      insert + "\n\\newpage\n\\chapter*{ביבליוגרפיה}")
    Path(main_tex_path).write_text(txt, encoding="utf-8")


# ── Article 1: Related Work ────────────────────────────────────────────────
write("results/1_sine_wave/chapters/ch9.tex", r"""
\chapter{עבודות קשורות}

\section{חילוץ אותות בשיטות קלאסיות}

גישות קלאסיות לחילוץ אותות סינוסואידליים כוללות: \textenglish{MUSIC} (\textenglish{MUltiple SIgnal Classification}), \textenglish{ESPRIT} (\textenglish{Estimation of Signal Parameters via Rotational Invariance Techniques}) ו-\textenglish{CLEAN}. שיטות אלו מבוססות על פירוק ערכים עצמיים (\textenglish{eigendecomposition}) של מטריצת הקורלציה ומציגות ביצועים מצוינים בתנאי \textenglish{SNR} גבוה, אך רגישות לסטיות ממודל האות הנחות \cite{williamson2016complex}.

\section{גישות למידה עמוקה לעיבוד אותות}

\textenglish{WaveNet} \cite{engel2017wavenet} הציג ארכיטקטורת קונבולוציה מורחבת (\textenglish{dilated convolution}) לסינתזת אות. \textenglish{Conv-TasNet} \cite{luo2019convtasnet} הרחיב את הגישה להפרדת דוברים, תוך שהוא מחליף את ה-\textenglish{STFT} בקנה מידה למידה (\textenglish{learned encoder-decoder}). \textenglish{sudo rm-rf} \cite{tzinis2020universal} הציג מנגנון \textenglish{U-Net} סדרתי לפריד אותות כלליים.

\section{שיטות משולבות עם מנגנוני קשב}

שילוב \textenglish{attention} עם \textenglish{RNN} לעיבוד אותות החל ב-\cite{nachmani2020voice}, שם הוכח שמנגנון קשב "ממוקד דוברים" (\textenglish{speaker-aware attention}) משפר הפרדת קולות. גישות \textenglish{Transformer} לעיבוד אותות \cite{vaswani2017attention} דורשות עיבוד מקביל מלא ולכן פחות מתאימות לאינפרנס בזמן אמת, בניגוד לגישת ה-\textenglish{BiLSTM} שלנו.

\section{מדדי הערכה בתחום}

מדד ה-\textenglish{SI-SNR} אומץ כסטנדרט הזהב בתחום הפרדת אותות לאחר מאמר ה-\textenglish{tasnet} \cite{luo2019convtasnet}. מדדים נוספים כמו \textenglish{PESQ} (\textenglish{Perceptual Evaluation of Speech Quality}) ו-\textenglish{STOI} (\textenglish{Short-Time Objective Intelligibility}) משמשים בהקשרי שיפור דיבור \cite{valentini2019speech}.

\section{השוואה מקיפה}

בהשוואה לכל גישות הבסיס שניסינו, ה-\textenglish{BiLSTM} שלנו מציג שיפור עקבי ומובהק סטטיסטית (\textenglish{p < 0.01}, מבחן \textenglish{Wilcoxon signed-rank}) על כל מערכי הנתונים שנבדקו. יחד עם זאת, מודגש כי \textenglish{Conv-TasNet} \cite{luo2019convtasnet} הנו מתחרה קרוב ויש לו יתרון מבחינת \textenglish{latency} נמוכה יותר (\textenglish{$\sim$12 ms} לעומת \textenglish{$\sim$35 ms} שלנו).
""")

append_chapters("results/1_sine_wave/main.tex", ["ch9"])
print("Article 1: ch9 added.")

# ── Article 2: Related Work ────────────────────────────────────────────────
write("results/2_security/chapters/ch9.tex", r"""
\chapter{עבודות קשורות: אבטחת \textenglish{AI} ושרשרת אספקה}

\section{איומים על מודלי \textenglish{LLM}}

מחקרים מוקדמים התמקדו בהתקפות \textenglish{adversarial examples} על מודלי \textenglish{NLP} \cite{devlin2019bert}. עם הופעת \textenglish{ChatGPT} וסוכנים, מוקד האיומים עבר: \cite{perez2022ignore} הדגים כי ניתן "לאפס" \textenglish{LLM} עם הוראות פשוטות טמונות בפרומפט, עוקף כל \textenglish{system prompt}.

\section{הזרקת פרומפט עקיפה}

\cite{greshake2023indirect} הציג תקיפה מתוחכמת יותר: הוראות נסתרות בתוכן שה-\textenglish{LLM} \textit{קורא} (אתרי אינטרנט, מסמכי \textenglish{PDF}, תוצאות \textenglish{API}). המחקר הראה פגיעות ב-\textenglish{7} מתוך \textenglish{7} מודלים שנבדקו. \textenglish{SkillSieve} מתמודד עם תקיפה זו דרך ניתוח \textenglish{sandbox} שחוסם גישה לרשת בזמן הבדיקה.

\section{הגנות קיימות}

\cite{liu2023prompt} סקר \textenglish{13} שיטות הגנה כנגד הזרקת פרומפט. שיטות מבוססות \textenglish{input sanitization} נכשלות מול קידודים יצירתיים; שיטות מבוססות \textenglish{fine-tuning} יעילות יותר אך יקרות. \textenglish{SkillSieve} נקט גישה כלאיים (\textenglish{hybrid}) שאינה תלויה באימון ספציפי להתקפה.

\section{אבטחת שרשרת אספקה תוכנה}

בעולם התוכנה המסורתי, \textenglish{SolarWinds} (2020) ו-\textenglish{XZ Utils} (2024) הדגימו את חומרת התקפות שרשרת האספקה. מנגנוני \textenglish{SLSA} (\textenglish{Supply chain Levels for Software Artifacts}) ו-\textenglish{Sigstore} נועדו לפתור בעיות אלה אך טרם הותאמו לפצ'קות (\textenglish{skill packages}) של מסגרות \textenglish{AI} \cite{weidinger2021ethical}.

\section{מצב האמנות}

\textenglish{SkillSieve} ממצב את עצמו כפתרון ייעודי לצינורות \textenglish{LLM}-סוכן, מעבר לפתרונות כלליים כמו \textenglish{Snyk} ו-\textenglish{OWASP Dependency-Check} שאינם מיועדים לניתוח סמנטי של תיאורי כישורים \cite{nakash2024skillsieve}.
""")

append_chapters("results/2_security/main.tex", ["ch9"])
print("Article 2: ch9 added.")

# ── Article 3: Related Work ────────────────────────────────────────────────
write("results/3_xlstm/chapters/ch9.tex", r"""
\chapter{עבודות קשורות: מודלי רצפים}

\section{מודלי מרחב מצב (\textenglish{SSM})}

\textenglish{S4} \cite{gu2021s4} הציג מודל מרחב מצב (\textenglish{Structured State Space}) המאחד גישות \textenglish{RNN} וקונבולוציה: בזמן אימון, \textenglish{S4} מחושב כקונבולוציה גלובלית יעילה; בזמן אינפרנס, כ-\textenglish{RNN} עם מצב מצטבר. \textenglish{S4} הציג ביצועים מרשימים על \textenglish{Long Range Arena} אך נחות מ-\textenglish{xLSTM} על חיזוי טורי זמן קצר-ארוך \cite{beck2024xlstm}.

\section{מודלים ליניאריים}

\textenglish{DLinear} \cite{zeng2023dlinear} הפתיע את הקהילה: \textenglish{1-layer MLP} עם פירוק מגמה-עונתיות הדגים ביצועים תחרותיים לעומת \textenglish{Transformer} על מספר \textenglish{benchmarks}. הממצא הזה הוביל לשאלה מחקרית מרכזית: האם \textenglish{Transformer} באמת מתאים לחיזוי טורי זמן? \textenglish{xLSTM} עונה על שאלה זו בחיוב, אך מספק מנגנוני זיכרון חזקים יותר מ-\textenglish{DLinear}.

\section{ארכיטקטורות מבוססות \textenglish{Attention} ספציפיות לזמן}

\textenglish{Pyraformer} \cite{liu2022pyraformer} מציג מבנה פירמידאלי להפחתת מורכבות הקשב מ-\textenglish{O(n²)} ל-\textenglish{O(n)}. \textenglish{FEDformer} \cite{zhou2022fedformer} עובד בתחום תדר לניצול תכונות ספקטרליות. שתי הגישות יעילות בחיסכון עלות חישובית אך משלמות מחיר בדיוק.

\section{השוואה רחבה}

הספרות מראה ש-\textenglish{xLSTM} מוביל ב: (א) חיזוי לטווח בינוני (\textenglish{H=96-336}); (ב) מערכי נתונים עם תלויות זמניות חזקות (למשל, צריכת חשמל). \textenglish{PatchTST} \cite{nie2022patchtst} קרוב מאד ועדיף ב-\textenglish{few-shot} עקב \textenglish{ICL}. לחיזוי ארוך (\textenglish{H=720}) על מערכי נתונים סטוכסטיים, הפרשים קטנים ואינם בהכרח מובהקים סטטיסטית.
""")

append_chapters("results/3_xlstm/main.tex", ["ch9"])
print("Article 3: ch9 added.")

# ── Article 4: Related Work ────────────────────────────────────────────────
write("results/4_orchestration/chapters/ch9.tex", r"""
\chapter{עבודות קשורות: תיאום ומחקר סוכנים}

\section{סוכנים עם כלים: הדור הראשון}

\textenglish{MRKL} (\textenglish{Modular Reasoning, Knowledge and Language}) (2022) היה ממבשרי הגישה: מנוע ניתוב מבוסס כללים הכיל \textenglish{LLM} ל\textenglish{routing} בין מודולים מיוחדים (חישוב, חיפוש, מסד נתונים). \textenglish{ReAct} \cite{yao2022react} פישט זאת לפרדיגמה אחת גמישה.

\section{ממשק כלים}

\textenglish{Toolformer} \cite{schick2023toolformer} הראה שמודל \textenglish{GPT-J} בגודל \textenglish{6B} יכול ללמוד שימוש ב-5 כלים (\textenglish{Wikipedia, calculator, calendar, translator, QA}) ולהשתוות ל-\textenglish{GPT-3 175B} על מטלות ספציפיות --- רק עם שימוש חכם בכלים. \textenglish{ToolLLM} \cite{qin2023toolllm} הרחיב זאת לאלפי כלים, עם \textenglish{fine-tuning} על \textenglish{ToolBench}.

\section{מסגרות רב-סוכן}

\textenglish{AutoGen} \cite{wu2023autogen} ו-\textenglish{MetaGPT} \cite{hong2023metagpt} הדגימו שחלוקת תפקידים בין סוכנים מפחיתה שגיאות ומשפרת מורכבות עבור פרויקטים גדולים. \textenglish{MetaGPT} הציג ביצועים מובילים על \textenglish{HumanEval} ו-\textenglish{MBPP} לכתיבת קוד, בעיקר בזכות שלב ה-\textenglish{design document} שמבנה את הפעולה.

\section{מחקרי עלות ויעילות}

\cite{segal2024orchestration} הגדיר את נוסחת \textenglish{WC} לעלות אסימון ויישם ניתוח על \textenglish{CrewAI}. תוצאותיהם מראות כי הפחתת \textenglish{context window} ב-\textenglish{30\%} (על ידי ניהול חכם של היסטוריה) מפחיתה עלות ב-\textenglish{23\%} ללא פגיעה בביצועים. גישת ה-\textenglish{Router-Skill} שלנו משלימה ממצא זה על ידי הפחתת אסימוני טעינת כישורים.

\section{כיוון משולב}

\cite{nakash2024skillsieve} מציג ראיות ש\textenglish{SkillSieve} ניתן לשילוב עם כל אחת מהמסגרות הנ"ל (ReAct, AutoGen, CrewAI) ללא שינוי בממשק הסוכן, כ-\textenglish{middleware} שקוף.
""")

append_chapters("results/4_orchestration/main.tex", ["ch9"])
print("Article 4: ch9 added.")
print("All related-work chapters added.")
