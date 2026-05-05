<div align="center">
  <img src="./assets/logo.png" alt="logo" width="200" height="200" />
  <h1>Проект: calorie_tracker_toma</h1>
  <p><b><i>Десктоп‑трекер калорий: авторизация, профиль, приёмы пищи, прогресс и отчёты</i></b></p>
  <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-2.0.0+-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
    <img alt="SQLite" src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
    <img alt="CustomTkinter" src="https://img.shields.io/badge/CustomTkinter-5.2.0+-0A7CFF?style=for-the-badge" />
    <img alt="Matplotlib" src="https://img.shields.io/badge/Matplotlib-3.7.0+-11557C?style=for-the-badge" />
  </div>
</div>

## ✨ Возможности

- Регистрация и вход, хранение сессии пользователя;
- Профиль: рост/вес/возраст/пол, дневная цель калорий;
- Добавление приёмов пищи и расчёт дневного прогресса;
- Отчётность и визуализация (графики).

---

## 🧱 Архитектура

```mermaid
flowchart LR
  GUI["GUI (CustomTkinter)"] --> C["Controllers"]
  C --> S[Services]
  S --> R["Repositories"]
  R --> DB[(SQLite)]
  S --> D["Domain models"]
```

- `app/domain` - доменные сущности и интерфейсы репозиториев;
- `app/repositories` - реализация хранилищ на SQLAlchemy + SQLite;
- `app/services` - бизнес-логика (авторизация, калории, прогресс, профиль);
- `app/gui` - GUI (окно авторизации + главное окно с вкладками);
- `app/utils` - безопасность, логирование, работа с сессией, исключения.

---

## 🚀 Запуск

```powershell
# создай и активируй окружение
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# установи зависимости
pip install -U pip
pip install -e .

# мигрируй бд и запусти приложение
py .\init_db.py
py .\run.py
```

---

## ⚙️ Конфигурация

Основные пути и параметры описаны в [config.py](./app/config.py):

- БД: `calories.db` (SQLite) в корне проекта
- Файл сессии: `.session`
- Логи: `calorie_tracker.log`

---

<div align="center">
  <img src="./assets/logo.png" alt="logo" width="100" height="100" />
  <br>
    <sub><b>Десктоп-приложение // Трекер калорий</b></sub>
    <br>
    <sup><i>Made with cranch by <a href="https://github.com/nineteentearz" target="_blank" title="nineteentearz">nineteentearz</a></i></sup>
</div>
