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

#----------CLEANING PART-------------------------------------------------

LOG = []
def log(rule, n, action, remaining): LOG.append(dict(rule=rule, rows_affected=int(n), action=action, rows_remaining=int(remaining)))

raw = pd.read_csv(USERS_PATH, dtype=str)
u = raw.copy(); log('Raw users.csv', len(u), 'loaded as text', len(u))

n = u.duplicated().sum(); u = u.drop_duplicates()
log('Exact duplicate rows', n, 'dropped, first kept', len(u))
log('Duplicate user_id with conflicting content', u.user_id.duplicated().sum(), 'none found', len(u))

m = u.user_id.str.startswith('QA_') | (u.channel == 'internal'); n = m.sum(); u = u[~m]
log("Internal/test accounts (user_id 'QA_', channel 'internal')", n, 'removed', len(u))

n_slash = u.signup_date.str.contains('/', na=False).sum()
def parse_date(x):                                          # yyyy-mm-dd first, then dd/mm/yyyy (day part >12 occurs, month part never)
    return pd.to_datetime(x, format='%Y-%m-%d', errors='coerce').fillna(pd.to_datetime(x, format='%d/%m/%Y', errors='coerce'))
for c in ['signup_date','trial_start_date','subscription_start_date','subscription_end_date']: u[c] = parse_date(u[c])
log('Mixed date format dd/mm/yyyy in signup_date', n_slash, 'parsed day-first, kept', len(u))

bad = (u.signup_date < '2025-01-01') | (u.signup_date > EXT); n = bad.sum(); u = u[~bad]
log('Impossible signup_date (1900, 1970, 2099)', n, 'removed (no cohort possible)', len(u))

chmap = {'tiktok':'TikTok Ads','TikTok Ads':'TikTok Ads','meta_ads':'Meta Ads','Facebook Ads':'Meta Ads','Meta Ads':'Meta Ads',
         'google_ads':'Google Ads','Google Ads':'Google Ads','Organic':'Organic','Referral':'Referral','Influencers':'Influencers'}
n = (~u.channel.isin(['Meta Ads','Google Ads','TikTok Ads','Influencers','Organic','Referral'])).sum()
u['channel'] = u.channel.map(chmap)
assert u.channel.isin(CH).all()
log("Inconsistent channel labels ('tiktok','meta_ads','Facebook Ads','google_ads')", n, 'harmonised to 6 channels', len(u))

n = u.country.isna().sum(); u['country'] = u.country.fillna('Unknown')
log('Missing country', n, "kept as 'Unknown', not imputed", len(u))

u['activated_d7'] = u.activated_d7.astype(int)
viol = ((u.trial_start_date < u.signup_date).sum() + (u.subscription_start_date < u.trial_start_date).sum()
        + (u.subscription_end_date <= u.subscription_start_date).sum()
        + (u.subscription_start_date.notna() & u.trial_start_date.isna()).sum()
        + (u.plan.notna() & u.subscription_start_date.isna()).sum()
        + (u.subscription_end_date.notna() & u.subscription_start_date.isna()).sum()
        + (u[['trial_start_date','subscription_start_date','subscription_end_date']] > EXT).any(axis=1).sum())
log('Chronology checks (trial<signup, sub<trial, end<=start, plan/end without sub, dates after extraction)', viol, 'violations remaining', len(u))

u['cohort'] = u.signup_date.dt.to_period('M').dt.to_timestamp()
u['paid'] = u.subscription_start_date.notna(); u['has_trial'] = u.trial_start_date.notna(); u['ended'] = u.subscription_end_date.notna()

# marketing spend
sp = pd.read_csv(SPEND_PATH); sp['month'] = pd.to_datetime(sp.month)
cleaning_log = pd.DataFrame(LOG); cleaning_log.to_csv(f'{OUT_DIR}/cleaning_log.csv', index=False)
print(cleaning_log.to_string(index=False)); print(f'\nClean users: {len(u):,} ({len(raw)-len(u):,} rows removed)')
