# ============================================
# FIX IMPORT PATH (WAJIB untuk Termux)
# ============================================
import sys, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ============================================
# IMPORTS
# ============================================
from dotenv import load_dotenv
load_dotenv()

# Pastikan modul git ditemukan
try:
    from app.service.git import check_for_updates
except Exception as e:
    print("⚠️  Tidak dapat mengimport check_for_updates:", e)
    print("   Program tetap berjalan tanpa pengecekan update.\n")
    def check_for_updates():
        return False

import json
from datetime import datetime

# ======= WARNA ========
from colorama import init, Fore, Style
init(autoreset=True)
# ======================

from app.menus.util import clear_screen, pause
from app.client.engsel import get_balance, get_tiering_info
from app.client.famplan import validate_msisdn
from app.menus.payment import show_transaction_history
from app.service.auth import AuthInstance
from app.menus.bookmark import show_bookmark_menu
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family, show_package_details
from app.menus.hot import show_hot_menu, show_hot_menu2
from app.service.sentry import enter_sentry_mode
from app.menus.purchase import purchase_by_family
from app.menus.famplan import show_family_info
from app.menus.circle import show_circle_info
from app.menus.notification import show_notification_menu
from app.menus.store.segments import show_store_segments_menu
from app.menus.store.search import show_family_list_menu, show_store_packages_menu
from app.menus.store.redemables import show_redeemables_menu
from app.client.registration import dukcapil
