\chapter{דו-כיווניות}

\section{קידוד מיקומי רוטציוני (\textenglish{RoPE})}

אחת הבעיות המרכזיות בארכיטקטורת ה-\textenglish{Transformer} \cite{vaswani_2017_transformer}
היא ייצוג המיקום היחסי של האסימונים ברצף. בגישות המקוריות נעשה שימוש בקידוד מיקומי מוחלט,
אשר מוסף לוקטור הייצוג של כל אסימון לפני כניסתו לשכבות הקשב. גישה זו, אף שפשוטה ליישום,
אינה מאפשרת לשכבות הקשב להסיק מיקום יחסי באופן ישיר מתוך מכפלת הוקטורים.

מנגנון ה-\textenglish{RoPE} (\textenglish{Rotary Position Embedding}) שהוצג על ידי
\cite{su_2021_rope} מציע פרדיגמה שונה: במקום להוסיף וקטור מיקום לייצוג, מוחל טרנספורמציה
רוטציונית על זוגות של ממדים בוקטורי ה-\textenglish{query} וה-\textenglish{key}.
הרוטציה מבוצעת לפי תדרים הנקבעים על-פי הנוסחה הבאה:

\begin{equation}
  \theta_i = 10000^{-2(i-1)/d}, \quad i = 1, 2, \ldots, \frac{d}{2}
\end{equation}

כאשר \(d\) הוא ממדיות הוקטור ו-\(i\) מציין את אינדקס הזוג. התכונה המרכזית של
\textenglish{RoPE} היא שמכפלת הוקטורים \(\langle q_m, k_n \rangle\) תלויה
אך ורק במרחק היחסי \(m - n\) בין שני האסימונים, ולא במיקומם המוחלט ברצף.
תכונה זו מעניקה למודל יכולת הכללה טבעית לרצפים ארוכים יותר מאלו שנצפו במהלך האימון.

בזכות יתרונות אלו, \textenglish{RoPE} אומץ כמנגנון הקידוד המיקומי הסטנדרטי
במשפחות מודלים מובילות, ובהן \textenglish{LLaMA} ו-\textenglish{Mistral}.
אימוץ נרחב זה מעיד על כך שהשיטה מספקת מענה מעשי לאחת מהמגבלות הבולטות
של ארכיטקטורת ה-\textenglish{Transformer} המקורית.

\section{\textenglish{FlashAttention}: קשב יעיל לזיכרון}

גם לאחר שיפור מנגנון הקידוד המיקומי, נותרת בעיה מבנית נוספת: חישוב הקשב
עצמו דורש שמירת מטריצת קשב בגודל \(N \times N\) בזיכרון ה-\textenglish{GPU},
כאשר \(N\) הוא אורך הרצף. עבור רצפים ארוכים, הדבר מציב דרישות זיכרון
חמורות המגבילות את גודל ה-\textenglish{batch} ואת אורך הרצף האפשרי בפועל.

\textenglish{FlashAttention} \cite{dao_2022_flashattention} הציגה גישה חדשה
המכונה קשב מודע-\textenglish{IO} (\textenglish{IO-Aware Attention}).
הרעיון המרכזי הוא לחלק את המטריצות \(Q\), \(K\), ו-\(V\) לבלוקים קטנים
(\textenglish{tiles}), ולבצע את חישוב הקשב ישירות בזיכרון המהיר \textenglish{SRAM}
של המעבד הגרפי, מבלי לכתוב את מטריצת הקשב המלאה לזיכרון האיטי יותר
(\textenglish{HBM} — \textenglish{High Bandwidth Memory}).

\begin{LTR}
Standard attention: \(\Omega(Nd + N^2)\) HBM accesses \\
FlashAttention:    \(O\!\left(\frac{N^2 d^2}{M}\right)\) HBM accesses
\end{LTR}

