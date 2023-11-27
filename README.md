# NLSQL

## Переводчик с естественного языка на SQL - «Цифровой прорыв» — 1 место

### Краткое описание кейса
Современные технологии позволяют легко решать задачи перевода естественных человеческих языков. Доступно большое количество технологий и уже обученных нейросетей для решения подобных задач, но стабильно работающего переводчика с человеческой речи на язык программирования - нет. 

Решения в datadriven-компаниях принимаются на основании проверки гипотез на данных. При этом большая часть таких гипотез не является сложными — такие проверки могут осуществлять сами участники команд со стороны бизнеса (selfservice), но они не всегда обладают знаниями языков программирования.

Участникам хакатона предлагается реализовать переводчик с «человеческого» языка на язык SQL. 

Разработанное участниками решение позволит сократить время при принятии решений, ускорит бизнес-процессы в компании ПАО «Ростелеком», а также позволит командам быстрее обучаться работе с данными и сократит нагрузку на дата-аналитиков. 

### Решение команды DeviAⁱnts.
Модель машинного обучения для перевода естественного языка на SQL. Может обрабатывать как простые, так и сложные запросы.
Решение упростит работу людям, которые не умеют составлять запросы SQL. Интерфейс решения представлен в виде веб-приложения, а также в виде чат-бота.

### Стек решения:
Стек решения: Python, Transformers, T5, PyTorch, Django, telebot.

### Уникальность:
Высокая точность, возможность обрабатывать несколько таблиц, высокая скорость работы модели Text-To-Text, простой и интуитивный интерфейс.

### Поддерживаемые операторы SQL

- [X] SELECT
    - [X] one column
    - [X] multiple columns
    - [X] all columns
    - [X] distinct select
    - [X] aggregate functions
        - [X] count-select
        - [X] sum-select
        - [X] avg-select
        - [X] min-select
        - [X] max-select
- [ ] JOIN
- [X] WHERE
    - [X] one condition
    - [X] multiple conditions
    - [X] operators
        - [X] equal/not equal operator
        - [X] greater-than/less-than operator
        - [ ] like operator
        - [ ] between operator
    - [X] aggregate functions
        - [X] sum in condition
        - [X] avg in condition
        - [X] min in condition
        - [X] max in condition
- [X] ORDER BY
    - [X] ASC
    - [X] DESC
- [X] GROUP BY
- [ ] detection of values

### Файлы:
- `Making Spider Dataset.ipynb` - Преобразование датасета Spider для обучения T5
- `Training T5-Base on Spider.ipynb` - Обучение T5-Base
- `Making Translated Spider Dataset.ipynb` - Перевод датасета Spider для обучения моделей на русском
- `nlpQL/` - Сайт на Django
- `NQLbot/` - Telegram бот на Telebot
