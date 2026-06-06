\chapter{ארכיטקטורה של רובוטריקים}

\section{מבוא לארכיטקטורת טרנספורמר}

טרנספורמר הוא מודל עמוק המבוסס על מנגנון ה-Attention בלבד, ללא שימוש בשכבות Recurrent או Convolutional \cite{vaswani2017attention}. המודל הזה השתנה באופן דרמטי את תחום עיבוד השפה הטבעית (NLP) ולאחרונה הוביל לפריצות במודלים למולטימודלים ובראייה ממוחשבת. 

הארכיטקטורה הבסיסית של טרנספורמר מורכבת משתי רכיבים עיקריים: (1) \textenglish{encoder} המקודד את הקלט, ו-(2) \textenglish{decoder} אשר מייצר את הפלט. כל אחד מהם מורכב מ-$N$ שכבות זהות, כאשר בכל שכבה יש שתי תת-שכבות: שכבת \textenglish{multi-head self-attention} ושכבת \textenglish{fully connected} (חיבור מלא).

\section{מנגנון ה-Attention}

המנגנון המרכזי של טרנספורמר הוא \textenglish{Scaled Dot-Product Attention} (SDP). בהינתן שלוש מטריצות — \textenglish{Query} ($Q$), \textenglish{Key} ($K$), ו-\textenglish{Value} ($V$) — פלט ה-Attention מחושב כ:

\begin{equation}
\textenglish{Attention}(Q, K, V) = \textenglish{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\end{equation}

כאן, $d_k$ היא הממד של וקטורי ה-Key, והחלוקה ב-$\sqrt{d_k}$ משמשת לייצוב מספרי של המנגנון. פעולת ה-softmax משמשת כדי לייצר משקלות Attention שמסתכמות לאחד על פני כל מיקום בסדרה.

\textenglish{Multi-Head Attention} מרחיבה את הרעיון הזה על ידי הפעלה של מנגנון ה-Attention המקורי $h$ פעמים במקביל, כאשר כל \textenglish{head} כולל טרנספורמציות ליניאריות שונות של $Q$, $K$, ו-$V$:

\begin{equation}
\textenglish{MultiHead}(Q, K, V) = \textenglish{Concat}(\textenglish{head}_1, \ldots, \textenglish{head}_h)W^O
\end{equation}

כאשר $\textenglish{head}_i = \textenglish{Attention}(QW_i^Q, KW_i^K, VW_i^V)$ ו-$W^O$ היא מטריצת טרנספורמציה פלט משותפת.

\section{שכבות להנדסה (Feedforward Networks)}

כל שכבת encoder וגם decoder כוללת שכבת \textenglish{feed-forward network} (FFN) אחרי שכבת ה-Attention. זו היא רשת עם שתי שכבות ליניאריות עם פונקציית הפעלה ReLU ביניהן:

\begin{equation}
\textenglish{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
\end{equation}

הממד הפנימי של FFN (בדרך כלל $d_{ff} = 2048$ עבור מימד מודל $d_{model} = 512$) גדול בהרבה מממד המודל, מה שמאפשר למודל ללמוד הצגות מורכבות יותר. שכבה זו מיושמת בצורה זהה בכל מיקום בסדרה, אך משתנים שלה משותפים על פני כל הסדרה \cite{vaswani2017attention}.

\section{Positional Encoding}

מכיוון שטרנספורמר עושה שימוש רק ב-Attention ולא ברכיבים \textenglish{recurrent}, הוא איננו מקודד אינהרנטית את סדר הסדרה. כדי להתמודד עם בעיה זו, מוסיפים \textenglish{Positional Encoding} (PE) לטבעות ההטבעה של הקלט:

\begin{equation}
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right) \quad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
\end{equation}

כאן, $pos$ הוא המיקום בסדרה ו-$i$ הוא ממד ההטבעה. כל מימד של ה-PE שונה בתדר שונה, מה שמאפשר למודל ללמוד בעיתוד על קשרים יחסיים בין מיקומים בסדרה \cite{vaswani2017attention}.

\section{יתרונות וביצועים}

ארכיטקטורת טרנספורמר מציעה מספר יתרונות כלל משמעותיים בהשוואה למודלים קודמים:

\begin{LTR}
\textbf{Parallelizability:} בניגוד למודלים RNN שעוסקים ברצף, טרנספורמר יכול לעבד את כל המיקומים בסדרה בו-זמנית. זה מאפשר הנדסה יעילה יותר על יחידות GPU\slash TPU.

\textbf{Temporal Dependencies:} Attention מאפשר מודלים ללמוד תלות ארוכת-טווח ישירה בעלות חישובית נמוכה יותר מאשר RNNs. המנגנון הסקלרי של ה-Attention מובטח בעלות זיכרון $\mathcal{O}(n^2)$ כאשר $n$ הוא אורך הסדרה.

\textbf{הניצול של מטריצות גדולות:} Attention מהווה פעולות מטריצה תומיד שניתן להאיץ באופן משמעותי תוך שימוש בכרטיסי GPU עם יחידות CUDA רבות.
\end{LTR}

עם זאת, מודלים כמו BERT ו-GPT קיימים בהן פשרות בין גודל מודל כלל-כיווני לעומת מודל חד-כיווני (left-to-right). מחקרים שונים מתארים שיטות שונות לאזן בין דיוק ויעילות (Devlin et al., 2018; Radford et al., 2019).