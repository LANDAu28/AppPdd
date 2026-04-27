# Currency-Converter-
Пирожков Даниил Олегович
## Как запустить
1. Установите библиотеки: `pip install requests customtkinter`
2. Получите API-ключ на [exchangerate-api.com](https://exchangerate-api.com)
3. Вставьте ключ в переменную `self.api_key`
4. Запустите: `python main.py`

## Тестирование
- Ввод букв или отрицательных чисел выдаст предупреждение.
- После каждой конвертации данные мгновенно появляются в таблице и сохраняются в `history.json`.
