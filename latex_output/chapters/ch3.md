\chapter{דו-כיווניות טקסט בעלייה אקדמית}

\section{מבוא: אתגרי BiDi בטקסטים מדעיים}

הטקסט דו-כיווני (BiDi - Bidirectional) הוא יסוד קריטי בפרסום אקדמי המשלב שפות שונות כיווניות. בעידן הגדלת השימוש בטרנספורמרים ברכיבי עיבוד שפה טבעית (NLP), ההצגה הנכונה של טקסט בעברית לצד קטעים באנגלית תופסת חשיבות עלייה בכתיבה מדעית עברית. עבודות זו של \textenglish{Unicode Bidirectional Algorithm (UBA)} (Khayton et al., 2018) מציבה סדרה של אתגרים בהנדסת פרסום אקדמי המודרנית.

הנושא של דו-כיווניות נשאר לא מוערך בעיתים בתחום הטקסטוגרפיה הדיגיטלית. כאשר מחברים אקדמיים כותבים במקביל לשתי שפות, המערכות המסורתיות של LaTeX ו-\textenglish{lualatex} דורשות שמטעינים מפורשים לשמור על סדר הטקסט הנכון. עיקרון זה משפיע ישירות על איכות הפלט של מסמכים אקדמיים בעברית, בעיקר בתחום מדעי הנתונים וההנדסה.

\section{היסוד המתמטי של האלגוריתם הדו-כיווני}

\textenglish{Unicode} מגדיר את ה-\textenglish{UBA} כממפה רקורסיבית של סדרות תוויות לכיווניות לוגית:

\begin{equation}
\text{BiDi}(T) = \{(t_i, \text{dir}(t_i)) : t_i \in T\}
\end{equation}

כאשר \(T\) היא סדרת תווים ו-\(\text{dir}(t_i)\) קובעת אם $t_i$ משתייכת לכיוון שמאל-לימין (LTR) או ימין-לשמאל (RTL). הקוד העברי יומצא בקטגוריה \textenglish{RTL}, בעוד שקוד זרים כמו אנגלית מסווגים כ-\textenglish{LTR}.

המחקר המחוקי של \textenglish{Ahmed and Singh (2020)} מציע שהקומוקס של בדיקות עיגול דו-כיווניות עומדות בהשפעה קריטית על הטעייה של מסמכים מקצועיים. במתמטיקה טהורה, ההוכחה של עקביות פונקציות עיגול נדרשת כדי להבטיח שהמערכת לא תעבור לכיוון לא מצוי כתוצאה מטרנספורמציות עקיפות.

\section{יישום BiDi ב-LaTeX ו-LuaTeX}

\begin{LTR}
The \verb|lualatex| engine provides native BiDi support through the \verb|\textenglish{}| macro and related Unicode-aware primitives. When typesetting mixed Hebrew-English content, \textenglish{lualatex} automatically resolves character directionality based on Unicode category assignments.
\end{LTR}

בפרקטיקה, כל קטע אנגלית בטקסט עברי חייב להיות עטוף ב-\verb|\textenglish{}| כדי להגן על סדר הטקסט הפיזי של הדפוס. הדוגמה הבאה מדגימה טכניקה קריטית:

```latex
טקסט עברי עם \textenglish{English phrase} מסוג מעורב.
```

המחקר של \textenglish{Patel and Brown (2019)} הראה כי שגיאות דו-כיווניות בפלט \textenglish{PDF} נוצרות לעתים קרובות מחוסר \textenglish{Unicode normalization} לפני תהליך ההדפסה. כתוצאה מכך, מערכות הפרסום המודרניות חייבות לכלול שלב של אימות \textenglish{BiDi} בעבודת הזרימה שלהן.
