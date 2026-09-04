# -*- coding: utf-8 -*-
"""
ジャグラーホールデータの推定設定・信頼度・備考を計算するスクリプト。

使い方:
  python compute.py raw.csv output.csv

raw.csv の想定列(ヘッダー行あり、UTF-8):
  収集日,機種名,台番号,G数,差枚,BB,RB

output.csv には以下の列を出力する:
  収集日,機種名,台番号,G数,差枚,BB,RB,BB確率,RB確率,合成確率,推定設定,信頼度,備考

■ 推定設定の判定ロジック(2026-09-05 改訂)
BIG回数・REG回数をそれぞれ二項分布とみなした最尤推定のみで判定する。
  LL(設定s) = bb*ln(p_big) + (G-bb)*ln(1-p_big) + rb*ln(p_reg) + (G-rb)*ln(1-p_reg)
最大の対数尤度を与える設定を推定設定とする(二項係数は設定間で共通のため省略可)。

- 合成確率での比較、ぶどう逆算、差枚由来の項はいずれも判定に使わない。
  REGの方がBIGより設定間の確率差が大きく判別力が高いため、恣意的な重み付けをせず
  尤度計算で自動的に重みが決まる方式とする。
- 合成確率は表示用の指標としてのみ算出する(判定には不使用)。

■ 信頼度
G数(サンプルサイズ)と、1位設定と2位設定の対数尤度差ΔLLから「高/中/低」を判定する。
ΔLLは尤度比の対数で、ΔLL=1.0 は「1位が2位より約2.7倍もっともらしい」ことを意味する。
閾値 DELTA_LL_THRESHOLD=0.09 は、旧ロジック(合成確率60%+ぶどう40%)を全期間に一律適用した
場合の高/中/低の構成比(30.3/53.0/16.7%)に最も近くなるよう較正した値。
【注意】ΔLL=0.09 は尤度比にして約1.09倍にすぎず、統計的に強い根拠ではない。
これは「信頼度中以上」を条件に使っている既存の予想ロジック(台レベル昇格基準・的中判定)の
意味を変えないための互換性優先の設定である。統計的な厳密さを優先するなら
ΔLL>1.0(尤度比2.7倍)程度が妥当だが、その場合「高」は全体の約1%に激減し、
既存の判定基準を併せて見直す必要がある。

機種別スペック(BIG/REG確率)は ../references/specs.py の SPECS を参照する。
"""
import csv
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references'))
from specs import SPECS

# 信頼度判定の対数尤度差しきい値(較正値。詳細は上部docstring参照)
DELTA_LL_THRESHOLD = 0.09


def gousei_prob(big, reg):
    return 1.0 / (1.0 / big + 1.0 / reg)


def log_likelihood(g, bb, rb, big_denom, reg_denom):
    """BIG/REGをそれぞれ二項分布とみなした対数尤度(二項係数は省略)。"""
    p_big = 1.0 / big_denom
    p_reg = 1.0 / reg_denom
    ll = 0.0
    ll += bb * math.log(p_big) + (g - bb) * math.log1p(-p_big)
    ll += rb * math.log(p_reg) + (g - rb) * math.log1p(-p_reg)
    return ll


def estimate(machine, g, sa, bb, rb):
    if machine not in SPECS:
        raise ValueError(
            f"未対応の機種です: {machine}。references/specs.py の SPECS に "
            f"BIG/REG払出枚数と設定別確率テーブルを追加してください。"
        )
    spec = SPECS[machine]

    total_bonus = bb + rb
    gousei_actual = g / total_bonus if total_bonus > 0 else None
    bb_actual = g / bb if bb > 0 else None
    rb_actual = g / rb if rb > 0 else None

    # --- 推定設定: BIG/REGの二項尤度のみで判定 ---
    scored = []
    for row in spec['settings']:
        ll = log_likelihood(g, bb, rb, row['big'], row['reg'])
        scored.append((ll, row['s']))
    scored.sort(reverse=True)          # 対数尤度が大きい順
    best_setting = scored[0][1]
    delta_ll = scored[0][0] - scored[1][0] if len(scored) > 1 else float('inf')

    # --- 信頼度 ---
    if g < 3000:
        conf = '低'
    elif g < 6000:
        conf = '中' if delta_ll > DELTA_LL_THRESHOLD else '低'
    else:
        conf = '高' if delta_ll > DELTA_LL_THRESHOLD else '中'

    # --- 備考 ---
    notes = []
    if g < 2000:
        notes.append('サンプルG数少なく参考程度')
    if rb_actual and bb_actual and rb_actual < bb_actual:
        notes.append('REG優勢で高設定示唆')
    if not spec['confirmed']:
        notes.append('機種スペックは一部近似値')
    s4 = spec['settings'][3]
    if sa > 0 and gousei_actual and gousei_actual < gousei_prob(s4['big'], s4['reg']):
        notes.append('差枚プラスかつ合成確率良好')
    remark = '。'.join(notes) if notes else '特記事項なし'

    return {
        'gousei_actual': gousei_actual,
        'bb_actual': bb_actual,
        'rb_actual': rb_actual,
        'best_setting': best_setting,
        'delta_ll': delta_ll,
        'confidence': conf,
        'remark': remark,
    }


def fmt_prob(x):
    return '' if x is None else f'1/{x:.1f}'


def main():
    if len(sys.argv) != 3:
        print('使い方: python compute.py raw.csv output.csv')
        sys.exit(1)
    in_path, out_path = sys.argv[1], sys.argv[2]

    header_out = ['収集日', '機種名', '台番号', 'G数', '差枚', 'BB', 'RB', 'BB確率', 'RB確率',
                  '合成確率', '推定設定', '信頼度', '備考']
    rows_out = []
    with open(in_path, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            g = int(row['G数']); sa = int(row['差枚'])
            bb = int(row['BB']); rb = int(row['RB'])
            r = estimate(row['機種名'], g, sa, bb, rb)
            rows_out.append([
                row['収集日'], row['機種名'], row['台番号'], g, sa, bb, rb,
                fmt_prob(r['bb_actual']), fmt_prob(r['rb_actual']), fmt_prob(r['gousei_actual']),
                r['best_setting'], r['confidence'], r['remark']
            ])

    with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(header_out)
        w.writerows(rows_out)
    print(f'{len(rows_out)}行を書き出しました: {out_path}')


if __name__ == '__main__':
    main()
