# 三重県の試算の値の当て方（2026-11-11）。_calc.py の PLAN はこの出力。作り直すときは python3 -B data/area/mie/_assign.py
# 滋賀県の _assign.py と同じ当て方（規模の小さい順に、空いている小さい値から当てる）。余りは ×4 を4で割って 2（端数 .50）
import sys, importlib.util
from decimal import Decimal as D
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("g","/home/user/ai-bpo-wp/data/area/mie/_calc.py")
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
hu,mu=g.used_values()
# (city, slug, ind, sub, keys, size, task)。業種は stats.md の「市町ごとの主要産業の候補」の (B)
ROWS=[
("津市","tsu","情報通信業","ソフトウェア業（企業・団体向けの業務システムの受託開発・保守）",{"ソフトウェア受託開発","業務システム","情報サービス"},68,
 "顧客からの問い合わせ・不具合連絡への一次回答の下書きと、打合せ記録の要約、仕様書・提案書の下書き"),
("四日市市","yokkaichi","建設業","設備工事業（工場・プラントの電気・配管の設備工事）",{"設備工事","電気工事","管工事"},86,
 "工事日報・安全書類（作業計画書・KY記録）の取りまとめと、元請・工場の担当者への工程・作業の連絡文、見積書の下書き"),
("伊勢市","ise","製造業","食料品（土産の菓子・餅の製造と販売）",{"菓子","食料品","土産菓子"},58,
 "土産物店・通販の取引先からの賞味期限・アレルゲン・在庫の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ"),
("松阪市","matsusaka","運輸業・郵便業","道路貨物運送（食品・日用品の店舗への配送）",{"運送","道路貨物運送"},72,
 "荷主からの配送状況・納品時刻の問い合わせへの回答と、配車の連絡、運転日報・点呼記録の取りまとめ"),
("桑名市","kuwana","製造業","鉄鋼（鋳物の製造）",{"鋳物","鉄鋼","鋳造"},54,
 "取引先からの図面・納期・材質の問い合わせへの回答と、検査記録・ミルシートの取りまとめ、不具合の報告書の下書き"),
("鈴鹿市","suzuka","製造業","輸送用機械（自動車部品のプレス加工・溶接）",{"自動車部品","輸送用機械","プレス加工"},92,
 "取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ"),
("名張市","nabari","製造業","生産用機械（工場の省力化設備・治具の設計製作）",{"生産用機械","省力化設備","治具"},40,
 "顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き"),
("尾鷲市","owase","製造業","食料品（干物・練り製品などの水産加工）",{"水産加工","食料品","水産食料品"},28,
 "量販店・通販の取引先からの原材料・産地・賞味期限の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ"),
("亀山市","kameyama","製造業","プラスチック製品（樹脂部品の射出成形・組立）",{"プラスチック製品","射出成形"},78,
 "取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き"),
("鳥羽市","toba","宿泊・飲食サービス業","海辺の旅館（団体・家族客の宿泊と食事）",{"旅館","宿泊"},48,
 "予約サイト・メールの問い合わせへの返信の下書きと、送迎・食事の手配の連絡、館内案内の多言語の文の作成"),
("熊野市","kumano-city","医療・福祉","特別養護老人ホーム（デイサービスを併設）",{"介護","特別養護老人ホーム"},52,
 "介護記録の要約と、家族への連絡文・お便り、ケアマネジャーへの報告書・会議録の作成"),
("いなべ市","inabe","製造業","窯業・土石（コンクリート二次製品の製造）",{"窯業・土石","コンクリート製品"},39,
 "建設会社・商社の取引先からの規格・納期・数量の問い合わせへの回答と、見積書・納品書の作成、製造・検査の記録の取りまとめ"),
("志摩市","shima","宿泊・飲食サービス業","リゾートホテル（宿泊・宴会・婚礼）",{"ホテル","宿泊"},96,
 "予約・宴会の問い合わせへの返信の下書きと、宴会・婚礼の打合せ記録の要約、館内案内・メニューの多言語の文の作成"),
("伊賀市","iga","製造業","金属製品（機械部品の切削加工）",{"金属製品","切削加工","機械部品"},62,
 "取引先からの図面・納期の問い合わせへの回答と、見積書の作成、検査記録・作業日報の取りまとめ"),
("木曽岬町","kisosaki","運輸業・郵便業","道路貨物運送（港の輸入貨物・工場の製品の輸送）",{"運送","道路貨物運送"},36,
 "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計"),
("東員町","toin","製造業","生産用機械（工場の自動化設備・搬送装置の製作）",{"生産用機械","自動化設備","搬送装置"},30,
 "顧客との仕様の打合せ記録の要約と、見積書・取扱説明書の下書き、設計変更の連絡書の作成"),
("菰野町","komono","製造業","金属製品（板金・溶接による部品の製造）",{"金属製品","板金","溶接"},46,
 "取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ"),
("朝日町","asahi-town","製造業","金属製品（めっき・表面処理の加工）",{"金属製品","めっき","表面処理"},26,
 "取引先からの処理の仕様・納期の問い合わせへの回答と、検査成績書・作業記録の取りまとめ、見積書の作成"),
("川越町","kawagoe-town","運輸業・郵便業","倉庫業（港湾地区の工場の部品・製品の保管と配送）",{"倉庫業","運輸"},59,
 "荷主からの在庫・入出庫の問い合わせへの回答と、入出庫の記録・在庫報告の作成、配送業者への手配の連絡"),
("多気町","taki","製造業","電気機械（電子機器・制御機器の組立）",{"電気機械","電子機器","組立"},34,
 "取引先からの仕様・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ、不具合の報告書の下書き"),
("明和町","meiwa","卸売業・小売業","米穀の卸売・小売（米の精米・配達と通販）",{"米穀","卸売","小売"},22,
 "飲食店・個人客からの在庫・配達・品種の問い合わせへの回答と、商品の説明文、注文と配達の記録の取りまとめ"),
("大台町","odai","製造業","木材・木製品（製材・プレカット）",{"木材・木製品","製材","プレカット"},20,
 "工務店からの見積・納期・寸法の問い合わせへの回答と、加工指示書・出荷の記録の取りまとめ"),
("玉城町","tamaki","運輸業・郵便業","道路貨物運送（工場の部品・製品の輸送）",{"運送","道路貨物運送"},32,
 "荷主からの配送状況の問い合わせへの回答と、配車の連絡、運行の記録・点呼記録の取りまとめ"),
("度会町","watarai","製造業","製茶（伊勢茶の荒茶・仕上げ茶の製造と販売）",{"製茶","茶","飲料"},18,
 "問屋・小売店・通販の取引先からの在庫・産地・品質の問い合わせへの回答と、商品の説明文、製造の記録の取りまとめ"),
("大紀町","taiki","医療・福祉","通所介護・訪問介護の事業所",{"介護","通所介護","訪問介護"},24,
 "介護記録の要約と、家族への連絡文、ケアマネジャーへの報告書・サービス担当者会議の記録の作成"),
("南伊勢町","minamiise","卸売業・小売業","水産物の卸売（鮮魚・養殖魚の卸と通販）",{"卸売","水産物卸","鮮魚"},16,
 "飲食店・量販店の取引先からの入荷・規格・価格の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ"),
("紀北町","kihoku","製造業","家具・装備品（ヒノキの木工品・建具の製造）",{"家具・装備品","木工","建具"},23,
 "工務店・小売店・通販の取引先からの見積・納期・仕様の問い合わせへの回答と、商品の説明文、製作の記録の取りまとめ"),
("御浜町","mihama-town-mie","製造業","食料品（みかんの加工品＝ジュース・ゼリーの製造）",{"果実加工","食料品","飲料"},27,
 "通販・土産物店の取引先からの原材料・賞味期限・在庫の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ"),
("紀宝町","kiho","建設業","総合工事業（土木・道路の工事）",{"土木","総合工事業","建設"},38,
 "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理"),
]
HMAX=D(sys.argv[1] if len(sys.argv)>1 else "44")
# 規模の幅: ROWS の規模を下限にし、SMAX（市町の業種の従業者で上限を決めた値）まで広げてよい。小さい町は小さい時間・金額が使い切られているため（奈良・和歌山と同じ）
SMAX={"尾鷲市":44,"木曽岬町":48,"東員町":44,"朝日町":40,"多気町":48,"明和町":40,"大台町":36,"玉城町":46,"度会町":34,"大紀町":42,"南伊勢町":38,"紀北町":40,"御浜町":42,"紀宝町":50,"いなべ市":56,"名張市":56,"菰野町":60,"鳥羽市":64}
cands={}
for r in ROWS:
    city,slug,ind,sub,keys,size,task=r; c={}
    for sz in range(size, SMAX.get(city,size)+1):
        for n in range(max(4,int(sz*0.2)), int(sz*0.9)+1):
            hrs=D("20")
            while hrs<=HMAX:
                h=D(n)*hrs*D("0.25")
                if (h*4)%1==0 and int(h*4)%4==2 and h not in hu:
                    yen=h*g.RATE[ind]; m=g.man(yen)
                    if m not in mu and g.border_ok(yen):
                        k=(h,m)
                        sc=abs(n/sz-0.5)*2+abs(float(hrs)-30)/15+(sz-size)/size*2
                        if k not in c or sc<c[k][3]: c[k]=(sz,n,hrs,sc)
                hrs+=D("0.25")
    # 並べ方: 対象人数が従業員の半分に近い・業務量が30時間に近い・規模が下限に近い・時間が小さいものを先に
    def score(x, size=size):
        sz,hrs,h,n,m=x
        return abs(n/sz-0.5)*2 + abs(float(hrs)-30)/15 + (sz-size)/size*2 + float(h)/400
    cands[city]=sorted(((v[0],v[2],k[0],v[1],k[1]) for k,v in c.items()), key=score)
