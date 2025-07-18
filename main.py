from exceptions import (
    UserNotFound,
    NotAuthenticated,
)


def decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper


class ExceptionHandler:
    def __init__(self, exceptions, handler):
        self.exceptions = tuple(exceptions)
        self.handler = handler
        self.counter = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                self.counter += 1
                if self.counter > 500:
                    # send_admin_email("СРОЧНО ПРОВЕРЬ ЧТО ПРОИСХОДИТ!!")
                    self.counter = 0
                    print("Счётчик сброшен")
                print(f"[ExceptionHandler] Поймано исключение: {e}\nВсего исключений было: {self.counter}")
                return self.handler(e, *args, **kwargs)

        return wrapper


# Общий обработчик ошибок
def handle_auth_error(exc, *args, **kwargs):
    print(f"⚠ [handle_auth_error] Обработка исключения: {type(exc).__name__}")
    return {"error": str(exc)}


@ExceptionHandler(exceptions=[UserNotFound, NotAuthenticated], handler=handle_auth_error)
def get_user_data(user_id):  # страшная и бессмысленная функция, но наглядно
    if user_id == 1:
        return {"id": 1, "name": "Alice"}
    elif user_id == 2:
        raise NotAuthenticated("Пользователь не авторизован")
    else:
        raise UserNotFound("Пользователь не найден")


# Примеры вызова
print(get_user_data(1))  # {'id': 1, 'name': 'Alice'}
print(get_user_data(2))  # ⚠ Обработка исключения: NotAuthenticated
# {'error': 'Пользователь не авторизован'}
print(get_user_data(3))  # ⚠ Обработка исключения: UserNotFound
# {'error': 'Пользователь не найден'}
