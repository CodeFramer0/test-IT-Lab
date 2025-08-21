# IT Lab Test Work

## Требования
- Docker
- Docker
- Файл `.env` с настройками окружения

---

## Установка и запуск проекта

1. **Клонировать репозиторий**
```bash
git clone 
cd 
```

2. **Настроить .env**
```bash
cp .env.template .env
nano .env
Указать BOT_TOKEN
```


3. **Запустить проект**
```bash
docker compose -f 'docker-compose.yml' up -d --build 
```
## Доступы
```bash
При старте проекта автоматически создается учетная запись
login:admin
password:admin

Для доступа в админ панель необходимо перейти по http://localhost/admin/
```
## API
```bash
API Находится по адресу 
http://localhost/api/v1/
```
