# 🪙 CoinsGram – Коллекционер монет

**CoinsGram** — это платформа для нумизматов: создавай коллекцию монет, смотри чужие находки, подписывайся на коллекционеров, комментируй, оценивай и экспортируй свои избранные монеты.

## 🚀 Быстрый старт

### 1. Клонируй проект
```bash
git clone https://github.com/MichaelV6/CoinsGram.git
cd CoinsGram/backend
```

### 2. Установи зависимости
```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows
pip install -r requirements.txt
```

### 3. Применяй миграции
```bash
python manage.py migrate
```

### 4. Создай суперпользователя (админа)
```bash
python manage.py createsuperuser
```
Введи email, имя пользователя и пароль по инструкции в консоли.

### 5. Запусти сервер
```bash
python manage.py runserver
```
Сервер будет доступен по адресу: http://127.0.0.1:8000

## 🛠 Вход в админку

Админка доступна по адресу:
http://127.0.0.1:8000/admin

Используй логин и пароль, указанные при создании суперпользователя.

## 📖 Документация API

### ReDoc
Подробная документация и тестирование API в браузере:
http://127.0.0.1:8000/api/docs/

### SwaggerUI (Удобный инстурмент для проверки всех API-запросов)
Можно перейти по кнопке в шапке страницы. Вы ее увидите.
Нажми Authorize, вставь `Bearer <твой_access_токен>` без кавычек.
Пробуй любые эндпоинты прямо из интерфейса.

## 🔑 Авторизация (JWT)

- Регистрация — `POST /api/users/` (email, username, имя, фамилия, пароль, аватар).
- Получение токена — `POST /api/auth/jwt/create/` (email + пароль) → access + refresh.
- Использование — в Swagger UI или curl-запросах передавай заголовок:
```
Authorization: Bearer <access>
```

## 🔥 Основные возможности

- Пользователи: регистрация, профиль, смена пароля, аватар.
- Монеты: CRUD, поиск, фильтрация, загрузка изображений.
- Теги: категоризация монет. (Только админ может создавать их)
- Избранное: добавление, удаление, экспорт Word.
- Подписки: подписаться/отписаться от других пользователей.
- Комментарии: оставить, удалить, (опционально) править — только автор или админ.
- Экспорт: DOCX-файл списка избранного.

## ⚙️ Примеры запросов (curl)

### Получить токен
```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpass"}'
```

### Добавить монету в избранное
```bash
curl -X POST http://127.0.0.1:8000/api/favorites/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d '{"coin":3}'
```

### Скачать избранное в Word
```bash
curl -X GET http://127.0.0.1:8000/api/favorites/download/ \
  -H "Authorization: Bearer <access>" --output favorites.docx
```

### Отписаться от пользователя
```bash
curl -X DELETE "http://127.0.0.1:8000/api/subscriptions/by_user/?subscribed_to=5" \
  -H "Authorization: Bearer <access>"
```

### Добавить комментарий
```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d '{"coin":3,"text":"Отличная монета!"}'
```

## 💻 Структура репозитория
```
CoinsGram/
├─ backend/        # Django REST API
 └─ docs/           # OpenAPI спецификации, схемы
```

## 👨‍💻 Советы для проверяющего

- Права доступа: многие действия требуют JWT.
- Файлы: загрузка аватаров и изображений монет — multipart/form-data.
- Ошибки: возвращаются в JSON с понятными сообщениями.
- Экспорт: проверяй DOCX-файл через Word/LibreOffice.

## 📬 Контакты

Михаил Волобуев (ПИ01/23б)
- ✉️ volobuev.m@edu.rea.ru
- 🔗 GitHub: [MichaelV6/CoinsGram](https://github.com/MichaelV6/CoinsGram)
