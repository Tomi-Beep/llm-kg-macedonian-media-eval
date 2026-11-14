# Development runs

## 01 · First question with and without graph evidence

Question: „Наведи еден студиски албум на составот што ја компонирал музиката за „Пред дождот“.“

Script: `../run-benchmark.py`. Both calls used `qwen3:4b-instruct-2507-q4_K_M` with temperature 0 and a limit of 100 output tokens. The question and answer instructions were identical. The second call also received two Macedonian sentences from the graph.

~~~text
Музика од: Анастасија
Албуми: ['Nocturnal']

Докази:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.
„Анастасија“ го издаде албумот „Nocturnal“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден студиски албум на составот што ја компонирал музиката за „Пред дождот“ е „Nocturnal“.

Process finished with exit code 0
~~~

The model said it lacked information in the first call. With both facts supplied, it named Nocturnal, an acceptable answer listed in the discography. The first reply also used “одговорим” where standard Macedonian would use “одговорам”. This is a development example. It tests the effect of providing the facts on one question. The comparison with keyword retrieval is still pending.

[Film credits](https://manchevski.com/films/before-the-rain/) · [Анастасија discography](https://musicbrainz.org/artist/1682bbd8-41ec-45cf-8232-3ed5e94d8aa2)

## 02 · Comparison with film-title text search

Question: „Наведи еден студиски албум на составот што ја компонирал музиката за „Пред дождот“.“

Script: `../run-benchmark.py`. All three calls used `qwen3:4b-instruct-2507-q4_K_M`, temperature 0, and a 100-token output limit. The prompts had the same question and instructions. The first call received no evidence, the second received the two linked graph facts, and the third searched the same facts as text for the film title and received only the composer credit.

~~~text
Музика од: Анастасија
Албуми: ['Nocturnal']

Докази:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.
„Анастасија“ го издаде албумот „Nocturnal“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден студиски албум на составот што ја компонирал музиката за „Пред дождот“ е „Nocturnal“.

Докази од текстуалното пребарување:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.

Одговор со текстуално пребарување:
Немам доволно информации за да одговорим на прашањето.

Process finished with exit code 0
~~~

The film-title search found the composer credit. Its album sentence does not include the film title. Graph lookup used the composer from the first link to find the album in the second. Qwen answered correctly with the complete path and abstained in the other two calls. Both abstentions used “одговорим” where standard Macedonian uses “одговорам”. This is one development question and the text baseline here is a single title search.

## 03 · Dust and the composer-name error

Question: „Кој е еден албум на авторот на музиката за филмот „Прашина“?“

Script: `../run-benchmark.py`. The catalogue now includes four facts for two films. All three calls used `qwen3:4b-instruct-2507-q4_K_M`, temperature 0 and a 100-token output limit.

~~~text
Музика од: ['Кирил Џајковски']
Албуми: ['Homebound']

Докази:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.
„Кирил Џајковски“ го издаде албумот „Homebound“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден албум на авторот на музиката за филмот „Прашина“ е „Homebound“.

Докази од текстуалното пребарување:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.

Одговор со текстуално пребарување:
Еден албум на Кирил Џајковски, авторот на музиката за филмот „Прашина“, е „Кирил Џајковски“.
~~~

Without evidence, the model abstained and used “одговорим” in place of “одговорам”. Graph lookup supplied both links, and Qwen gave Homebound, a valid album. Film-title search found the composer credit only. Qwen then treated the composer's name as the album title, an answer unsupported by the retrieved sentence. This is a development example.

[Official film credits](https://manchevski.com/films/dust/) · [Кирил Џајковски discography](https://musicbrainz.org/artist/87d4efc5-c4a8-422b-9f8c-ea94c2eb4d0f)

## 04 · First batch with both album questions

Script: `../run-benchmark.py`. The same three conditions now run from a list of questions in one execution. The results below repeat the individual development examples from runs 02 and 03.

~~~text
Прашање: Наведи еден студиски албум на составот што ја компонирал музиката за „Пред дождот“.
Музика од: ['Анастасија']
Албуми: ['Nocturnal']

Докази:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.
„Анастасија“ го издаде албумот „Nocturnal“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден студиски албум на составот што ја компонирал музиката за „Пред дождот“ е „Nocturnal“.

Докази од текстуалното пребарување:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.

Одговор со текстуално пребарување:
Немам доволно информации за да одговорим на прашањето.

Прашање: Кој е еден албум на авторот на музиката за филмот „Прашина“?
Музика од: ['Кирил Џајковски']
Албуми: ['Homebound']

Докази:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.
„Кирил Џајковски“ го издаде албумот „Homebound“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден албум на авторот на музиката за филмот „Прашина“ е „Homebound“.

Докази од текстуалното пребарување:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.

Одговор со текстуално пребарување:
Еден албум на Кирил Џајковски, авторот на музиката за филмот „Прашина“, е „Кирил Џајковски“.

Process finished with exit code 0
~~~

The batch ran both questions in order. Graph lookup supplied the two needed facts each time. The one-pass title search supplied the composer credit. This confirms that the batch can rerun the development questions and reproduces the two earlier outcomes.

## 05 · One link, two links, and missing album evidence

Script: `../run-benchmark.py`. The batch contains a direct composer question, an album question supported by two links, and an album question for which the local catalogue contains only the film credit. Both retrieval conditions still use the same general answer instruction as the question-only condition.

~~~text
Прашање: Кој ја компонирал музиката за „Пред дождот“?
Музика од: ['Анастасија']
Албуми: []

Докази:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.

Одговор без граф:
Немам доволно информации.

Одговор со граф:
Музиката за филмот „Пред дождот“ ја компонираше Анастасија.

Докази од текстуалното пребарување:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.

Одговор со текстуално пребарување:
Музиката за филмот „Пред дождот“ ја компонираше Анастасија.

Прашање: Кој е еден албум на авторот на музиката за филмот „Прашина“?
Музика од: ['Кирил Џајковски']
Албуми: ['Homebound']

Докази:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.
„Кирил Џајковски“ го издаде албумот „Homebound“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден албум на авторот на музиката за филмот „Прашина“ е „Homebound“.

Докази од текстуалното пребарување:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.

Одговор со текстуално пребарување:
Еден албум на Кирил Џајковски, авторот на музиката за филмот „Прашина“, е „Кирил Џајковски“.

Прашање: Наведи еден албум на главниот композитор на музиката за „Сенки“.
Музика од: ['Рајан Шор']
Албуми: []

Докази:
Музиката за филмот „Сенки“ ја компонираше „Рајан Шор“.

Одговор без граф:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Главниот композитор на музиката за филмот „Сенки“ е Рајан Шор, и еден албум на Рајан Шор е „Муслим“.

Докази од текстуалното пребарување:
Музиката за филмот „Сенки“ ја компонираше „Рајан Шор“.

Одговор со текстуално пребарување:
Главниот композитор на музиката за филмот „Сенки“ е Рајан Шор, и еден албум на Рајан Шор е „Муслим“.

Process finished with exit code 0
~~~

Both retrieval methods answered the direct question using the same composer credit. The graph returned the two required links for the question about Прашина, while the text search returned the composer credit and Qwen repeated the composer as an album title. For Сенки, both methods supplied only the Ryan Shore credit, and both answers named an album absent from that evidence. The title “Муслим” is unsupported by the supplied record. The run does not establish its status outside the catalogue.

[Film credits for Сенки](https://manchevski.com/films/shadows/)

## 06 · Three questions with an evidence-only instruction

Script: `../run-benchmark.py`. Both retrieval prompts now tell the model to use only the supplied evidence and answer “Немам доволно информации.” if it is insufficient. The question-only prompt stayed the same. Its console label changed to “Одговор без дополнителен контекст”.

~~~text
Прашање: Кој ја компонирал музиката за „Пред дождот“?
Музика од: ['Анастасија']
Албуми: []

Докази:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.

Одговор без дополнителен контекст:
Немам доволно информации.

Одговор со граф:
Музиката за филмот „Пред дождот“ ја компонирале „Анастасија“.

Докази од текстуалното пребарување:
Музиката за филмот „Пред дождот“ ја компонираше „Анастасија“.

Одговор со текстуално пребарување:
Музиката за филмот „Пред дождот“ ја компонирале „Анастасија“.

Прашање: Кој е еден албум на авторот на музиката за филмот „Прашина“?
Музика од: ['Кирил Џајковски']
Албуми: ['Homebound']

Докази:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.
„Кирил Џајковски“ го издаде албумот „Homebound“.

Одговор без дополнителен контекст:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Еден албум на авторот на музиката за филмот „Прашина“ е „Homebound“.

Докази од текстуалното пребарување:
Музиката за филмот „Прашина“ ја компонираше „Кирил Џајковски“.

Одговор со текстуално пребарување:
Еден албум на Кирил Џајковски, авторот на музиката за филмот „Прашина“, не е даден во доказите.

Прашање: Наведи еден албум на главниот композитор на музиката за „Сенки“.
Музика од: ['Рајан Шор']
Албуми: []

Докази:
Музиката за филмот „Сенки“ ја компонираше „Рајан Шор“.

Одговор без дополнителен контекст:
Немам доволно информации за да одговорим на тоа прашање.

Одговор со граф:
Немам доволно информации.

Докази од текстуалното пребарување:
Музиката за филмот „Сенки“ ја компонираше „Рајан Шор“.

Одговор со текстуално пребарување:
Немам доволно информации.

Process finished with exit code 0
~~~

Both retrieval methods answered the direct question from the composer credit. Graph retrieval still answered the Прашина album question. The text condition expressed that the album was missing from its evidence, instead of repeating the composer as the title. Both conditions abstained for Сенки with the same partial evidence that had led to an unsupported album title in run 05. The question-only condition abstained on all three questions. These are development observations on the same cases used to revise the prompt.
