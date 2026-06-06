\chapter{מבוא לארכיטקטורת Transformer}

\section{מהו Transformer?}

\textenglish{Transformer} היא ארכיטקטורה של רשת עצבית עמוקה שפותחה לעיבוד של רצפים (sequences). בניגוד למודלים הקודמים בתחום עיבוד שפה טבעית (NLP), \textenglish{Transformer} מבוססת על מנגנון \textenglish{attention} בלבד, ללא שימוש בתאי זיכרון מחוזר (\textenglish{recurrent units}). מנגנון זה מאפשר לדגם קשרים בין כל זוג אלמנטים ברצף בו זמנית, מה שהופך את המודל ליעיל וגמיש יותר.

\textenglish{Transformer} משנת 2017 הפכה למודל בסיסי במודרני של בינה מלאכותית, המשמש כבסיס למודלים גדולים של שפה (\textenglish{LLMs}) כמו \textenglish{BERT}, \textenglish{GPT}, ו-\textenglish{T5}. משמעות ההצלחה של ארכיטקטורה זו טמונה בכושרה לתפוס קשרים תלויים ארוכי טווח ברצפים, תוך שמירה על יעילות חישובית גבוהה.

\section{רקע היסטורי ופיתוח}

התפתחות \textenglish{Transformer} נשנעה מהצורך להתגבר על מגבלות הארכיטקטורות הקודמות. בשנים הראשונות של מהפכת הלמידה העמוקה, מודלים מסוג \textenglish{RNN} ו-\textenglish{LSTM} היו התקן בתחום עיבוד הרצפים. עם זאת, לאלה היו בעיות משמעותיות: תלות סדרתית שמנעה הקבלה מלאה, ובעיות כמו הידלדלות או התפוצצות גרדיאנט.

המנגנון של \textenglish{attention} הוצג כדי לתמוך במודלים של \textenglish{sequence-to-sequence}, במיוחד לתרגום מכונה. עם זאת, בשנת 2017, המאמר "Attention is All You Need" הציג את \textenglish{Transformer}, שהחליף כליל את הרכיבים הרקורנטיים בשכבות \textenglish{attention} מקביליות. זו הייתה אבן דרך בתחום, כיוון שהדגימה כי \textenglish{attention} בלבד יכול לשרת למודליות של רצפים מורכבים ללא רקוריות.

\section{מרכיבים עיקריים}

ארכיטקטורת \textenglish{Transformer} מורכבת מכמה מרכיבים חיוניים:

\begin{equation}
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\end{equation}

מנגנון \textenglish{attention} זה מאפשר לכל עמדה ברצף להשתקלל על כל עמדות אחרות. שכבות \textenglish{multi-head attention} מאפשרות למודל ללמוד חיזוי ליניארי מרובי באותו זמן, כל אחד מתמקדת בתלות שונה.

רשת \textenglish{feed-forward} כוללת שתי שכבות לינאריות עם פונקציית הפעלה (בדרך כלל ReLU) ביניהן. קידוד מיקום (\textenglish{positional encoding}) מוסיף מידע על סדר האלמנטים ברצף, מכיוון ש-\textenglish{attention} כשלעצמה אינה תלויה בסדר.

\section{יישומים ודוגמאות}

היום, \textenglish{Transformer} משמשת כבסיס למערכות בעלות משמעות כלכלית וחברתית ניכרת. תרגום מכונה נהיה דומה יותר לאנושי. יוצרי טקסט כמו \textenglish{GPT} מודגמים את הפוטנציאל של מודלים בעלי פרמטרים ענקיים. בנוסף, \textenglish{Transformer} הוצגה בתחומים אחרים: ראייה ממוחשבת (vision transformers), זיהוי דיבור, וניתוח ביוטכנולוגי.

ההתאמות והשיפורים על ארכיטקטורת ה-\textenglish{Transformer} המקורית נמשכות, עם פוקוס על יעילות, קנה מידה, והבנה טובה יותר של כוחה התיאורטי.
