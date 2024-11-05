### Запуск 

```bash
sudo docker compose up -d --build
sleep 5
sudo docker compose exec bot alembic revision --autogenerate
sudo docker compose exec bot alembic upgrade head
```

или

```bash
./start.sh
```

### TODOS
- добавить возможность добавлять количество разработчиков в проекте
- добавить возможность принудительного добавления и удаления разработчиков
