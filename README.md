# 🚀 OTUS UI + API Test Automation Project

Автоматизированный проект тестирования, включающий:

- UI тесты для PrestaShop (Selenium + Page Object)
- API тесты для Restful-booker (pytest + requests)
- CI/CD через Jenkins
- Отчётность через Allure
- Запуск в Docker / Docker Compose

---

## 📌 О проекте

*   **Двойное покрытие**: 10+ UI-тестов для PrestaShop и 20+ API-тестов для Restful-booker.
*   **Паттерн PageObject**: UI-тесты построены на классическом PageObject, что делает их лёгкими в поддержке.
*   **API-клиент**: Собственный клиент для Restful-booker, инкапсулирующий всю логику HTTP-запросов.
*   **Контейнеризация**: Полная среда (браузеры, база данных, приложение) поднимается через `docker-compose.yml`.
*   **Удалённый запуск браузеров**: Интеграция с **Selenoid** для запуска UI-тестов в изолированных контейнерах.
*   **CI/CD с Jenkins**: Автоматический запуск тестов с параметризацией (выбор браузера, scope тестов, количество потоков и т.д.).
*   **Параметризация тестов**: Широкое использование `@pytest.mark.parametrize` для увеличения тестового покрытия без дублирования кода.
*   **Промышленная отчётность**: Интеграция с **Allure Report**. К каждому тесту прикрепляются логи, а в случае падения API-теста — последний запрос и ответ сервера (благодаря `ApiContext`). Для UI-тестов при падении прикрепляется скриншот.
*   **Логирование**: Многоуровневое логирование с помощью модуля `logging`.
---

## 🛠️ Стек технологий

- Python 3.12
- pytest
- requests
- Selenium WebDriver
- Allure Report
- Docker / Docker Compose
- Selenoid
- Jenkins

---

## ✅ Реализовано

### UI тесты
- PageObject pattern
- Кроссбраузерность
- Скриншоты при падении

### API тесты
- CRUD операции
- Негативные кейсы
- Параметризация
- Логирование
- Allure attachments

---

## ▶️ Запуск тестов

### 1. Клонирование репозитория

```bash
git clone https://github.com/AleksKhrap/otus_ui_tests/
```

### 2. Запуск контейнеров Prestashop и Selenoid

```bash
docker-compose up -d
```
Можно добавить профиль local для запуска контейнера с тестами **локально** без Jenkins.
Но тогда нужно предварительно собрать и образ тестового контейнера:
```bash
docker build -t prestashop-tests:latest .
```

### 3. Запуск Jenkins

```bash
docker-compose -f docker-compose-jenkins.yml up -d
```

### 4. Настройка Jenkins
Необходимо войти в интерфейс и установить плагины (как минимум Allure, Pipelines,
Docker, Git).

- Логин: admin
- Пароль найти в контейнере jenkins: 
```bash
docker exec jenkins cat //var/jenkins_home/secrets/initialAdminPassword
```

Далее настроить пайплайн, указав в настройках скрипт - скопировать из Jenkinsfile или указать путь к данному репозиторию 
и ветку `feature/api-tests`

### 5. Запуск пайплайна
Кликнуть "Build Now", затем подтвердить кнопкой "Create" - первый пайплайн создан.
Далее при необходимости можно указать переменные.

### 6. Завершение работы

Существует два варианта завершения работы контейнера: 

- Для остановки процессов используйте команду:
```bash
docker-compose stop
```

- Если необходимо полностью очистить память или вы внесли какие-то изменения, то:
```bash
docker-compose down
```
- Или для полной очистки (включая volumes):
```bash
docker-compose down -v
```
- Аналогично останавливаем Jenkins:
```bash
docker-compose -f docker-compose-jenkins.yml down
```

---

## 📊 Allure

Отчет Allure доступен в Jenkins в левом меню после запуска пайплайна.

При локальном запуске:
```bash
allure serve allure-results
```

---

## 👨‍💻 Автор

AleksKhrap


