# import des données
import os, numpy as np, pandas as pd
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 40)

# ── FICHIERS  ────────────────────────────
USERS_PATH = 'users.csv'                # fichier uploadé dans Colab
SPEND_PATH = 'marketing_spend.csv'

OUT_DIR = 'out'; os.makedirs(OUT_DIR, exist_ok=True)
EXT = pd.Timestamp('2026-06-30')                       # extraction date
CH = ['Meta Ads','Google Ads','TikTok Ads','Influencers','Organic','Referral']
PAID = CH[:4]
PRICE_M, PRICE_A, STORE_FEE = 9.99, 59.99, 0.15       # STORE_FEE = hypothèse (absente des données)
