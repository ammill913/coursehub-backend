# CourseHub

## Ідея

Платформа для зручного вибору та запису на вибіркові університетські дисципліни. 
Студент часто обирає дисципліни вільного вибору навмання: інформація розкидана
по різних сторінках, незрозуміло, скільки залишилось місць, і ніхто не знає,
що думають про курс ті, хто його вже проходив.

**CourseHub** збирає це в одному місці:

- каталог курсів з пошуком за назвою й ключовими словами;
- фільтри за факультетом, викладачем, семестром і мовою викладання;
- сортування за кількістю кредитів ECTS, рейтингом серед студентів і кількістю вільних місць;
- сторінки викладачів і факультетів, де видно їхні курси;
- відгуки та оцінки студентів, з яких складається рейтинг курсу;
- запис на курс і скасування запису;
- профіль студента з історією його записів.

---

## Ендпоінти
Усі дані передаються у форматі JSON.

*позначка 🔒 означає, що потрібен авторизований користувач*

### Авторизація

| Метод | URL | Призначення |
|---|---|---|
| POST | `/api/auth/register/` | Реєстрація |
| POST | `/api/auth/login/` | Вхід |
| POST | `/api/auth/logout/` 🔒 | Вихід |

#### `POST /api/auth/register/`

Request body:

```json
{
  "email": "student@ukma.edu.ua",
  "password": "secret123",
  "first_name": "Олена",
  "last_name": "Коваль"
}
```

Response `201`:

```json
{ "id": 7, 
   "email": "student@ukma.edu.ua", 
   "first_name": "Олена", 
   "last_name": "Коваль" 
}
```

Помилки: `400`, якщо email уже зайнятий або пароль занадто простий.

#### `POST /api/auth/login/`

Request body: `{ "email": "...", "password": "..." }`

Response `200`: `{ "token": "..." }`
Помилка: `401` при неправильних даних.

#### `POST /api/auth/logout/` 🔒

Response `204`, без тіла.
Помилка: `401` без авторизації.

---

### Профіль

| Метод | URL | Призначення |
|---|---|---|
| GET | `/api/users/me/` 🔒 | Мій профіль |
| PATCH | `/api/users/me/` 🔒 | Редагувати мої дані |
| GET | `/api/users/me/enrollments/` 🔒 | Історія моїх записів на курси |

#### `GET /api/users/me/`

Response `200`:

```json
{ "id": 7, "email": "student@ukma.edu.ua", "first_name": "Олена", "last_name": "Коваль", "faculty": "ФСНСТ" }
```

#### `PATCH /api/users/me/`

Request body (будь-які з полів): `{ "first_name": "Олена", "last_name": "Коваль", "faculty": "ФСНСТ" }`
Response `200`: оновлений профіль. 
Помилка: `400`.

#### `GET /api/users/me/enrollments/`

Response `200`:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 15,
      "course": { "id": 3, "title": "Вступ до політичної аналітики" },
      "enrolled_at": "2026-10-10 14:30:00"
    }
  ]
}
```

---

### Курси

| Метод | URL | Призначення |
|---|---|---|
| GET | `/api/courses/` | Список курсів з пошуком, фільтрами, сортуванням |
| POST | `/api/courses/` 🔒 | Додати курс |
| GET | `/api/courses/{id}/` | Сторінка курсу |
| PATCH | `/api/courses/{id}/` 🔒 | Редагувати курс |
| DELETE | `/api/courses/{id}/` 🔒 | Видалити курс |

#### `GET /api/courses/`

Параметри (усі необов'язкові):

| Параметр | Приклад | Значення |
|---|---|---|
| `search` | `?search=політика` | пошук за назвою та ключовими словами |
| `faculty` | `?faculty=2` | id факультету |
| `teacher` | `?teacher=5` | id викладача |
| `semester` | `?semester=autumn` | `autumn` або `spring` |
| `language` | `?language=en` | мова викладання |
| `ordering` | `?ordering=-rating` | сортування: `ects_credits`, `rating`, `free_places`; мінус означає за спаданням |
| `page`, `page_size` | `?page=2` | пагінація |

Response `200`:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "title": "Вступ до політичної аналітики",
      "ects_credits": 4,
      "semester": "autumn",
      "language": "uk",
      "faculty": { "id": 2, "name": "ФСНСТ" },
      "teachers": [{ "id": 5, "full_name": "Яковлєв Максим Володимирович" }],
      "rating": 4.6,
      "free_places": 8
    }
  ]
}
```

#### `POST /api/courses/` 🔒

Request body:

```json
{
  "title": "Вступ до політичної аналітики",
  "description": "Базові методи аналізу політичних подій.",
  "keywords": "політика, аналітика, дані",
  "ects_credits": 4,
  "semester": "autumn",
  "language": "uk",
  "capacity": 25,
  "faculty_id": 2,
  "teacher_ids": [5]
}
```

Response `201`: створений курс (формат як у деталях). Помилка: `400`, `403`.

#### `GET /api/courses/{id}/`

Response `200`:

```json
{
  "id": 3,
  "title": "Вступ до політичної аналітики",
  "description": "Базові методи аналізу політичних подій.",
  "keywords": "політика, аналітика, дані",
  "ects_credits": 4,
  "semester": "autumn",
  "language": "uk",
  "capacity": 25,
  "free_places": 8,
  "rating": 4.6,
  "reviews_count": 12,
  "faculty": { "id": 2, "name": "ФСНСТ" },
  "teachers": [{ "id": 5, "full_name": "Яковлєв Максим Володимирович" }]
}
```

