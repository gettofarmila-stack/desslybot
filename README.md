# 🤖 DesslyBot

Telegram-бот для продажи игровых товаров с интеграцией DesslyHub.

## 🚀 Возможности

- 💰 Пополнение Steam по низким ценам
- 🎁 Отправка подарков
- 🎟 Работа с ваучерами
- 👥 Реферальная система
- 💳 Интеграция с платёжкой
- ⚡ Быстрая обработка заказов

---

## 🧩 Стек

- Python 3.10+
- aiogram 3
- SQLAlchemy
- PostgreSQL
- DesslyHub API

---

## 📦 Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/gettofarmila-stack/desslybot.git
cd desslybot
```

---

### 2. Создай виртуальное окружение

```bash
python -m venv venv
```

Активируй его:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / MacOS**

```bash
source venv/bin/activate
```

---

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

---

## ⚙️ Настройка

Создай файл `.env` в корне проекта и заполни его:

```env
TOKEN=токен_телеграм_бота
DESSLY_TOKEN=токен_desslyhub
POSTGRES_URL=postgresql+asyncpg://postgres:1234@127.0.0.1:5432/desslybot

MARKET_CHANNEL=https://t.me/sanyabaranovbio
SUPPORT_LINK=https://t.me/sanyalca
REVIEW_LINK=https://t.me/sanyabaranovbio

SERVICE_NAME=SanyaStore

PROJECT_UUID=твой_uuid_платёжки
SIGN_2328=твой_api_ключ_платёжки
```

---

## 🔑 Получение доступа

### DesslyHub

Чтобы получить `DESSLY_TOKEN`, напиши менеджеру:

👉 [https://t.me/DesslyHub_Manager](https://t.me/DesslyHub_Manager)

Укажи ссылку на своего бота или магазин, тебе помогут с подключением.

Если в проекте есть инструкция по регистрации - смотри соответствующий раздел в репозитории.

---

### Платёжка (2328)

Регистрация:
👉 [https://my.2328.io/register?invite=GA3LH5XYML](https://my.2328.io/register?invite=GA3LH5XYML)

После регистрации получишь:

* `PROJECT_UUID`
* `SIGN_2328`

---

## 🗄 База данных

Используется PostgreSQL.

Пример строки подключения:

```
postgresql+asyncpg://postgres:1234@127.0.0.1:5432/desslybot
```

Перед запуском убедись, что база создана и доступна.

---

## ▶️ Запуск

```bash
python bot.py
```

---

## 🛠 Дополнительная настройка

В файле `config.py` есть переменные, которые можно изменить под себя:

* настройки режима разработки
* дополнительные параметры сервиса
* айди админов в телеграм

---

## ⚠️ Важно

* Без токенов и доступа к API бот работать не будет
* Проверь правильность `.env`
* Убедись, что PostgreSQL запущен

---

## 📬 Поддержка

По вопросам проекта:

👉 Автор [https://t.me/sanyalca](https://t.me/sanyalca)
