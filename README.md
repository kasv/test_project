# Система перевода денежных средств (демо)

## Общие сведения
Простая система перевода денежных средств между пользователями. Используемый стек: Django/DRF, Postgresql, Docker/compose.
Система поддерживает следующие валюты: EUR, USD, GPB, RUB.
Обновление курса валют происходит автоматически с некоторой периодичностью от брокера [exchangeratesapi.io](https://exchangeratesapi.io/)

## API методы
- [POST] `/api/v1/register` - регистрация нового пользователя
- [POST] `/api/v1/pay` - перевод средств со счета текущего пользователя другому
- [GET] `/api/v1/history` - история операций текущего пользователя

### Регистрация нового пользователя (`register`), передаваемые параметры:
- **username** _STR_: Уникльное имя пользователя (___required___)
- **password** _STR_: Надежный пароль (___required___)
- **email** _STR_: Адрес эл. почты (___required___)
- **balance** _FLOAT_: Текущий баланс (___required___)
- **currency** _STR_: Код валюты (___required___)

При успешном выполнении ответом будет:
```json
{"success": true}
```

### перевод средств со счета текущего пользователя другому (`pay`), передаваемые параметры:
- **payee** _STR_: Имя получателя (___required___)
- **transfer_sum** _FLOAT_: Сумма перевода в валюте отправителя (___required___)

При успешном выполнении ответом будет:
```json
{"success": true}
```

### Просмотр истории своих операций по счету (`history`), передаваемые параметры отсутствуют.
При успешном выполнении ответом будет (пример):
```json
{
    "success": true,
    "result": {
        "incoming_payments": [],
        "outgoing_payments": [
            {
                "datetime": "2020-01-22 10:53:58",
                "user_from": "user1",
                "transfer_sum": "1.00",
                "status": "1"
            },
            {
                "datetime": "2020-01-22 10:44:27",
                "user_from": "user1",
                "transfer_sum": "11.00",
                "status": "1"
            }
        ]
    }
}
```

## Запуск проекта
$ `docker-compose up -d --build`
$ `docker-compose run web python /opt/project/manage.py migrate --noinput`
$ `docker-compose run web python /opt/project/manage.py loaddata currency users`
