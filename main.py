#!/usr/bin/env python3
"""
Мой Персональный Торрент Клиент v1.0
Простейшая рабочая версия на базе aria2c
"""

import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="🚀 Мой Персональный Торрент Клиент v1 — быстрый и простой",
        epilog="Пример: python main.py 'magnet:?xt=urn:btih:...' -p ./movies"
    )
    parser.add_argument("source", help="Magnet-ссылка или путь к .torrent файлу")
    parser.add_argument("-p", "--path", default="downloads", help="Папка для загрузок")
    parser.add_argument("--seed-time", default="0", help="Минут сидировать после загрузки (0 = не сидировать)")
    parser.add_argument("--max-peers", default="200", help="Максимум пиров")
    args = parser.parse_args()

    save_path = Path(args.path).resolve()
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"📥 Загрузка в: {save_path}")
    print(f"🔗 {args.source[:90]}..." if len(args.source) > 90 else f"🔗 {args.source}")

    cmd = [
        "aria2c",
        args.source,
        f"--dir={save_path}",
        f"--seed-time={args.seed_time}",
        f"--bt-max-peers={args.max_peers}",
        "--max-connection-per-server=16",
        "--min-split-size=1M",
        "--split=16",
        "--continue=true",
        "--check-integrity=true",
        "--bt-enable-lpd=true",
        "--enable-peer-exchange=true",
        "--bt-tracker-connect-timeout=15",
        "--timeout=30",
        "--retry-wait=5",
        "--summary-interval=1",
    ]

    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print("\n✅ Загрузка завершена!")
        else:
            print(f"\n⚠️ Завершено с кодом {result.returncode}")
    except FileNotFoundError:
        print("\n❌ ОШИБКА: aria2c не найден в системе!")
        print("\n📦 Как установить aria2c:")
        print("   Windows: winget install aria2.aria2")
        print("   Linux:   sudo apt update && sudo apt install aria2")
        print("   macOS:   brew install aria2")
        print("\nПосле установки запусти меня снова.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Загрузка остановлена пользователем.")
        sys.exit(0)

if __name__ == "__main__":
    main()