res={}; used_h=set(); used_m=set(); used_s=set()
def ok(x): return x[2] not in used_h and x[4] not in used_m and x[0] not in used_s
def solve(rest):
    if not rest: return True
    rest=sorted(rest,key=lambda city:sum(1 for x in cands[city] if ok(x)))
    city=rest[0]
    for x in cands[city]:
        if not ok(x): continue
        sz,hrs,h,n,m=x
        used_h.add(h); used_m.add(m); used_s.add(sz); res[city]=x
        if solve(rest[1:]): return True
        used_h.discard(h); used_m.discard(m); used_s.discard(sz); del res[city]
    return False
sys.setrecursionlimit(10000)
print("解けた" if solve([r[0] for r in ROWS]) else "解けない", {k:len(v) for k,v in cands.items() if len(v)<30})
# 改善: 1行ずつ、空いている・より良い候補に移す（候補は良い順に並んでいる）。さらに2行の入れ替えも試す
improved=True
while improved:
    improved=False
    for city in list(res):
        cur=res[city]; used_h.discard(cur[2]); used_m.discard(cur[4]); used_s.discard(cur[0])
        for x in cands[city]:
            if x==cur: break
            if ok(x):
                cur=x; improved=True; break
        res[city]=cur; used_h.add(cur[2]); used_m.add(cur[4]); used_s.add(cur[0])
    cities=list(res)
    for a in cities:
        for b in cities:
            if a>=b: continue
            xa,xb=res[a],res[b]
            for v in (xa,xb): used_h.discard(v[2]); used_m.discard(v[4]); used_s.discard(v[0])
            ia=cands[a].index(xa); ib=cands[b].index(xb); done=False
            for na in cands[a][:ia]:
                if not ok(na): continue
                used_h.add(na[2]); used_m.add(na[4]); used_s.add(na[0])
                for nb in cands[b][:ib+1]:
                    if ok(nb):
                        res[a]=na; res[b]=nb; used_h.add(nb[2]); used_m.add(nb[4]); used_s.add(nb[0]); done=improved=True; break
                if done: break
                used_h.discard(na[2]); used_m.discard(na[4]); used_s.discard(na[0])
            if not done:
                for v in (xa,xb): used_h.add(v[2]); used_m.add(v[4]); used_s.add(v[0])
out=[]
for r in ROWS:
    if r[0] not in res: print("NO",r[0]); continue
    sz,hrs,h,n,m=res[r[0]]
    print(f"{r[0]} {r[2]} {sz}名（下限{r[5]}） {n}人×{hrs}h → {h}h {m}万")
    out.append(r[:5]+(sz,r[6],n,float(hrs)))
open("/tmp/claude-0/-home-user-ai-bpo-wp/d8586234-7704-5689-9cb0-8512468a2efc/scratchpad/calc/plan.txt","w").write("PLAN = [\n"+"".join(f"    ({r[0]!r}, {r[1]!r}, {r[2]!r}, {r[3]!r}, {set(sorted(r[4]))!r}, {r[5]},\n     {r[6]!r}, {r[7]}, {r[8]}),\n" for r in out)+"]\n")
