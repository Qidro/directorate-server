### Гайдлайн по разработке
При начале разработки нового функционала, нужно создать новую ветку
<br>`git checkout -b branch_name`<br>
> Имя ветки должно соответствовать следующему виду `номер_задачи-кратное_название`, например `8-authorization`

<br>После окончания разработки, необходимо отправить изменения в свою ветку
<br>`git push origin my_branch`<br>

<br>Далее нужно переключится в `dev` ветку и получить изменения, если они были
<br>`git checkout dev`
<br>`git pull origin dev`<br>

<br>После этого, нужно слить изменения в ветке dev с нашей веткой и залить изменения в свою ветку
<br>`git checkout my_branch`
<br>`git rebase dev`
<br>`git push -f origin my_branch`<br>

<br>Далее, заходим на github, переходим в раздел Pull requests и создаем запрос на слияние.


### Кодстайл
На сервере придерживаемся следующей концепции именования:
- Переменные и функции - snake_case
- Классы - CamelCase
- Константы - UPPER_CASE

Кто не будет придерживаться этих правил будет изнасилован шампуром.