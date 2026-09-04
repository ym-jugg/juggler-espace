# -*- coding: utf-8 -*-
# 各機種のスペック定義（BIG/REG獲得枚数、設定1-6のBIG/REG/ぶどう確率）
# 出典: slobase.jp、nana-press.com(ガリぞう独自調査値)、p-town.dmm.com等の公開解析データ、
# および一部はユーザー提供のキャプチャ画像(2026年時点の情報)。
# 全機種 confirmed:True (2026年時点で全機種のBIG/REG/ぶどう確率とも出典を確認済み)。
# 「ネオアイムジャグラーEX」のみ、データ出典が「SアイムジャグラーEX-TP」名義のため
# 同一機種かどうか要再確認（乖離が大きい場合は見直すこと）。
#
# 注意: 2026-09-05の改訂で推定設定の判定は BIG/REG のみを使う方式になったため、
# 'grape' / 'cherry_prob_avg' / 'cherry_payout' は判定には使われていない。
# 将来ぶどう関連の分析を再開する可能性を考えて値自体は残してある。

GRAPE_PAYOUT = 8  # 全機種共通想定（3枚賭け、ぶどう払い出し8枚）
CHERRY_PAYOUT_DEFAULT = 2  # 大半のジャグラー系機種はチェリー払い出し2枚（ミスタージャグラーのみ4枚）
BIG_BET = 3
REPLAY_PROB = 7.3  # リプレイ確率（コイン消費なし）。ジャグラーシリーズでほぼ共通の値