כאשר \(M\) הוא גודל ה-\textenglish{SRAM} הזמין. הקטנת מספר הגישות ל-\textenglish{HBM}
מאפשרת האצה של עד פי 7.6 בהשוואה לחישוב הקשב הסטנדרטי, כפי שנמדד על
מודל \textenglish{GPT-2}.
חשוב להדגיש כי \textenglish{FlashAttention} מחשבת תוצאה מדויקת מבחינה מתמטית
— אין כל קירוב בחישוב הקשב עצמו — ולכן ניתן לשלב אותה בכל ארכיטקטורה
המבוססת על קשב סטנדרטי ללא שינוי בהתנהגות המודל.

\section{מגבלות הקשב הריבועי ואתגרי הרצפים הארוכים}

למרות ההתקדמות שהביאו \textenglish{RoPE} ו-\textenglish{FlashAttention},
מגבלת הסיבוכיות הריבועית של מנגנון הקשב נותרת אתגר עיקרי.
בארכיטקטורת ה-\textenglish{Transformer} המקורית, סיבוכיות חישוב הקשב
היא \(O(N^2 \cdot d)\) בזמן ו-\(O(N^2)\) בזיכרון, כאשר \(N\) הוא אורך
הרצף ו-\(d\) ממדיות הראש. בעבור רצפים בני אלפי אסימונים — כגון
מסמכים ארוכים, קוד מקור מלא, או רצפי גנום — עלות זו הופכת לבלתי
ישימה מבחינה חישובית ותפעולית.

סקר ה-\textenglish{Efficient Transformers} של \cite{tay_2022_efficient_transformers}
מסווג את האסטרטגיות הקיימות להפחתת הסיבוכיות הריבועית למספר משפחות עיקריות:

\begin{itemize}
  \item \textbf{קשב דל (\textenglish{Sparse Attention})}: \textenglish{Longformer}
        מגביל כל אסימון לשקלל רק חלון מקומי של שכנים, תוך מתן קשב גלובלי
        לאסימוני ייחוס ייעודיים, ומשיג סיבוכיות \(O(N)\).
  \item \textbf{קשב בשיטת הכלה (\textenglish{Low-Rank Approximation})}: \textenglish{Linformer}
        מקרב את מטריצת הקשב על-ידי הקרנה למימד \(k \ll N\), ומשיג \(O(Nk)\).
  \item \textbf{קשב אקראי (\textenglish{Random Feature Attention})}: \textenglish{Performer}
        מחשב קירוב של פונקציית ה-\textenglish{softmax} באמצעות
        \textenglish{Random Features}, ומשיג \(O(Nd^2)\) ללא שמירת
        מטריצת הקשב כלל.
  \item \textbf{גיבוב רגיש-מקומי (\textenglish{LSH Attention})}: \textenglish{Reformer}
        מקבץ אסימונים דומים לדליים ומחשב קשב רק בתוך כל דלי,
        ומשיג \(O(N \log N)\).
\end{itemize}

על אף הגיוון בגישות, כל משפחה מציגה פשרות שונות בין יעילות חישובית
לאיכות הייצוג הנוצר. בפועל, לא כל שיטה שומרת על ביצועים שווים לאלו
של קשב מלא (\textenglish{full attention}) בכל משימה, ולכן הבחירה
בין השיטות תלויה במידה רבה בדרישות האפליקציה הספציפית.

סוגיה זו נותרת פתוחה כיום: ארכיטקטורת ה-\textenglish{Transformer} המקורית,
שהוצגה ב-\textenglish{Attention Is All You Need} \cite{vaswani_2017_transformer},
לא נועדה לרצפים ארוכים מאות אסימונים. ההרחבה לרצפים בני עשרות אלפי
אסימונים — כנדרש ביישומי ניתוח קוד, ביולוגיה חישובית, ועיבוד מסמכים ארוכים —
עדיין מחייבת פתרונות ארכיטקטורליים חדשניים שיוכלו לשמור הן על הדיוק
הן על היעילות החישובית גם יחד.
