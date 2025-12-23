import streamlit as st
import pandas as pd
import requests
import unicodedata

# --- ページ設定 ---
st.set_page_config(page_title="AIプロンプト製造機", page_icon="🚀", layout="wide")

# --- セッション状態の初期化 ---
if 'mode' not in st.session_state:
    st.session_state.mode = "📈 売買・エントリー"
if 'status' not in st.session_state:
    st.session_state.status = "未保有（これから買いたい）" # ポジションの初期値
if 'scraped_text' not in st.session_state:
    st.session_state.scraped_text = ""

# --- 関数：全角→半角変換 ---
def to_half_width(text):
    if not text:
        return ""
    # 英数字と記号を半角に正規化
    return unicodedata.normalize('NFKC', text)

# --- 関数：モード切替 ---
def set_mode(new_mode):
    st.session_state.mode = new_mode

# --- 関数：ポジション切替 ---
def set_status(new_status):
    st.session_state.status = new_status

# --- 関数：株ドラゴン取得 ---
def fetch_kabudragon_data(url_type):
    urls = {
        "値上がり率ランキング": "https://www.kabudragon.com/ranking/up/",
        "値下がり率ランキング": "https://www.kabudragon.com/ranking/down/",
        "ストップ高": "https://www.kabudragon.com/ranking/stopup/",
        "ストップ安": "https://www.kabudragon.com/ranking/stopdown/",
        "窓開け（上昇）": "https://www.kabudragon.com/ranking/madoakeup/",
        "窓開け（下落）": "https://www.kabudragon.com/ranking/madoakedown/",
        "ゴールデンクロス": "https://www.kabudragon.com/ranking/golden/",
        "5日間暴落": "https://www.kabudragon.com/ranking/5down/"
    }
    target_url = urls.get(url_type)
    if not target_url: return "URLエラー"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(target_url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        dfs = pd.read_html(response.text)
        if dfs:
            return f"### 参照データ：{url_type}\n\n{dfs[0].head(20).to_markdown(index=False)}"
        return "データなし"
    except Exception as e:
        return f"取得失敗: {e}"

# --- キャラクター定義（省略なしで全掲載） ---
chars_entry = [
    "順張り隊長（上昇トレンドの初動しか狙わない）",
    "逆張り名人（暴落のリバウンド狙い専門）",
    "チャート職人（移動平均線とローソク足の形が全て）",
    "材料スナイパー（好材料が出た瞬間の飛び乗り専門）",
    "テーマ株レーダー（国策・流行り廃りを先読みする）",
    "需給探偵（機関の空売りと信用買い残を読み解く）",
    "ブレイクアウトハンター（高値更新の瞬間だけ狙う）",
    "押し目待ちの達人（調整局面まで絶対手を出さない）",
    "低位株ギャンブラー（一発逆転の大相場狙い）",
    "IPOセカンダリー専門家（上場直後の値動き攻略）",
    "出来高ウォッチャー（バイイングクライマックスを見抜く）",
    "窓埋めハンター（開いた窓は必ず閉まると信じる）",
    "V字回復信者（底打ちからの急騰しか見ない）",
    "ボックス相場師（レンジ上限売り・下限買いの機械）",
    "アルゴ追従くん（高速取引の癖を読み取る）",
    "セクターローテ監視員（資金が流れてくる業種を先回り）",
    "PTS夜間取引の住人（明日の気配を誰よりも早く読む）"
]
chars_manage = [
    "リスク管理官（損切りライン未設定なら即却下）",
    "資金管理マネージャー（破産しないロット数を計算する）",
    "分割利確コーチ（頭と尻尾はくれてやる精神）",
    "高値掴み防止係（「本当にそこでいいの？」と止める）",
    "ポジポジ病治療医（無駄なエントリーを厳しく叱る）",
    "メンタル守護神（恐怖と欲望をコントロールする）",
    "初心者保護官（難しい専門用語を使わず導く）",
    "ルール厳守の鬼軍曹（感情による売買を許さない）",
    "建玉操作の魔術師（うねり取り・分割売買のプロ）",
    "相場ノート添削係（負けたトレードから反省点を抽出）",
    "トレーリングストップ使い（利益を極限まで伸ばす）",
    "ピラミッティング建築家（増し玉で利益を最大化）",
    "ドローダウン抑制係（資産曲線を滑らかに保つ）",
    "アセットアロケーション調整役（現金比率うるさい）",
    "損出し・節税アドバイザー（年末の損失確定を提案）"
]
chars_analysis = [
    "決算職人（決算短信と補足資料を隅々まで読む）",
    "グロース鑑定士（PSRと成長率で将来株価を弾く）",
    "バリュー査定士（解散価値・PBR1倍割れを許さない）",
    "配当・優待ガチ勢（利回りと権利落ち日の戦略家）",
    "IR翻訳マン（経営者のポエムを実務翻訳する）",
    "中期経営計画の査定員（絵に描いた餅か本気か見抜く）",
    "セクター分析官（半導体・銀行など循環物色を読む）",
    "円安・円高メリット判定員（為替感応度を分析）",
    "機関投資家のプロファイラー（大口の手口を推測）",
    "上級者専用ツッコミ役（「その前提、甘くない？」）",
    "キャッシュフロー探偵（営業CFの推移しか信じない）",
    "含み資産ハンター（不動産や保有株の価値を暴く）",
    "経済の堀（Moat）鑑定士（独占的強みがあるか見る）",
    "インサイダー監視員（役員の売買動向をチェック）",
    "貸借倍率ウォッチャー（踏み上げ相場を予知する）",
    "季節性アノマリー研究家（「セルインメイ」等を考慮）",
    "マクロ経済リンカー（金利と株価の相関を説く）"
]
chars_emergency = [
    "暴落サバイバー（セリクラ判定と生存戦略のプロ）",
    "決算シーズン警戒役（跨ぐべきか降りるべきかの審判）",
    "ショック安専門医（パニック売りの中でお宝を探す）",
    "増資・悪材料の解説員（希薄化懸念と今後の展開を読む）",
    "地合い番長（日経平均・マザーズの空気だけ読む）",
    "有事の金・原油番人（コモディティ関連の専門家）",
    "ブラックスワン理論家（想定外の事態への対処）",
    "ストップ安スナイパー（剥がれた瞬間を狙う）",
    "物言う株主フォロワー（アクティビストの思惑を読む）"
]

# --- 質問テンプレート ---
q_time_horizon = [
    "【短中期】1ヶ月〜3ヶ月の見通しと戦略は？",
    "【中期】3ヶ月〜半年の株価推移シナリオは？",
    "【中長期】半年〜1年のターゲット株価は？",
    "【長期】1年〜3年で持っておく価値はある？",
    "【超長期】3年以上のガチホ（長期保有）目線でどう？"
]
q_entry_short = [
    "この株、デイトレ目線で今入っていい？",
    "明日の寄り付きは「買い」？それとも「様子見」？",
    "今のチャート、上に行きそう？下に行きそう？",
    "エントリーするなら、指値はいくらがベスト？",
    "今買うと「高値掴み」になるリスクはある？",
    "ゴールデンクロスしそうだけど、ダマシじゃない？",
    "板の気配値を見て、強気か弱気か判断して"
]
q_entry_swing = [
    "数日〜数週間のスイング目線で評価して",
    "上昇トレンドはまだ続くと見ていい？",
    "押し目はどこ？具体的な価格で教えて",
    "週足チャートでの重要ラインを教えて",
    "信用買い残が多いけど、上値は重い？",
    "次の決算まで持っておくべき銘柄？",
    "チャートの形（酒田五法など）から分析して"
]
q_manage_risk = [
    "適切な損切り（逆指値）ラインはどこ？",
    "利確の目標値（第一、第二）を計算して",
    "含み損が辛い。損切りすべきか、耐えるべきか？",
    "ナンピンしても助かる可能性はある？",
    "今の資金量に対して、適正な株数は何株？",
    "リスクリワード比（損失：利益）は合ってる？",
    "連敗続きで辛い。メンタルを立て直す言葉を"
]
q_analysis_biz = [
    "直近の決算内容を、良い・悪い・中立で評価して",
    "売上高と営業利益の伸び率（成長性）はどう？",
    "この会社の「稼ぐ力（営業利益率）」は高い？",
    "ライバル企業と比較して、勝っている点は？",
    "将来性（AI、半導体など）はあるテーマ？",
    "PER・PBRから見て、今は割安？割高？",
    "中期経営計画の目標達成は現実的？"
]
q_emergency_crash = [
    "暴落中！今すぐ逃げるべき？それとも拾うべき？",
    "セリングクライマックス（大底）の兆候はある？",
    "追証回避のために、どこまで下がったらヤバい？",
    "この悪材料（不祥事など）、どこまで下がる？",
    "円高（円安）が急に進んだ。この株にプラス？マイナス？"
]
q_emergency_earnings = [
    "決算発表またぎ、勝負してもいい？（リスク判定）",
    "コンセンサス（市場予想）を超えられそう？",
    "好決算なのに暴落する「出尽くし売り」の可能性は？",
    "悪決算でも「悪材料出尽くし」で上がる可能性は？"
]

target_audience = "株式投資に取り組む個人投資家（年齢層高め・経験豊富・実益重視）。表面的な情報よりも、具体的な根拠や示唆に富んだ内容、相場格言や経験則を好む。"

# --- メインエリア：UI ---
st.title("🚀 AIプロンプト製造機")
st.write("▼ まずは「やりたいこと」のボタンを押してください！")

# 1. モード選択ボタン
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📈 売買・エントリー", type="primary" if st.session_state.mode == "📈 売買・エントリー" else "secondary", use_container_width=True):
        set_mode("📈 売買・エントリー")
with col2:
    if st.button("🛡️ 管理・メンタル", type="primary" if st.session_state.mode == "🛡️ 管理・メンタル" else "secondary", use_container_width=True):
        set_mode("🛡️ 管理・メンタル")
with col3:
    if st.button("📊 分析・ファンダ", type="primary" if st.session_state.mode == "📊 分析・ファンダ" else "secondary", use_container_width=True):
        set_mode("📊 分析・ファンダ")
with col4:
    if st.button("🚑 緊急・特別対応", type="primary" if st.session_state.mode == "🚑 緊急・特別対応" else "secondary", use_container_width=True):
        set_mode("🚑 緊急・特別対応")

# 現在モード表示
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <b>現在選択中：{st.session_state.mode}</b>
</div>
""", unsafe_allow_html=True)

# --- ロジック ---
def get_prompt_content(mode_name):
    char_list = []
    template_groups = {}
    include_time = True
    if mode_name == "📈 売買・エントリー":
        char_list = chars_entry
        template_groups = {"短期・デイトレ": q_entry_short, "スイング": q_entry_swing}
    elif mode_name == "🛡️ 管理・メンタル":
        char_list = chars_manage
        template_groups = {"資金・リスク管理": q_manage_risk}
    elif mode_name == "📊 分析・ファンダ":
        char_list = chars_analysis
        template_groups = {"業績・ファンダ": q_analysis_biz}
    elif mode_name == "🚑 緊急・特別対応":
        char_list = chars_emergency
        include_time = False
        template_groups = {"暴落対応": q_emergency_crash, "決算対応": q_emergency_earnings}
    
    if include_time:
        template_groups["⏱ 時間軸別"] = q_time_horizon
    return char_list, template_groups

current_chars, current_templates = get_prompt_content(st.session_state.mode)

# 2. キャラクター＆質問選択
c_char, c_quest = st.columns(2)
with c_char:
    selected_role = st.selectbox("1. 担当者（キャラクター）", current_chars)

with c_quest:
    # リスト作成：最初は空っぽに見せるための工夫（index=None）
    template_options = []
    for group_name, q_list in current_templates.items():
        for q in q_list:
            template_options.append(f"【{group_name}】 {q}")
            
    # ここがポイント！ index=None で「未選択（プレースホルダー表示）」にする
    selected_template_raw = st.selectbox(
        "2. 質問リスト（タップで選択肢が出ます）", 
        template_options, 
        index=None, 
        placeholder="▼ 質問のひな形を選ぶならここをタップ"
    )

# 質問文の抽出
selected_question_body = ""
if selected_template_raw:
    selected_question_body = selected_template_raw.split("】 ")[1]

st.markdown("---")

# 3. 入力エリア
st.write("3. 必要な情報を入力してください")

# (A) 銘柄コード入力
col_in1, col_in2 = st.columns([1, 2])
with col_in1:
    input_code_raw = st.text_input("銘柄コード / 社名", placeholder="例：7203、ソニー")
    # ここで全角→半角変換を自動適用
    input_code = to_half_width(input_code_raw)

# (B) ポジション選択（ボタン式に変更！）
with col_in2:
    st.write("現在の状態（ポジション）")
    # 4つのボタンを並べる
    pos1, pos2, pos3, pos4 = st.columns(4)
    
    # 状態管理のためのヘルパー関数
    def btn_type(label):
        return "primary" if st.session_state.status == label else "secondary"

    if pos1.button("未保有\n(買いたい)", type=btn_type("未保有（これから買いたい）"), use_container_width=True):
        set_status("未保有（これから買いたい）")
    if pos2.button("保有中\n(含み益)", type=btn_type("保有中（含み益）"), use_container_width=True):
        set_status("保有中（含み益）")
    if pos3.button("保有中\n(含み損)", type=btn_type("保有中（含み損）"), use_container_width=True):
        set_status("保有中（含み損）")
    if pos4.button("その他\n(監視中)", type=btn_type("その他・監視中"), use_container_width=True):
        set_status("その他・監視中")

# (C) 株ドラゴン & 詳細入力
with st.expander("🐉 株ドラゴンからデータを取得"):
    dragon_mode = st.selectbox("ランキング選択", ["値上がり率", "値下がり率", "ストップ高", "ストップ安", "窓開け（上昇）", "窓開け（下落）"])
    if st.button("データを読み込む"):
        with st.spinner("取得中..."):
            st.session_state.scraped_text = fetch_kabudragon_data(dragon_mode)

input_detail = st.text_area(
    "ニュース記事のコピペ / 補足・悩みなど",
    height=200,
    placeholder="例：決算が悪かったので売るか迷っています。（ここに株ドラゴンのデータも入ります）",
    value=st.session_state.scraped_text
)

# 4. 生成ボタン
if st.button("🚀 プロンプトを生成する（ここをクリック）", type="primary", use_container_width=True):
    if input_code or input_detail:
        final_request = ""
        parts = []
        if selected_question_body: parts.append(f"### 主な質問\n{selected_question_body}")
        if input_code: parts.append(f"### 対象銘柄\n{input_code}") # 変換済みコードを使用
        parts.append(f"### 現在の状態\n{st.session_state.status}")
        if input_detail: parts.append(f"### ニュース・補足\n{input_detail}")
        
        final_request = "\n\n".join(parts)
        
        prompt = f"""
# 命令書
あなたは「{selected_role}」になりきってください。
以下のターゲットに向けた、最高品質の回答を出力してください。

## ターゲット読者
{target_audience}

## 依頼内容
{final_request}

## 制約条件
- **文体**: キャラクターの性格を反映しつつ、投資家として納得感のあるプロの口調
- **内容**: 初心者向けの薄い内容ではなく、実践的で深みのある洞察を含めること
- **出力形式**: 読みやすいマークダウン形式（重要な数字や結論は太字にする）

## 出力
"""
        st.success("✨ 完成！")
        st.code(prompt, language="markdown")
        st.info("👆 コピーしてAIに貼り付けてね！")
    else:
        st.error("⚠️ 銘柄名か補足情報を入れてほしいにゃ！")
