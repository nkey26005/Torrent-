# 🚀 Мой Персональный Торрент Клиент (v1)

**Самый быстрый и простой торрент-клиент для личного использования.**  
Первая рабочая версия — лёгкая, быстрая и полностью функциональная.

## ✨ Особенности v1
- Поддержка **magnet-ссылок** и **.torrent** файлов
- Супер-быстрая загрузка благодаря aria2c (один из лучших движков)
- Автоматический resume (продолжение загрузки)
- Оптимизировано под высокую скорость (16 соединений + split)
- Простой CLI с красивым прогрессом
- Работает на Windows, Linux, macOS

## 📦 Установка (2 минуты)

### 1. Установи aria2c
**Windows:**
```bash
winget install aria2.aria2
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install aria2
```

**macOS:**
```bash
brew install aria2
```

### 2. Клонируй репозиторий
```bash
git clone https://github.com/nkey26005/Torrent-.git
cd Torrent-
```

### 3. Запуск
```bash
python main.py "magnet:?xt=urn:btih:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" -p ./downloads
```

Или с файлом:
```bash
python main.py путь/к/фильм.torrent -p ./downloads
```

## 🚀 Примеры использования

```bash
# Обычная загрузка
python main.py "magnet:..."

# В конкретную папку + сидировать 30 минут
python main.py "magnet:..." -p ./movies --seed-time 30

# Максимум скорости
python main.py "magnet:..." --max-peers 500
```

## 🛠️ Roadmap (что будет дальше)

- **v2** — Искусственные пиры на одном ПК (несколько сессий одновременно) → скорость взлетит
- **v3** — Красивый GUI
- **v4** — Автопоиск + интеграция с трекерами
- **v5** — Использование RTX 5060 Ti для ускорения

Хочешь — сразу делаем **v2** с искусственными пирами?

## 📄 Лицензия
MIT — это твой клиент, делай что хочешь!

---

Сделано с ❤️ для Никиты | 2026