SPECS = {
    'マイジャグラーV': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        # 非重複チェリー確率(設定別、出典同上): 1/38.10,38.10,36.82,35.62,35.62,35.62
        'cherry_prob_avg': (38.10+38.10+36.82+35.62+35.62+35.62)/6,
        # 出典: ガリぞう独自調査値 https://nana-press.com/post/1576232/3
        'settings': [
            {'s':1,'big':273.07,'reg':409.60,'grape':5.90},
            {'s':2,'big':270.81,'reg':385.51,'grape':5.85},
            {'s':3,'big':266.41,'reg':336.08,'grape':5.80},
            {'s':4,'big':254.02,'reg':289.98,'grape':5.78},
            {'s':5,'big':240.06,'reg':268.59,'grape':5.76},
            {'s':6,'big':229.15,'reg':229.15,'grape':5.66},
        ]
    },
    'ネオアイムジャグラーEX': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        'cherry_prob_avg': None,  # 出典記事にチェリー確率の記載なし
        # 出典: ガリぞう独自調査値 https://nana-press.com/post/1576232/3 (「SアイムジャグラーEX-TP」の調査値)
        # 「ネオアイムジャグラーEX」と同一スペックであることをユーザーに確認済み
        'settings': [
            {'s':1,'big':273.07,'reg':439.84,'grape':6.02},
            {'s':2,'big':269.70,'reg':399.61,'grape':6.02},
            {'s':3,'big':269.70,'reg':330.99,'grape':6.02},
            {'s':4,'big':259.04,'reg':315.08,'grape':6.02},
            {'s':5,'big':259.04,'reg':255.00,'grape':6.02},
            {'s':6,'big':255.00,'reg':255.00,'grape':5.78},
        ]
    },
    'ファンキージャグラー2': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        'cherry_prob_avg': 35.62,  # 非重複チェリー確率(全設定共通)
        # 出典: ガリぞう独自調査値 https://nana-press.com/post/1576232/3
        'settings': [
            {'s':1,'big':266.41,'reg':439.84,'grape':5.94},
            {'s':2,'big':259.04,'reg':407.06,'grape':5.92},
            {'s':3,'big':256.00,'reg':366.12,'grape':5.88},
            {'s':4,'big':249.19,'reg':322.84,'grape':5.83},
            {'s':5,'big':240.06,'reg':299.25,'grape':5.76},
            {'s':6,'big':219.92,'reg':262.14,'grape':5.67},
        ]
    },
    'ゴーゴージャグラー3': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        'cherry_prob_avg': None,
        # BIG/REG出典: slobase.jp。ぶどうはKITAC JUGGLER LANDアプリ抽出値(ユーザー提供キャプチャ、ガリぞう氏一部数値引用)
        'settings': [
            {'s':1,'big':264.3,'reg':397.2,'grape':6.25},
            {'s':2,'big':260.1,'reg':362.1,'grape':6.20},
            {'s':3,'big':256.0,'reg':332.7,'grape':6.15},
            {'s':4,'big':249.2,'reg':290.0,'grape':6.07},
            {'s':5,'big':240.1,'reg':255.0,'grape':6.00},
            {'s':6,'big':230.8,'reg':230.8,'grape':5.94},
        ]
    },
    'ジャグラーガールズ': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        'cherry_prob_avg': None,
        # 出典: p-town.dmm.com独自調査値(ユーザー提供キャプチャ)。ぶどうはガリぞうch様引用
        'settings': [
            {'s':1,'big':273.1,'reg':381.0,'grape':5.98},
            {'s':2,'big':270.8,'reg':350.5,'grape':5.98},
            {'s':3,'big':260.1,'reg':316.6,'grape':5.98},
            {'s':4,'big':250.1,'reg':281.3,'grape':5.98},
            {'s':5,'big':243.6,'reg':270.8,'grape':5.88},
            {'s':6,'big':226.0,'reg':252.1,'grape':5.83},
        ]
    },
    'ハッピージャグラーVIII': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        # 通常時非重複チェリー確率(設定別): 1/62.24,62.47,62.95,64.00,64.57,65.34
        'cherry_prob_avg': (62.24+62.47+62.95+64.00+64.57+65.34)/6,
        # 出典: ガリぞう独自調査値 https://nana-press.com/post/1576232/3
        'settings': [
            {'s':1,'big':273.07,'reg':397.19,'grape':6.04},
            {'s':2,'big':270.81,'reg':362.08,'grape':6.01},
            {'s':3,'big':263.20,'reg':332.67,'grape':5.98},
            {'s':4,'big':254.02,'reg':300.62,'grape':5.84},
            {'s':5,'big':239.18,'reg':273.07,'grape':5.81},
            {'s':6,'big':225.99,'reg':256.00,'grape':5.79},
        ]
    },
    'ウルトラミラクルジャグラー': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 2,
        'cherry_prob_avg': None,
        # 出典: p-town.dmm.com独自調査値(BIG/REG)+ガリぞう調べ逆算ぶどう確率(ユーザー提供キャプチャ)
        'settings': [
            {'s':1,'big':267.5,'reg':425.6,'grape':5.93},
            {'s':2,'big':261.1,'reg':402.1,'grape':5.93},
            {'s':3,'big':256.0,'reg':350.5,'grape':5.93},
            {'s':4,'big':242.7,'reg':322.8,'grape':5.93},
            {'s':5,'big':233.2,'reg':297.9,'grape':5.87},
            {'s':6,'big':216.3,'reg':277.7,'grape':5.81},
        ]
    },
    'ミスタージャグラー': {
        'big_payout': 240, 'reg_payout': 96, 'confirmed': True,
        'cherry_payout': 4,  # ユーザー提供情報: ミスタージャグラーのみチェリー払い出し4枚
        'cherry_prob_avg': None,
        # 出典: p-town.dmm.com独自調査値(BIG/REG)+逆算ぶどう確率(ユーザー提供キャプチャ)
        'settings': [
            {'s':1,'big':268.6,'reg':374.5,'grape':6.29},
            {'s':2,'big':267.5,'reg':354.2,'grape':6.22},
            {'s':3,'big':260.1,'reg':331.0,'grape':6.15},
            {'s':4,'big':249.2,'reg':291.3,'grape':6.09},
            {'s':5,'big':240.9,'reg':257.0,'grape':6.02},
            {'s':6,'big':237.4,'reg':237.4,'grape':5.96},
        ]
    },
}
