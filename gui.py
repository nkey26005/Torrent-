#!/usr/bin/env python3
"""
Torrent- v1.2 - GUI с массой проверок и понятными ошибками
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import shutil
from pathlib import Path
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TorrentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Torrent- v1.2 | Персональный Торрент Клиент")
        self.geometry("780x620")
        self.resizable(False, False)

        self.download_path = ctk.StringVar(value=str(Path.home() / "Downloads"))
        self.process = None
        self.is_downloading = False

        self.create_widgets()
        self.check_aria2c()   # проверка при запуске

    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#0f172a")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="🚀 Torrent- v1.2", font=ctk.CTkFont(size=24, weight="bold"), text_color="#38bdf8").pack(pady=10)

        # === SOURCE ===
        frame = ctk.CTkFrame(self)
        frame.pack(pady=6, padx=15, fill="x")

        ctk.CTkLabel(frame, text="Magnet или .torrent", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=3)

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=8)
        self.source_entry = ctk.CTkEntry(row, placeholder_text="Вставьте magnet: или нажмите кнопку...", width=480)
        self.source_entry.pack(side="left", padx=4, fill="x", expand=True)

        ctk.CTkButton(row, text="📁 .torrent", command=self.browse_torrent, width=85, height=28).pack(side="left", padx=2)
        ctk.CTkButton(row, text="📋 Буфер", command=self.paste_clipboard, width=80, height=28).pack(side="left")

        # === PATH + CHECKS ===
        path_frame = ctk.CTkFrame(self)
        path_frame.pack(pady=6, padx=15, fill="x")

        ctk.CTkLabel(path_frame, text="Папка сохранения", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)

        path_row = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_row.pack(fill="x", padx=8)
        self.path_entry = ctk.CTkEntry(path_row, textvariable=self.download_path, width=420)
        self.path_entry.pack(side="left", padx=4, fill="x", expand=True)
        ctk.CTkButton(path_row, text="📂", command=self.browse_folder, width=45, height=28).pack(side="left", padx=2)
        ctk.CTkButton(path_row, text="✅ Проверить место", command=self.check_space, width=120, height=28).pack(side="left", padx=3)

        # === BUTTONS ===
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=8)

        self.start_btn = ctk.CTkButton(btn_frame, text="▶️ Начать загрузку", command=self.start_download,
                                     fg_color="#16a34a", hover_color="#15803d", width=200, height=38, font=ctk.CTkFont(size=14, weight="bold"))
        self.start_btn.pack(side="left", padx=6)

        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹️ Остановить", command=self.stop_download,
                                    fg_color="#dc2626", hover_color="#b91c1c", width=130, height=38, state="disabled")
        self.stop_btn.pack(side="left", padx=6)

        self.open_btn = ctk.CTkButton(btn_frame, text="📂 Открыть папку", command=self.open_folder, width=130, height=38)
        self.open_btn.pack(side="left", padx=6)

        # === PROGRESS ===
        prog = ctk.CTkFrame(self)
        prog.pack(pady=6, padx=15, fill="x")

        self.progress_label = ctk.CTkLabel(prog, text="Готов к работе", font=ctk.CTkFont(size=13))
        self.progress_label.pack(pady=4)

        self.progress_bar = ctk.CTkProgressBar(prog, width=620, height=20, progress_color="#22d3ee")
        self.progress_bar.pack(pady=3)
        self.progress_bar.set(0)

        self.stats_label = ctk.CTkLabel(prog, text="Скорость: --   |   Пиры: --   |   Осталось: --", font=ctk.CTkFont(size=11))
        self.stats_label.pack(pady=2)

        # === LOG (новое!) ===
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=6, padx=15, fill="both", expand=True)

        ctk.CTkLabel(log_frame, text="📋 Лог загрузки (всё как на ладони)", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=8, pady=2)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, bg="#0f172a", fg="#e0f2fe", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=6, pady=4)

        self.status_label = ctk.CTkLabel(self, text="Введите ссылку или выберите файл", text_color="gray60")
        self.status_label.pack(pady=4)

    # ==================== ПРОВЕРКИ ====================
    def check_aria2c(self):
        if shutil.which("aria2c") is None:
            self.log("[⚠️] aria2c не найден! Установите: winget install aria2.aria2")
            messagebox.showerror("Ошибка", "aria2c не установлен!\n\nУстановите его:\nwinget install aria2.aria2")

    def check_space(self):
        path = self.download_path.get()
        try:
            total, used, free = shutil.disk_usage(path)
            free_gb = free / (1024**3)
            self.log(f"[✅] Свободно на диске: {free_gb:.1f} GB")
            if free_gb < 5:
                messagebox.showwarning("Мало места", f"Только {free_gb:.1f} GB свободно!\nРекомендуется минимум 10-15 GB")
        except Exception as e:
            self.log(f"[❌] Ошибка проверки места: {e}")

    def log(self, text):
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.update_idletasks()

    # ==================== ОСНОВНые ФУНкции ====================
    def browse_torrent(self):
        path = filedialog.askopenfilename(filetypes=[("Torrent files", "*.torrent")])
        if path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, path)

    def paste_clipboard(self):
        try:
            text = self.clipboard_get().strip()
            if text.startswith("magnet:"):
                self.source_entry.delete(0, "end")
                self.source_entry.insert(0, text)
            else:
                self.log("[⚠️] В буфере нет magnet-ссылки")
        except:
            self.log("[❌] Не удалось получить из буфера")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)

    def open_folder(self):
        path = self.download_path.get()
        os.startfile(path) if os.name == 'nt' else os.system(f'xdg-open "{path}"')

    def start_download(self):
        src = self.source_entry.get().strip()
        if not src:
            messagebox.showerror("Ошибка", "Введите magnet или выберите .torrent")
            return

        save_path = self.download_path.get()
        os.makedirs(save_path, exist_ok=True)

        # Проверки перед запуском
        if src.endswith(".torrent") and not os.path.exists(src):
            messagebox.showerror("Ошибка", "Файл .torrent не найден!")
            return

        self.is_downloading = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Проверка перед загрузкой...")
        self.log_text.delete("1.0", "end")
        self.log("[🚀] Запуск загрузки...")
        self.status_label.configure(text="Работает...", text_color="white")

        threading.Thread(target=self._run_aria2, args=(src, save_path), daemon=True).start()

    def _run_aria2(self, src, save_path):
        cmd = [
            "aria2c", src,
            f"--dir={save_path}",
            "--seed-time=0",
            "--max-connection-per-server=16",
            "--split=16",
            "--continue=true",
            "--summary-interval=1",
            "--bt-max-peers=200"
        ]

        self.log(f"[CMD] {' '.join(cmd)}")

        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, creationflags=0x08000000 if os.name == 'nt' else 0
            )

            for line in iter(self.process.stdout.readline, ''):
                if not self.is_downloading:
                    break
                line = line.strip()
                if line:
                    self.after(0, lambda l=line: self._parse_and_log(l))

            if self.is_downloading:
                self.after(0, self._finish)

        except Exception as e:
            self.after(0, lambda: self.log(f"[❌] Критическая ошибка: {e}"))
            self.after(0, self._reset)

    def _parse_and_log(self, line):
        self.log(line)

        # Прогресс
        if "%" in line and "(" in line:
            try:
                match = re.search(r"\((\d+\.?\d*)%\)", line)
                if match:
                    p = float(match.group(1))
                    self.progress_bar.set(p / 100)
                    self.progress_label.configure(text=f"Загрузка: {p:.1f}%")
            except:
                pass

        # Статистика
        if "DL:" in line:
            try:
                speed = re.search(r"DL:([\d.]+[KMG]?B/s)", line)
                peers = re.search(r"CN:(\d+)", line)
                if speed:
                    self.stats_label.configure(text=f"Скорость: {speed.group(1)}   |   Пиры: {peers.group(1) if peers else '--'}")
            except:
                pass

        # Ошибки
        if "ERROR" in line or "errorCode" in line or "Failed" in line:
            self.log(f"[❌] {line}")
            self.status_label.configure(text="Ошибка! Смотри лог", text_color="#ef4444")

    def _finish(self):
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✅ Загрузка завершена!")
        self.status_label.configure(text_color="#22c55e")
        self.log("[✅] Загрузка успешно завершена!")
        self._reset()

    def stop_download(self):
        self.is_downloading = False
        if self.process:
            self.process.terminate()
        self.log("[⏹️] Загрузка остановлена пользователем")
        self._reset()

    def _reset(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.is_downloading = False

if __name__ == "__main__":
    app = TorrentGUI()
    app.mainloop()