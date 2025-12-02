from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "/login": {
            "POST": "Авторизация пользователя"
        },
        "/logout": {
            "POST": "Выход из авторизации"
        },
        "/protected": {
            "GET": "Проверка токена на доступ к ресурсу"
        },
        "/api/users": {
            "GET": "Информация о всех пользователях",
            "POST": "Создание нового пользователя"
        },
        "/api/users/me": {
            "GET": "Данные пользователя",
            "PUT": "Изменение информации о пользователе",
            "DELETE": "Удаление информации о пользователе"
        },
        "/api/users/me/profile": {
            "GET": "Профиль пользователя",
            "POST": "Изменение профиля пользователя"
        },
        "/api/users/profiles": {
            "GET": "Профили всех пользователей"
        },
        "api/images/recognize-face": {
            "POST": "Определяет возраст, пол и эмоцию лица на изображении"
        },
        "api/images/compare-faces": {
            "POST": "Сравнивает два загруженных изображения на предмет схожести лиц"
        },
        "api/images/count-people": {
            "POST": "Определяет количество лиц на изображении"
        },
        "api/images/generate_image": {
            "POST": "Генерирует изображение по описанию"
        },
        "api/images/generate_avatar": {
            "POST": "Генерирует уникальный аватар по фотографии пользователя"
        },
    }
