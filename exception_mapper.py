from exceptions import (
    UserNotFound,
    NotAuthenticated,
)


class ExceptionMapper:
    def __init__(self, handlers: dict):
        # Ожидаем словарь: {ExceptionType: handler_function}
        self.handlers = handlers

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                for exc_type, handler in self.handlers.items():  # items = (key, value)
                    # exceptions = {
                    #     UserNotFound: handle_user_not_found,
                    #     NotAuthenticated: handle_auth_error,
                    # }
                    if isinstance(e, exc_type):
                        print(f"[ExceptionMapper] Обработка {exc_type.__name__} через {handler.__name__}")
                        return handler(e, *args, **kwargs)
                # Если не нашли подходящий обработчик — пробрасываем дальше
                raise

        return wrapper


# Обработчики
def handle_user_not_found(exc, *args, **kwargs):
    print("❌ Пользователь не найден.")
    return {"error": str(exc), "code": 404}


def handle_auth_error(exc, *args, **kwargs):
    print("🔐 Пользователь не авторизован.")
    return {"error": str(exc), "code": 401}


def handle_no_money_error(exc, *args, **kwargs):
    ...


# raise NoMoneyError

# Основная функция
@ExceptionMapper({
    UserNotFound: handle_user_not_found,
    NotAuthenticated: handle_auth_error,
    # NoMoneyError: handle_no_money_error,  # {"message": "недостаточно средств"} status_code 400
})
def get_user(user_id):
    if user_id == 1:
        return {"id": 1, "name": "Alice"}
    elif user_id == 2:
        raise NotAuthenticated("Токен невалиден")
    else:
        raise UserNotFound("Нет такого пользователя")


def get_user_without_decorator(user_id):
    try:
        if user_id == 1:
            return {"id": 1, "name": "Alice"}
        elif user_id == 2:
            raise NotAuthenticated("Токен невалиден")
        else:
            raise UserNotFound("Нет такого пользователя")
    # Если вдруг появится новое исключение, его придётся добавлять вручную
    except NotAuthenticated as e:
        print("🔐 Пользователь не авторизован.")
        return {"error": str(e), "code": 401}

    except UserNotFound as e:
        print("❌ Пользователь не найден.")
        return {"error": str(e), "code": 404}

    # except NoMoneyError as e:
    #     print({"message": "недостаточно средств"})
    #     return {"message": "недостаточно средств"}


print(get_user(1))  # ✅ OK
print(get_user(2))  # 🔐 NotAuthenticated - невалидный токен
print(get_user(3))  # ❌ UserNotFound