Помилка: `404`.

#### `PATCH /api/courses/{id}/` 🔒

Request body: будь-які поля з `POST`. 
Response `200`: оновлений курс. 
Помилки: `400`, `403`, `404`.

#### `DELETE /api/courses/{id}/` 🔒

Response `204`. 
Помилки: `403`, `404`.

---

### Відгуки на курси

| Метод | URL | Призначення |
|---|---|---|
| GET | `/api/courses/{id}/reviews/` | Відгуки на курс |
| POST | `/api/courses/{id}/reviews/` 🔒 | Залишити відгук |
| PATCH | `/api/reviews/{id}/` 🔒 | Змінити свій відгук |
| DELETE | `/api/reviews/{id}/` 🔒 | Видалити свій відгук |

#### `GET /api/courses/{id}/reviews/`

Response `200`:

```json
[
  { "id": 9, "author": "Олена К.", "rating": 5, "comment": "Дуже корисний курс", "created_at": "2026-09-20 10:00:00" }
]
```

#### `POST /api/courses/{id}/reviews/` 🔒

Request body: `{ "rating": 5, "comment": "Дуже корисний курс" }` (`rating` від 1 до 5).
Response `201`: створений відгук.
Помилки: `400` (оцінка поза діапазоном).

#### `PATCH /api/reviews/{id}/` 🔒

Request body: `{ "rating": 4, "comment": "..." }`. 
Response `200`. 
Помилки: `403` (не мій відгук), `404`.

#### `DELETE /api/reviews/{id}/` 🔒

Response `204`. 
Помилки: `403`, `404`.

---

### Викладачі

| Метод | URL | Призначення |
|---|---|---|
| GET | `/api/teachers/` | Список викладачів (`?search=`, `?faculty=`) |
| POST | `/api/teachers/` 🔒 | Додати викладача |
| GET | `/api/teachers/{id}/` | Сторінка викладача |
| PATCH | `/api/teachers/{id}/` 🔒 | Редагувати викладача |
| DELETE | `/api/teachers/{id}/` 🔒 | Видалити викладача |
| GET | `/api/teachers/{id}/courses/` | Усі курси викладача |

Request body (`POST`, `PATCH`):

```json
{ "full_name": "Яковлєв Максим Володимирович", "position": "доцент", "degree": "кандидат політичних наук", "faculty_id": 2 }
```

Response (`GET` деталі, `POST` `201`, `PATCH` `200`):

```json
{ 
   "id": 5, 
   "full_name": "Яковлєв Максим Володимирович", 
   "position": "доцент", 
   "degree": "кандидат політичних наук", 
   "faculty": { "id": 2, "name": "ФСНСТ" } 
}
```

`GET /api/teachers/{id}/courses/` повертає список курсів у тому ж форматі, що й `GET /api/courses/`.
`DELETE` повертає `204`. 
Помилки: `400`, `403`, `404`.

---

### Факультети

| Метод | URL | Призначення |
|---|---|---|
| GET | `/api/faculties/` | Список факультетів |
| POST | `/api/faculties/` 🔒 | Додати факультет |
| GET | `/api/faculties/{id}/` | Сторінка факультету |
| PATCH | `/api/faculties/{id}/` 🔒 | Редагувати факультет |
| DELETE | `/api/faculties/{id}/` 🔒 | Видалити факультет |
| GET | `/api/faculties/{id}/courses/` | Усі курси факультету |

Request body (`POST`, `PATCH`): 
`{ "name": "ФСНСТ", "description": "Факультет соціальних наук та соціальних технологій" }`

Response (`GET` деталі, `POST` `201`, `PATCH` `200`): 
`{ "id": 2, "name": "ФСНСТ", "description": "..." }`

`GET /api/faculties/{id}/courses/` повертає список курсів у форматі `GET /api/courses/`.
`DELETE` повертає `204`. 
Помилки: `400`, `403`, `404`.

---

### Записи на курси

| Метод | URL | Призначення |
|---|---|---|
| POST | `/api/enrollments/` 🔒 | Записатися на курс |
| DELETE | `/api/enrollments/{id}/` 🔒 | Скасувати свій запис |

#### `POST /api/enrollments/` 🔒

Request body: `{ "course_id": 3 }`

Response `201`:

```json
{ "id": 15, "course_id": 3, "enrolled_at": "2026-10-10 14:30:00" }
```

Помилки:
- `404`, якщо курсу не існує;
- `409`, якщо вільних місць немає або користувач уже записаний на цей курс.

#### `DELETE /api/enrollments/{id}/` 🔒

Response `204`. Помилки: `403`, `404`.

---

### Про нас

| Метод | URL | Призначення |
|---|---|---|
| GET | `/api/about/` | Контакти та правила запису |

Response `200`:

```json
{
  "contacts": "Деканат ФСНСТ, корпус 6, кабінет 213, тел. (044) 463 58 63",
  "enrollment_rules": "Запис на курси відкритий до початку семестру. Скасувати запис можна до його старту."
}
```

---

## Схема бази даних

![Схема БД](db-schema.png)