[POST] http://localhost:8000/api/v1/ -
(def create)

принимаем у пользователя 
login (CharField), 
email (EmailField), 
password (CharField) 

если данные валидны - создаем пользователя (status=201)


[POST] http://localhost:8000/api/v1/ -
(def set_password)

принимаем у пользователя
email (EmailField)
password (CharField)
pin (CharField)

если пользователь ввел не все поля выдаем ответ 'Не хватает полей' (status=401)

если пользователь не ввел пин-код выдаем ответ 'Вы авторизированы' (status=500)

если пользователь ввел неверный пин-код выдаем ответ 'Неверный пин код' (status=500)

если все данные валидны обнуляем пин-код (pin=None)
(если у пользователя пин = None - он авторизирован)

сохраняем пользавателя (status=201)



[GET] http://localhost:8000/api/v1/7 -
(def retrieve)

принимаем у пользователя id(7), 

выводим пользователя с таким id,
если такого пользователя нет - выдаем ошибку


[GET] http://localhost:8000/api/v1 -
(class TransactionsModelSet)

выводим все транзакции (переводы)
sender - отправитель
receiver - получатель
status - статус транзакции (
        PROCESSING = 'Обрабатывается'
        OK = 'Успешно'
        BAD = 'Неверно'
        LATE = 'Ожидание превышено'
        REJECTED = 'Отклонено'
)
amount - сумма транзакции
