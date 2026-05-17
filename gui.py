#!/usr/bin/env python3
"""
Torrent- v1.1 - Полноценный GUI на CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TorrentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Torrent- v1.1 | Персональный Торрент Клиент")
        self.geometry("720x550")
        self.resizable(False, False)

        self.download_path = ctk.StringVar(value=str(Path.home() / "Downloads"))
        self.process = None
        self.is_downloading = False

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#1a1a2e")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="🚀 Torrent- v1.1", font=ctk.CTkFont(size=26, weight="bold"), text_color="#00d4ff").pack(pady=12)

        # Source
        frame = ctk.CTkFrame(self)
        frame.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(frame, text="Magnet или .torrent файл", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=12, pady=4)

        entry_frame = ctk.CTkFrame(frame, fg_color="transparent")
        entry_frame.pack(fill="x", padx=10)

        self.source_entry = ctk.CTkEntry(entry_frame, placeholder_text="Вставьте magnet:ссылку...", width=480)
        self.source_entry.pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(entry_frame, text="📁 .torrent", command=self.browse_torrent, width=90).pack(side="left", padx=3)
        ctk.CTkButton(entry_frame, text="📋 Из буфера", command=self.paste_clipboard, width=100).pack(side="left")

        # Path
        path_frame = ctk.CTkFrame(self)
        path_frame.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(path_frame, text="Папка сохранения", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=12, pady=4)

        path_row = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_row.pack(fill="x", padx=10)
        self.path_entry = ctk.CTkEntry(path_row, textvariable=self.download_path, width=450)
        self.path_entry.pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(path_row, text="📂", command=self.browse_folder, width=50).pack(side="left")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=12)

        self.start_btn = ctk.CTkButton(btn_frame, text="▶️ Начать загрузку", command=self.start_download,
                                     fg_color="#00c853", hover_color="#00a844", width=220, height=42, font=ctk.CTkFont(size=15, weight="bold"))
        self.start_btn.pack(side="left", padx=8)

        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹️ Остановить", command=self.stop_download,
                                    fg_color="#ff1744", hover_color="#d50000", width=140, height=42, state="disabled")
        self.stop_btn.pack(side="left", padx=8)

        # Progress
        prog_frame = ctk.CTkFrame(self)
        prog_frame.pack(pady=8, padx=20, fill="x")

        self.progress_label = ctk.CTkLabel(prog_frame, text="Готов к работе", font=ctk.CTkFont(size=14))
        self.progress_label.pack(pady=6)

        self.progress_bar = ctk.CTkProgressBar(prog_frame, width=580, height=22, progress_color="#00d4ff")
        self.progress_bar.pack(pady=4)
        self.progress_bar.set(0)

        self.stats_label = ctk.CTkLabel(prog_frame, text="Скорость: --  |  Пиры: --  |  Осталось: --", font=ctk.CTkFont(size=12))
        self.stats_label.pack(pady=4)

        self.status_label = ctk.CTkLabel(self, text="Введите ссылку или выберите файл", text_color="gray60")
        self.status_label.pack(pady=8)

    def browse_torrent(self):
        path = filedialog.askopenfilename(filetypes=[("Torrent", "*.torrent")])
        if path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, path)

    def paste_clipboard(self):
        try:
            text = self.clipboard_get()
            if text.startswith("magnet:"):
                self.source_entry.delete(0, "end")
                self.source_entry.insert(0, text)
        except:
            pass

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)

    def start_download(self):
        src = self.source_entry.get().strip()
        if not src:
            messagebox.showerror("Ошибка", "Введите magnet или выберите .torrent")
            return

        save = self.download_path.get()
        os.makedirs(save, exist_ok=True)

        self.is_downloading = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Загрузка начата...")
        self.status_label.configure(text="Работает...", text_color="white")

        threading.Thread(target=self._run_aria, args=(src, save), daemon=True).start()

    def _run_aria(self, src, save):
        cmd = ["aria2c", src, f"--dir={save}", "--seed-time=0", "--max-connection-per-server=16", "--split=16", "--continue=true", "--summary-interval=1"]
        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=0x08000000 if os.name=='nt' else 0)
            for line in iter(self.process.stdout.readline, ''):
                if not self.is_downloading: break
                self._parse_line(line)
            if self.is_downloading:
                self.after(0, self._finish)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
            self.after(0, self._reset)

    def _parse_line(self, line):
        if "%" in line:
            try:
                p = float(line.split("%")[0].split("(")[-1])
                self.after(0, lambda: self.progress_bar.set(p/100))
                self.after(0, lambda: self.progress_label.configure(text=f"Загрузка: {p:.1f}%"))
            except: pass
        if "DL:" in line:
            try:
                spd = line.split("DL:")[1].split()[0]
                self.after(0, lambda: self.stats_label.configure(text=f"Скорость: {spd}  |  Пиры: --"))
            except: pass

    def _finish(self):
        self.progress_bar.set(1)
        self.progress_label.configure(text="✅ Завершено!")
        self.status_label.configure(text_color="#00ff9f")
        self._reset()

    def stop_download(self):
        self.is_downloading = False
        if self.process: self.process.terminate()
        self._reset()
        self.progress_label.configure(text="Остановлено")

    def _reset(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.is_downloading = False

if __name__ == "__main__":
    app = TorrentGUI()
    app.mainloop()