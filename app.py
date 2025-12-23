import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import unicodedata
import random
import re

# --- ページ設定 ---
st.set_page_config(
    page_title="フヤセルジワジワあつめ",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="expanded" # PCは開く、スマホは閉じる挙動になります
)

# --- 定数・データ定義（復活のキャラたち！） ---

MODES = {
    "📈 攻め（売買・戦略）": {
        "chars": [
            "【🟩 売買】短期売買コーチ（デイトレ・スキャル指導）",
            "【🟩 売買】スイング職人（波乗りプロ）",
            "【🟩 売買】順張り隊長（トレンドフォロー）",
            "【🟩 売買】逆張り名人（リバウンド狙い）",
            "【🟩 売買】エントリーポイント整理屋（根拠言語化）"
        ],
        "questions": [
            "今入っていい？（デイトレ目線）",
            "明日の寄り付きは「買い」か「様子見」か？",
            "押し目はどこ？具体的な価格で教えて",
            "チャートの形的に、上に行きそう？",
            "適切な損切りラインと利確目標は？"
        ]
    },
    "🛡️ 守り（管理・リスク）": {
        "chars": [
            "【🟥 辛口】鬼上司投資顧問（甘え一切なし）",
            "【🟥 辛口】撤退番長（逃げ遅れ許さない）",
            "【🟥 辛口】ポジポジ病矯正官（無駄エントリー叱責）",
            "【🟩 戦略】資金管理マネージャー（破産回避）",
            "【🟩 戦略】分割利確コーチ（利益確保優先）"
        ],
        "questions": [
            "含み損が辛い。切るべきか耐えるべきか？",
            "ナンピンしても助かる可能性はある？",
            "今の資金量に対して、適正なポジション量は？",
            "この銘柄のリスク要因を洗い出して",
            "最悪のシナリオ（スト安など）への対策は？"
        ]
    },
    "📊 分析（業績・ファンダ）": {
        "chars": [
            "【🟦 分析】需給探偵（出来高・板・信用残）",
            "【🟦 分析】材料スナイパー（IR・ニュース初動）",
            "【🟦 分析】20年選手の日本株アナリスト（王道）",
            "【🟦 分析】決算職人（短信ガチ読み）",
            "【🟨 長期】バリュー株査定士（割安度判定）"
        ],
        "questions": [
            "決算内容を、良い・悪い・中立で評価して",
            "この会社の「稼ぐ力」と「将来性」は？",
            "PER・PBR・配当から見て割安？",
            "機関投資家の動きや需給状況はどう見える？",
            "ライバル企業と比較した強みは？"
        ]
    },
    "🔰 初心者・メンタル": {
        "chars": [
            "【🟪 初心】投資を噛み砕く先生（図解気分）",
            "【🟪 メンタル】感情整理カウンセラー（恐怖ケア）",
            "【🟪 メンタル】「今日は休め」と言う人（休むも相場）",
            "【🟫 遊び】逆神おじさん（反面教師）",
            "【🟪 初心】専門用語禁止の優しい先輩"
        ],
        "questions": [
            "この銘柄、初心者でも買って大丈夫？",
            "専門用語が分からないので噛み砕いて教えて",
            "メンタルがボロボロ。励まして...",
            "投資の勉強として、この銘柄どう見る？",
            "私の考え、間違ってないかチェックして"
        ]
    },
    "🚑 緊急・特別対応": {
        "chars": [
            "【🟥 辛口】冷徹ファンドPM（数字以外信じない）",
            "【🟥 辛口】楽観論クラッシャー（最悪を想定）",
            "【🟨 長期】決算跨ぎ判断役（持ち越すべきか）",
            "【🟫 遊び】最後に現実を突きつける監督"
        ],
        "questions": [
            "暴落中！逃げるべきか拾うべきか？",
            "決算またぎ、勝負してもいい？",
            "悪材料が出たけど、どこまで下がる？",
            "ストップ安で売れない！どうすればいい？"
        ]
    }
}

