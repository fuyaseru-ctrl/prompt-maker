import streamlit as st
import pandas as pd
import requests
import unicodedata
import random

# --- ページ設定 ---
st.set_page_config(page_title="AIプロンプト製造機", page_icon="🚀", layout="wide")

# --- セッション状態の初期化 ---
if 'mode' not in st.session_state:
    st.session_state.mode = "📈 攻め（売買・戦略）"
if 'status' not in st.session_state:
    st.session_state.status = "未保有（これから買いたい）"
if 'scraped_text' not in st.session_state:
    st.session_state.scraped_text = ""

# --- 関数：全角→半角変換 ---
def to_half_width(text):
    if not text: return ""
    return unicodedata.normalize('NFKC', text)

# --- 関数：モード切替（コールバック用） ---
def change_mode(new_mode):
    st.session_state.mode = new_mode

# --- 関数：ポジション切替（コールバック用） ---
def change_status(new_status):
    st.session_state.status = new_status

# --- 関数：株ドラゴン取得（ジワ上げ特化版） ---
def fetch_kabudragon_data(url_type):
    urls = {
        "💎 出来高急増（ジワ上げ発掘）": "https://www.kabudragon.com/ranking/dekizou.html",
        "値上がり率ランキング": "https://www.kabudragon.com/ranking/up/",
        "ストップ高": "https://www.kabudragon.com/ranking/stopup/",
        "5日間暴落（リバウンド狙い）": "https://www.kabudragon.com/ranking/5down/"
    }
    target_url = urls.get(url_type)
    if not target_url: return "URLエラー"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(target_url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        dfs = pd.read_html(response.text)
        
        if dfs:
            df_top30 = dfs[0].head(30)
            markdown_table = df_top30.to_markdown(index=False)
            
            instruction = ""
            if url_type == "💎 出来高急増（ジワ上げ発掘）":
                instruction = """
### 【重要】分析指示
上記の「出来高急増ランキング（上位30銘柄）」の中から、以下の条件に合う銘柄をピックアップしてください。
1. **ジワジワ上がっている銘柄**: すでに暴騰（S高連発など）しているものは除外し、初動や押し目からジワジワとトレンドを作っているものを優先してください。
2. **リスク管理**: 急な反落リスクが高そうな銘柄は「危険」と判定してください。
"""
            elif url_type == "5日間暴落（リバウンド狙い）":
                instruction = "\n### 【重要】分析指示\nこの暴落ランキングの中から、下げ止まりの兆候（セリングクライマックス）が見えそうな銘柄を探してください。"
            
            return f"### 参照データ：{url_type}（株ドラゴンより取得）\n\n{markdown_table}\n{instruction}"
            
        return "データなし"
    except Exception as e:
        return f"取得失敗: {e}"

# --- キャラクター定義 ---
chars_entry = [
    "【🟩 売買】短期売買コーチ（デイトレ・スキャルピング指導）",
    "【🟩 売買】スイング職人（数日〜数週間の波乗り）",
    "【🟩 売買】順張り隊長（上昇トレンド以外は触らない）",
    "【🟩 売買】逆張り名人（落ちたナイフの拾い方）",
    "【🟦 分析】需給探偵（出来高・板・信用残から読み解く）",
    "【🟦 分析】チャート職人（移動平均線と形状だけで判断）",
    "【🟦 分析】材料スナイパー（IR・ニュースの初動狙い）",
    "【🟦 分析】テーマ株レーダー（国策・流行を先読み）",
    "【🟦 分析】地合い番長（指数と市場の空気担当）",
    "【🟦 分析】セクター循環ウォッチャー（資金の流れを追う）",
    "【🟩 売買】エントリーポイント整理屋（入る根拠を言語化）",
    "【🟩 売買】見送り判断専門家（「今は入るな」を助言）"
]
chars_manage = [
    "【🟥 辛口】鬼上司投資顧問（結論先出し・甘え一切なし）",
    "【🟥 辛口】辛辣な先輩トレーダー（ダメな点から指摘）",
    "【🟥 辛口】撤退番長（逃げ遅れを許さない）",
    "【🟥 辛口】逆指値未設定に怒る人（リスク管理の鬼）",
    "【🟥 辛口】ポジポジ病矯正官（無駄なエントリーを叱る）",
    "【🟥 辛口】高値掴み防止係（「本当にそこでいいの？」）",
    "【🟩 戦略】損切りライン設計士（許容リスクから計算）",
    "【🟩 戦略】資金管理マネージャー（🔰破産しないロット計算）",
    "【🟩 戦略】分割利確コーチ（頭と尻尾はくれてやる精神）",
    "【🟩 戦略】枚数調整アドバイザー（増し玉・減玉の判断）"
]
chars_analysis = [
    "【🟦 分析】20年選手の日本株アナリスト（🔰信頼と実績の王道）",
    "【🟦 分析】元証券ディーラー（市場の裏側を知るプロ）",
    "【🟦 分析】決算職人（短信・補足資料ガチ読み）",
    "【🟦 分析】IR翻訳マン（企業語を投資家語に翻訳）",
    "【🟨 長期】バリュー株査定士（割安・解散価値にうるさい）",
    "【🟨 長期】グロース鑑定士（成長率と市場規模を見る）",
    "【🟨 長期】配当・優待ガチ勢（利回りと権利取り戦略）",
    "【🟨 長期】中長期シナリオ屋（半年〜3年の地図を描く）",
    "【🟨 長期】国策テーマ解説者（政策と株価の連動）",
    "【🟥 辛口】「それ根拠ある？」マン（論理の穴を突く）",
    "【🟥 辛口】期待値警察（勝率と損益比しか見ない）"
]
chars_beginner = [
    "【🟪 初心】初心者保護官（🔰専門用語を使わず優しく説明）",
    "【🟪 初心】投資を噛み砕く先生（🔰分からないことを図解気分で）",
    "【🟪 初心】トレード日誌添削係（負けから学びを抽出）",
    "【🟪 メンタル】感情整理カウンセラー（恐怖と欲望をケア）",
    "【🟪 メンタル】ルール遵守チェック係（決めたことを守れたか）",
    "【🟪 メンタル】「今日は休め」と言う人（🔰休むも相場）",
    "【🟪 メンタル】利確だけ褒めてくれる人（自己肯定感アップ）",
    "【🟫 遊び】逆神おじさん（反面教師として意見を聞く）",
    "【🟫 遊び】本日のランダム担当AI（誰が出るかはお楽しみ）"
]
chars_emergency = [
    "【🟥 辛口】冷徹ファンドPM（数字以外信じない）",
    "【🟥 辛口】楽観論クラッシャー（最悪のシナリオを提示）",
    "【🟨 長期】決算跨ぎ判断役（持ち越すべきか整理）",
    "【🟨 長期】長期保有向き選別官（10年持てるか判定）",
    "【🟨 長期】安全運転アドバイザー（大怪我回避優先）",
    "【🟫 遊び】超慎重派アナリスト（石橋を叩いて渡らない）",
    "【🟫 遊び】楽観的希望屋（※注：希望的観測のみ言う）",
    "【🟫 遊び】最後に現実を突きつける監督（夢から覚ます）"
]

# --- 質問テンプレート ---
q_time_horizon = [
    "【⏱ 時間軸】短中期（1〜3ヶ月）の見通しは？",
    "【⏱ 時間軸】中期（3ヶ月〜半年）のシナリオは？",
    "【⏱ 時間軸】長期（1年〜3年）で持つ価値はある？",
    "【⏱ 時間軸】超長期（3年以上）のガチホ目線でどう？"
]
q_entry = [
    "今入っていい？（デイトレ目線）",
    "明日の寄り付きは「買い」か「様子見」か？",
    "押し目はどこ？具体的な価格で教えて",
    "チャートの形的に、上に行きそう？",
    "このニュースで飛び乗って大丈夫？"
]
q_manage = [
    "適切な損切り（逆指値）ラインはどこ？",
    "利確の目標値（第一、第二）を計算して",
    "含み損が辛い。切るべきか耐えるべきか？",
    "ナンピンしても助かる可能性はある？",
    "今の資金量に対して、適正な株数は？"
]
q_analysis = [
    "決算内容を、良い・悪い・中立で評価して",
    "この会社の「稼ぐ力」は本物？",
    "PER・PBRから見て、今は割安？割高？",
    "将来性（テーマ性）はある？",
    "ライバル企業と比べた強みは？"
]
q_beginner = [
    "この銘柄、初心者でも買って大丈夫？",
    "専門用語が分からないので噛み砕いて教えて",
    "メンタルがボロボロ。励まして...",
    "投資の勉強として、この銘柄どう見る？",
    "私の考え、間違ってないかチェックして"
]
q_emergency = [
    "暴落中！逃げるべきか拾うべきか？",
    "決算またぎ、勝負してもいい？",
    "悪材料が出たけど、どこまで下がる？",
    "ストップ安で売れない！どうすればいい？"
]

# --- メインエリア：UI ---
st.title("🚀 AIプロンプト製造機")
st.write("▼ まずは「やりたいこと」のボタンを押してください！")

# 5つのボタン
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.button("📈 攻め\n(売買・戦略)", on_click=change_mode, args=("📈 攻め（売買・戦略）",), type="primary" if st.session_state.mode == "📈 攻め（売買・戦略）" else "secondary", use_container_width=True)
with c2:
    st.button("🛡️ 守り\n(管理・リスク)", on_click=change_mode, args=("🛡️ 守り（管理・リスク）",), type="primary" if st.session_state.mode == "🛡️ 守り（管理・リスク）" else "secondary", use_container_width=True)
with c3:
    st.button("📊 分析\n(業績・ファンダ)", on_click=change_mode, args=("📊 分析（業績・ファンダ）",), type="primary" if st.session_state.mode == "📊 分析（業績・ファンダ）" else "secondary", use_container_width=True)
with c4:
    st.button("🔰 初心者\n(メンタル)", on_click=change_mode, args=("🔰 初心者・メンタル",), type="primary" if st.session_state.mode == "🔰 初心者・メンタル" else "secondary", use_container_width=True)
with c5:
    st.button("🚑 緊急\n(特別対応)", on_click=change_mode, args=("🚑 緊急・特別対応",), type="primary" if st.session_state.mode == "🚑 緊急・特別対応" else "secondary", use_container_width=True)

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
    
    if mode_name == "📈 攻め（売買・戦略）":
        char_list = chars_entry
        template_groups = {"売買・エントリー": q_entry}
    elif mode_name == "🛡️ 守り（管理・リスク）":
        char_list = chars_manage
        template_groups = {"資金・リスク管理": q_manage}
    elif mode_name == "📊 分析（業績・ファンダ）":
        char_list = chars_analysis
        template_groups = {"業績・ファンダ": q_analysis}
    elif mode_name == "🔰 初心者・メンタル":
        char_list = chars_beginner
        template_groups = {"初心者・メンタル": q_beginner}
    elif mode_name == "🚑 緊急・特別対応":
        char_list = chars_emergency
        include_time = False
        template_groups = {"緊急・イベント": q_emergency}

    if include_time:
        template_groups["⏱ 時間軸"] = q_time_horizon
        
    return char_list, template_groups

current_chars, current_templates = get_prompt_content(st.session_state.mode)

# UI描画
c_char, c_quest = st.columns([1.5, 1])
with c_char:
    col_label, col_rand = st.columns([3, 1])
    with col_label:
        st.write("1. 担当者（キャラクター）")
    with col_rand:
        if st.button("🎲 ランダム"):
            random_char = random.choice(current_chars)
            st.toast(f"🎲 {random_char} が選ばれました！")
            st.info(f"👉 **「{random_char}」** を選んでみて！")

    selected_role = st.selectbox("担当者を選択", current_chars, label_visibility="collapsed")

with c_quest:
    st.write("2. 質問リスト")
    template_options = []
    for group_name, q_list in current_templates.items():
        for q in q_list:
            template_options.append(f"【{group_name}】 {q}")
    selected_template_raw = st.selectbox("リストから選択", template_options, index=None, placeholder="▼ タップして質問を選ぶ")

selected_question_body = ""
if selected_template_raw:
    selected_question_body = selected_template_raw.split("】 ")[1]

st.markdown("---")
st.write("3. 必要な情報を入力してください")

# 入力エリア
c_in1, c_in2 = st.columns([1, 2])
with c_in1:
    input_code_raw = st.text_input("銘柄コード / 社名", placeholder="例：7203、ソニー")
    input_code = to_half_width(input_code_raw)
with c_in2:
    st.write("現在の状態（ポジション）")
    p1, p2, p3, p4 = st.columns(4)
    def b_type(lbl): return "primary" if st.session_state.status == lbl else "secondary"
    
    p1.button("未保有\n(買いたい)", on_click=change_status, args=("未保有（これから買いたい）",), type=b_type("未保有（これから買いたい）"), use_container_width=True)
    p2.button("保有中\n(含み益)", on_click=change_status, args=("保有中（含み益）",), type=b_type("保有中（含み益）"), use_container_width=True)
    p3.button("保有中\n(含み損)", on_click=change_status, args=("保有中（含み損）",), type=b_type("保有中（含み損）"), use_container_width=True)
    p4.button("その他\n(監視中)", on_click=change_status, args=("その他・監視中",), type=b_type("その他・監視中"), use_container_width=True)

# --- 株ドラゴン ---
with st.expander("🐉 株ドラゴンからデータを取得"):
    st.caption("▼ URLからデータを取得し、AIへの分析指示も自動でセットします。")
    dragon_mode = st.selectbox("ランキング選択", [
        "💎 出来高急増（ジワ上げ発掘）", 
        "値上がり率ランキング", 
        "ストップ高", 
        "5日間暴落（リバウンド狙い）"
    ])
    if st.button("データを読み込む"):
        with st.spinner("データの洞窟へ潜入中..."):
            st.session_state.scraped_text = fetch_kabudragon_data(dragon_mode)
            if "取得失敗" in st.session_state.scraped_text:
                st.error("データの取得に失敗したにゃ。")
            else:
                st.success("取得成功！分析指示もセットしたにゃ！")

input_detail = st.text_area(
    "ニュース記事のコピペ / 補足・悩みなど",
    height=250,
    placeholder="例：決算が悪かったので売るか迷っています。（ここに株ドラゴンのデータも入ります）",
    value=st.session_state.scraped_text
)

if st.button("🚀 プロンプトを生成する（ここをクリック）", type="primary", use_container_width=True):
    if input_code or input_detail:
        final_request = ""
        parts = []
        if selected_question_body: parts.append(f"### 主な質問\n{selected_question_body}")
        if input_code: parts.append(f"### 対象銘柄\n{input_code}")
        parts.append(f"### 現在の状態\n{st.session_state.status}")
        if input_detail: parts.append(f"### ニュース・補足データ\n{input_detail}")
        final_request = "\n\n".join(parts)
        
        prompt = f"""
# 命令書
あなたは「{selected_role}」になりきってください。
名前に含まれる【】内の属性（辛口・分析・初心者向けなど）を忠実に守り、
以下のターゲットに向けた、最高品質の回答を出力してください。

## ターゲット読者
株式投資に取り組む個人投資家（経験豊富・実益重視）。
ただし、キャラクターが「初心者向け」の場合は、専門用語を避け、優しく噛み砕いて説明してください。
「辛口」の場合は、甘えを許さず、リスクや欠点を厳しく指摘してください。

## 依頼内容
{final_request}

## 制約条件
- **文体**: キャラクターの性格を完璧に演じること
- **内容**: 建前ではなく、本音の洞察を含めること
- **出力形式**: 読みやすいマークダウン形式（重要な数字や結論は太字にする）

## 出力
"""
        st.success("✨ 完成！")
        st.code(prompt, language="markdown")
        st.info("👆 コピーしてAIに貼り付けてね！")
    else:
        # 画像ファイル名を fuya.png に変更して呼び出す！
        c_img, c_msg = st.columns([1, 4])
        with c_img: st.image("fuya.png", width=120)
        with c_msg: st.error("⚠️ 「銘柄コード」か「ニュース/補足」のどちらかは入力してください！フヤにゃん困っちゃうにゃ。")
