# [Datanar](https://datanar.ru) - Нативная установка

> Это инструкция, которая по шагам распишет нативное развёртывание сайта на 
> локальной машине, приятного чтения!

## Содержание
- [Установка Python](#установка-python)
- [Установка Git](#установка-git)
  - [Windows](#windows)
  - [MacOS](#macos)
  - [Linux](#linux-debian--ubuntu)
- [Установка gettext](#установка-gettext)
  - [Windows](#windows-1)
  - [MacOS](#macos-1)
  - [Linux](#linux-debian--ubuntu-1)
- [Установка Redis](#установка-redis)
  - [Windows](#windows-2)
  - [MacOS](#macos-2)
  - [Linux](#linux-debian--ubuntu-2)
- [Установка Postgres](#установка-postgresql)
  - [Windows](#windows-3)
  - [MacOS](#macos-3)
  - [Linux](#linux-debian--ubuntu-3)
- [Клонирование репозитория](#клонирование-репозитория)
- [Установка виртуального окружения](#установка-виртуального-окружения)
- [Установка зависимостей](#установка-зависимостей)
- [Настройка сервера](#настройка-сервера)
- [Запуск сервера Django](#запуск-сервера-django)

## Установка Python
Для запуска этого проекта вам потребуется Python
  
Если у вас его еще нет, вы можете скачать его с официального 
[сайта](https://www.python.org/downloads/), рекомендуется установить версию в 
диапазоне 3.9 - 3.12 (но лучше всё же 3.12)

## Установка Git
### Windows
1. Скачайте установщик Git с официального
   [сайта](https://git-scm.com/download/win)
2. Запустите установщик и следуйте инструкциям на экране

### MacOS
1. Откройте терминал
2. Установите Git с помощью [Homebrew](https://brew.sh/ru/):
   ```bash
   brew install git
   ```
    
### Linux (Debian / Ubuntu)
1. Откройте терминал
2. Обновите список пакетов:
   ```bash
   sudo apt update
   ```
3. Установите Git с помощью следующей команды:
   ```bash
   sudo apt install git
   ```

После установки Git с помощью команды `git --version` вы можете проверить его 
версию и убедиться, что он установлен правильно

## Установка gettext
### Windows
1. Скачать
   [установщик](https://mlocati.github.io/articles/gettext-iconv-windows.html)
   gettext для windows
2. Запустите установщик и следуйте инструкциям на экране

### MacOS
1. Откройте терминал
2. Установите gettext с помощью [Homebrew](https://brew.sh/ru/):
   ```bash
   brew install gettext
   ```

### Linux (Debian / Ubuntu)
1. Откройте терминал
2. Установите gettext с помощью следующей команды:
   ```bash
   sudo apt install gettext
   ```

## Установка Redis
> Для celery (очередь задач, для обработки файлов со ссылками) требуется 
> установить redis. Этот шаг можно пропустить, если этот функционал не нужен.

### Windows
> Redis официально не поддерживает Windows, поэтому ниже описанный способ может
> не сработать (лично у нас получилось, но только без виртуального окружения)

1. Скачать неофициальный [порт](https://github.com/tporadowski/redis/releases)
   и запустить установщик msi (от имени администратора). В диспетчере задач в
   службах должна появится служба `Redis`

### MacOS
1. Откройте терминал
2. Установите Redis с помощью [Homebrew](https://brew.sh/ru/):
   ```bash
   brew install redis
   ```
3. Запустите Redis:
   ```bash
   brew services start redis
   ```

### Linux (Debian / Ubuntu)
1. Откройте терминал
2. Установите Redis с помощью следующей команды:
   ```bash
   sudo apt install redis
   ```

## Установка Postgresql
> Postgresql - мощная и современная система управления базой данных. Хорошо 
> подходит как БД в боевой среде. Его установку можно пропустить, при простой
> нативной установке, а в качестве замены использовать более простую sqlite3
> (база данных в одном файле)

### Windows
1. Скачать [установщик](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
   (рекомендуемая версия 16, но можно и 15)
2. Запустить установщик и следовать инструкциям на экране,
   вас попросят придумать и ввести пароль для суперпользователя, запомните его
3. Откройте терминал
4. Перейдите в директорию установки используя команду `cd`, скорее всего 
   команда полностью выглядит так:
   ```bash
   cd C:\Program Files\PostgreSQL\16\bin
   ```
5. Запустите postgres клиент (введя пароль, который вы вводили при установке):
   ```bash
   psql -U postgres
   ```

### MacOS
1. Откройте терминал
2. Установите Postgresql c помощью [Homebrew](https://brew.sh/ru/):
   ```bash
   brew install postgresql
   ```
3. Запустите Postgresql:
   ```bash
   brew services start postgresql
   ```
4. Запустите postgres клиент:
   ```bash
   psql -U postgres
   ```

### Linux (Debian / Ubuntu)
1. Откройте терминал
2. Установите Postgresql с помощью следующей команды:
   ```bash
   sudo apt install postgresql
   ```
3. Запустите postgres клиент:
   ```bash
   sudo -u postgres psql
   ```

Теперь когда вы запустили postgres клиент, создайте БД для проекта, а также
пользователя, которой будет с ней работать:
```sql
CREATE USER webmaster WITH PASSWORD 'this_very_secret_password_for_database';
CREATE DATABASE database;
GRANT ALL PRIVILEGES ON DATABASE database TO webmaster;
ALTER ROLE "webmaster" SET timezone TO 'UTC';
ALTER ROLE "webmaster" SET client_encoding TO 'utf8';
```

И не забудьте выйти из postgres клиента и вернуться к проекту
```
exit;
```

## Клонирование репозитория
1. Откройте терминал
2. Перейдите в директорию, где вы хотите сохранить проект, используя `cd`.
   Например: `cd %USERPROFILE%\Documents\myProjects` или `cd ~/myProject`
3. Клонируйте репозиторий, используя следующую команду:
   ```bash
   git clone https://github.com/Gray-Advantage/Datanar-Django.git
   ```

## Установка виртуального окружения
### Windows
> [!WARNING]
> Лично у нас на Windows не получилось запустить redis в виртуальном окружении,
> поэтому если вы его установили и сталкиваетесь с ошибками, попробуйте не 
> создавать его (пропустить шаг 2 и 3 и просто перейти в директорию)

> [!NOTE]
> Стоит отметить, что не всегда на linux будет работать python3, а на windows 
> python, попробуйте оба варианта написания команды

1. В терминале перейдите в директорию проекта:
   ```bash
   cd datanar
   ```
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```
3. Активируйте виртуальное окружение:
   ```bash
   venv\Scripts\activate
   ```

### MacOS или Linux (Debian / Ubuntu)
1. В терминале перейдите в директорию проекта:
   ```bash
   cd datanar
   ```
2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   ```
3. Активируйте виртуальное окружение:
   ```bash
   source venv/bin/activate
   ```

## Установка зависимостей
> [!NOTE]
> Как и с python/python3 возможны два варианта команд - c `pip` или c `pip3`

Установите все необходимые пакеты для работы в боевой среде, используя prod.txt 
```bash
pip install -r requirements/prod.txt
```
Необязательно, но можно установить и test.txt для проверки целостности проекта
```bash
pip install -r requirements/test.txt
```
Установить сразу и prod.txt и test.txt зависимости можно через dev.txt
```bash
pip install -r requirements/dev.txt
```

## Настройка сервера
1. Создайте в корне проекта файл `.env` скопировав содержимое из `.env.example`
   - На Windows:
     ```bash
     copy .env.example .env
     ```
   - На Mac или Linux:
     ```bash
     cp .env.example .env
     ```

   И измените все настройки в соответствии с [этой инструкцией](env-file.md).
   Если не добавить `.env` или просто продублировать информацию из
   `.env.example` в `.env`, приложение будет запущено с дефолтными настройками,
   что не рекомендуется по соображениям безопасности, а также часть функций 
   либо не будет работать, либо и вовсе вызовет ошибки.
2. Скомпилируйте файлы локализации данного проекта: 
   ```bash
   django-admin compilemessages
   ```
   Если возникает ошибка, то перейдите в директорию `datanar`:
   ```bash
   cd datanar
   ```
   И повторите немного изменённую команду:
   - Windows
     ```bash
     python manage.py compilemessages
     ```
   - macOS или linux (Debian / Ubuntu)
     ```bash
     python3 manage.py compilemessages
     ```
   Перейдите в директорию `datanar`, если вы этого ещё не сделали:
   ```bash
   cd datanar
   ```
3. Создайте первую миграцию базы данных:
   - Windows
     ```bash
     python manage.py migrate
     ```
   - macOS или linux (Debian / Ubuntu)
     ```bash
     python3 manage.py migrate
     ```
4. Также сделайте сбор статики, если будет предупреждение про перезапись файлов 
   введите "yes":
   - Windows
     ```bash
     python manage.py collectstatic
     ```
   - macOS или linux (Debian / Ubuntu)
     ```bash
     python3 manage.py collectstatic
     ```
5. И последние - создать суперпользователя (админа) сайта:
   - Windows
     ```bash
     python manage.py init_superuser
     ```
   - macOS или linux (Debian / Ubuntu)
     ```bash
     python3 manage.py init_superuser
     ```

   Будет создан суперпользователь с логином, почтой и паролем из 
   [`.env`](env-file.md/#пользователи-и-суперпользователь) файла. Теперь при
   авторизации с этими данными на сайте в правом верхнем углу, нажав на свою 
   аватарку, вы увидите в списке пункты "Панель управления" и "Админка"

## Запуск сервера Django
Запустите рабочий процесс celery в новой консоли
(только если [установили Redis](#установка-redis)):
```bash
celery -A datanar worker -l INFO
```

[Установив зависимости `test.txt`](#установка-зависимостей), вы также получите
возможность запустить тесты для локальной проверки целостности проекта:
- Windows
  ```bash
  python manage.py test
  ```
- macOS или linux (Debian / Ubuntu)
  ```bash
  python3 manage.py test
  ```

Ожидаемый результат после выполнения команды: `OK`

Ну и наконец, запустите сервер Django:
- Windows
  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```
- MacOS или Linux (Debian / Ubuntu)
  ```bash
  python3 manage.py runserver 0.0.0.0:8000
  ```

После запуска вы должны иметь возможность открыть проект в браузере по адресу 
http://127.0.0.1:8000/ или http://localhost:8000/.

Вы превосходны и роскошны! ©

> [!IMPORTANT]
> Помните, что Django при `DATANAR_DJANGO_DEBUG=False` не отдаёт статику 
> (например картинки), для этого обычно настраивают отдельный web-сервер
> ([Nginx](https://nginx.org/ru/), например) или же просто запускают Django
> в режиме разработки (`DATANAR_DJANGO_DEBUG=True`). См. подробней о 
> [`DATANAR_DJANGO_DEBUG`](env-file.md/#datanar_django_debug)