TIME_HORIZONS = [
    "指定なし",
    "超短期（デイトレ・当日）",
    "短期（数日〜数週間）",
    "中期（数ヶ月〜半年）",
    "長期（1年〜3年）",
    "超長期（永久保有）"
]

STATUS_OPTIONS = [
    "未保有（これから買いたい）",
    "保有中（含み益でホクホク）",
    "保有中（含み損でツライ）",
    "監視中（チャンス待ち）"
]

# --- 関数群 ---

def clean_tickers(text):
    if not text: return []
    normalized_text = unicodedata.normalize('NFKC', text)
    tokens = re.split(r'[,\s\n]+', normalized_text)
    return [t.upper() for t in tokens if t]

def fetch_fuyaseru_radar():
    """フヤセルジワジワレーダー（旧株ドラゴン）からデータを取得"""
    target_url = "https://www.kabudragon.com/ranking/dekizou.html"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(target_url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        dfs = pd.read_html(response.text, flavor='lxml')
        
        if dfs:
            df_top30 = dfs[0].head(30)
            markdown_table = df_top30.to_markdown(index=False)
            
            instruction = """
### 【レーダー検知データ】
上記のデータは「出来高急増ランキング（上位30銘柄）」です。
ここから以下の条件（フヤセルジワジワ条件）に合う銘柄を探し出してください。
1. **ジワジワ上昇**: 暴騰（S高連発）ではなく、初動や押し目からトレンドを作っているもの。
2. **リスク回避**: 急反落の危険性が高い銘柄は除外警告してください。
"""
            return f"{instruction}\n\n{markdown_table}"
        return "データなしにゃ..."
    except Exception as e:
        return f"レーダー故障中: {e} (lxml入れてる？)"

def copy_button_component(text_to_copy):
    escaped_text = text_to_copy.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    js_code = f"""
    <script>
    function copyText() {{
        const textToCopy = `{escaped_text}`;
        navigator.clipboard.writeText(textToCopy).then(function() {{
            const btn = document.getElementById("copyBtn");
            btn.innerText = "✅ コピー完了！";
            btn.style.backgroundColor = "#e0ffe0";
            setTimeout(() => {{
                btn.innerText = "📋 タップしてコピー";
                btn.style.backgroundColor = "#ffffff";
            }}, 2000);
        }});
    }}
    </script>
    <div style="margin-top: 10px;">
        <button id="copyBtn" onclick="copyText()" style="
            width: 100%;
            background-color: #ffffff; 
            border: 1px solid #d6d6d8; 
            border-radius: 8px; 
            padding: 12px; 
            font-size: 16px;
            font-weight: bold;
            cursor: pointer; 
            color: #31333F;">
            📋 タップしてコピー
        </button>
    </div>
    """
    components.html(js_code, height=60)

# --- サイドバー（グローバル設定・スマホではメニュー内） ---

st.sidebar.title("🐈 設定メニュー")

# 1. モード選択（これが全てを決める！）
selected_mode_name = st.sidebar.radio(
    "分析モード",
    list(MODES.keys()),
    index=0
)
current_mode_data = MODES[selected_mode_name]

st.sidebar.markdown("---")

# 2. フヤセルジワジワレーダー
st.sidebar.subheader("📡 フヤセルジワジワレーダー")
st.sidebar.caption("市場で「出来高急増中」の銘柄データを取得して分析に加えます。")
if st.sidebar.button("レーダー起動（データ取得）", type="secondary", use_container_width=True):
    with st.spinner("電波を受信中にゃ...📡"):
        scraped_data = fetch_fuyaseru_radar()
        if "故障中" in scraped_data:
            st.toast("フヤにゃん「あわわ、レーダーが反応しないにゃ💦」", icon="🙀")
        else:
            st.session_state['scraped_text'] = scraped_data
            st.toast("データ受信完了！入力欄に入れたにゃ！", icon="😺")

# --- メイン画面（スマホで操作しやすい配置） ---

st.title(f"{selected_mode_name.split()[0]} プロンプト製造機")
st.caption("スマホ片手に、サクッと最強の分析指示を作ろうにゃ！")

# フォームエリア
with st.container():
    # 1. キャラクター＆質問（2カラムだがスマホでは縦に並ぶ）
    c1, c2 = st.columns(2)
    
    with c1:
        # ランダムボタン機能
        if st.button("🎲 キャラをランダムにする"):
             st.session_state['rand_char_idx'] = random.randint(0, len(current_mode_data["chars"]) - 1)
        
        # インデックス制御
        idx = st.session_state.get('rand_char_idx', 0)
        if idx >= len(current_mode_data["chars"]): idx = 0
        
        selected_char = st.selectbox(
            "担当キャラクター",
            current_mode_data["chars"],
            index=idx
        )

    with c2:
        selected_q = st.selectbox(
            "聞きたいこと（メイン）",
            current_mode_data["questions"]
        )

    # 2. 状態・時間軸（展開式にしてスッキリさせる）
    with st.expander("⏱️ 時間軸・ポジション設定（任意）"):
        sc1, sc2 = st.columns(2)
        with sc1:
            time_horizon = st.selectbox("時間軸", TIME_HORIZONS)
        with sc2:
            status = st.selectbox("現在の状態", STATUS_OPTIONS)

    # 3. 入力エリア
    st.markdown("👇 **銘柄コード・ニュース・メモ**")
    
    # レーダーデータの反映
    default_text = st.session_state.get('scraped_text', "")
    
    input_text = st.text_area(
        "ここに入力（コード、ニュース、心の叫びなど）",
        value=default_text,
        height=150,
        placeholder="例：\n7203 トヨタ\n決算が心配。このまま持ってていい？\n（レーダーを使うとここにデータが入ります）"
    )

    # 生成ボタン（大きくて押しやすく！）
    generate_btn = st.button("🚀 プロンプトを生成する", type="primary", use_container_width=True)

# --- 生成ロジック ---

if generate_btn:
    # 銘柄抽出（テキスト全体から探す）
    tickers = clean_tickers(input_text)
    
    # 入力が空っぽの場合のフヤにゃん対応
    if not input_text.strip():
        st.error("フヤにゃん「にゃーん！入力が空っぽだにゃ😿 銘柄コードか、相談したいことを書いてほしいにゃ…」")
        st.image("https://placehold.co/100x100/orange/white?text=Fuya", width=100) # 仮画像
    
    else:
        # 銘柄リスト表記
        ticker_str = ", ".join(tickers) if tickers else "（文章内の銘柄または全般）"

        # プロンプト組み立て
        prompt = f"""
# あなたへの指令
あなたは**「{selected_char}」**です。
その性格、専門性、口調を完璧に再現し、以下のユーザーの相談に乗ってください。

## ユーザー情報・相談内容
- **現在の状態**: {status}
- **投資の時間軸**: {time_horizon}
- **聞きたいこと**: {selected_q}

## 対象銘柄・データ
{input_text}

## 回答のルール
1. **結論から書く**: 最初にズバリと回答してください。
2. **根拠を示す**: なぜそう判断したのか、論理的（または感情的）な理由を述べてください。
3. **キャラを貫く**: {selected_char.split('】')[1]}として、ターゲット読者に刺さる言葉選びをしてください。
4. **形式**: 読みやすいマークダウン形式（重要な数値は**太字**）

## 最後に
フヤセルジワジワレーダー（独自分析）の観点から、もし危険な兆候があれば警告してください。
"""
        st.session_state.generated_prompt = prompt
        st.success("生成完了にゃ！下のボタンでコピーして使ってね🐾")

# --- 結果表示エリア ---

if 'generated_prompt' in st.session_state and st.session_state.generated_prompt:
    st.markdown("---")
    st.subheader("📝 生成されたプロンプト")
    
    # 1. 標準コピー（中身確認用）
    st.code(st.session_state.generated_prompt, language="markdown")
    
    # 2. スマホ特化コピーボタン（デカくて押しやすい）
    copy_button_component(st.session_state.generated_prompt)
    
    st.caption("※上のコピーボタンを押すと、クリップボードに保存されるにゃ！")
