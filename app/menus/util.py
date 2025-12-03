from html.parser import HTMLParser
import os
import re
import textwrap

import os
import time
import random

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

import os
import time
import random

def animate_fire_diagonal():
    # Palet warna api (urutan untuk efek diagonal)
    fire_palette = [
        "\033[31m",   # merah gelap
        "\033[91m",   # merah terang
        "\033[33m",   # oranye
        "\033[93m",   # kuning terang
        "\033[97m",   # putih panas
    ]
    RESET = "\033[0m"

    ascii_art = r"""
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗
████╗  ██║██╔═══██╗██║   ██║██╔══██╗████╗  ██║
██╔██╗ ██║██║   ██║██║   ██║███████║██╔██╗ ██║
██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║
██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║
╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝

███████╗████████╗ ██████╗ ██████╗ ███████╗
██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝
███████╗   ██║   ██║   ██║██████╔╝█████╗
╚════██║   ██║   ██║   ██║██╔══██╗██╔══╝
███████║   ██║   ╚██████╔╝██║  ██║███████╗
╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
"""

    lines = ascii_art.split("\n")

    try:
        frame = 0
        while True:
            clear_terminal()

            for r, line in enumerate(lines):
                colored_line = ""
                for c, char in enumerate(line):
                    if char != " ":
                        # Indeks diagonal berdasarkan posisi + frame
                        idx = (r + c + frame) % len(fire_palette)
                        color = fire_palette[idx]
                        colored_line += f"{color}{char}{RESET}"
                    else:
                        colored_line += " "
                print(colored_line)

            frame += 1
            time.sleep(0.07)

    except KeyboardInterrupt:
        clear_terminal()
        print("Animasi diagonal dihentikan.")

# Jalankan animasi
animate_fire_diagonal()

def pause():
    input("\nPress enter to continue...")

class HTMLToText(HTMLParser):
    def __init__(self, width=80):
        super().__init__()
        self.width = width
        self.result = []
        self.in_li = False

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.in_li = True
        elif tag == "br":
            self.result.append("\n")

    def handle_endtag(self, tag):
        if tag == "li":
            self.in_li = False
            self.result.append("\n")

    def handle_data(self, data):
        text = data.strip()
        if text:
            if self.in_li:
                self.result.append(f"- {text}")
            else:
                self.result.append(text)

    def get_text(self):
        # Join and clean multiple newlines
        text = "".join(self.result)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        # Wrap lines nicely
        return "\n".join(textwrap.wrap(text, width=self.width, replace_whitespace=False))

def display_html(html_text, width=80):
    parser = HTMLToText(width=width)
    parser.feed(html_text)
    return parser.get_text()

def format_quota_byte(quota_byte: int) -> str:
    GB = 1024 ** 3 
    MB = 1024 ** 2
    KB = 1024

    if quota_byte >= GB:
        return f"{quota_byte / GB:.2f} GB"
    elif quota_byte >= MB:
        return f"{quota_byte / MB:.2f} MB"
    elif quota_byte >= KB:
        return f"{quota_byte / KB:.2f} KB"
    else:
        return f"{quota_byte} B"
