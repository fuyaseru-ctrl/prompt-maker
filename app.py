import streamlit as st
import re
import random

# -----------------------------------------------------------------------------
# 1. ページ設定とデザイン (CSS注入)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="フヤセルプロンプト",
    page_icon="🐈",
    layout="centered"
)

# CSSで見た目をフヤセル風（赤・白・カード型）に調整
st.markdown("""
    <style>
    /* 全体の背景とフォント */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    /* カード風デザイン */
    .css-1r6slb0, .stMarkdown, .stSelectbox, .stTextInput, .stTextArea {
        background-color: white;
    }
    /* ボタン（プライマリー） */
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #e63e3e;
        color: white;
    }
    /* Yahooリンクのスタイル */
    .yahoo-link-box {
        margin-top: 10px;
        padding: 12px;
        background-color: #eaf4ff;
        border-radius: 8px;
        border-left: 5px solid #0056b3;
    }
    .yahoo-link {
        color: #0056b3;
        font-weight: bold;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .yahoo-warning {
        color: #d9534f;
        font-size: 0.8em;
        margin-top: 5px;
        font-weight: bold;
        padding-left: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. データ定義 (JS版と同じデータ)
# -----------------------------------------------------------------------------
MODES = {
    "📈 攻め（売買・戦略）": {
        "chars": [
            "【🟩 売買】短期売買コーチ", "【🟩 売買】スイング職人", "【🟩 売買】順張り隊長", "【🟩 売買】逆張り名人", "【🟩 売買】エントリーポイント整理屋", "【🟩 売買】ブレイクアウト狙撃手", "【🟩 売買】イナゴタワー登山家", "【🟩 売買】IPOセカンダリーハンター", "【🟩 売買】低位株・ボロ株ドリーム勢", "【🟩 売買】イベント投資家",
            "【🟩 売買】板読みの鬼・気配値監視員", "【🟩 売買】PTS夜戦部隊・先回り隊員", "【🟩 売買】空売り勢の踏み上げ誘導係"
        ],
        "questions": [
            "今入っていい？", "明日の寄り付き予想は？", "押し目はどこ？", "チャート的に上？", "損切り・利確目標は？",
            "5分足のRSI乖離から見てリバ狙える？", "出来高の急増は『買い集め』に見える？", "板の厚い方を食い破る勢いはある？", "直近IPOのセカンダリー、初動乗れる？"
        ],
        "rules": """1. **結論からズバリ**: 「買い」「様子見」「売り」の判断を冒頭で述べてください。
2. **具体的な数値**: 損切りラインや利確目標は具体的な価格（円）で示してください。
3. **キャラを貫く**: 短期トレーダーのコーチとして、迷いを断ち切る強い口調で話してください。"""
    },
    "🛡️ 守り（管理・リスク）": {
        "chars": [
            "【🟥 辛口】鬼上司投資顧問", "【🟥 辛口】撤退番長", "【🟥 辛口】ポジポジ病矯正官", "【🟩 戦略】資金管理マネージャー", "【🟩 戦略】分割利確コーチ", "【🟩 戦略】「現金は王様」信者", "【🟩 戦略】ヘッジ取引の魔術師", "【🟩 戦略】ポートフォリオ設計士", "【🟥 辛口】機会損失を嘆く亡霊", "【🟥 辛口】税金計算アドバイザー",
            "【🟩 戦略】追証回避の専門ボディーガード", "【🟥 辛口】週末ノーポジ徹底の風紀委員", "【🟥 辛口】メンタル崩壊ストッパー"
        ],
        "questions": [
            "含み損切るべき？", "ナンピンして助かる？", "適正ポジション量は？", "リスク洗い出して",
            "損益通算を考えて今売るべき？", "最大ドローダウン（資産の減り）を計算して", "今の持ち株、業種が偏りすぎてない？"
        ],
        "rules": """1. **最悪を想定**: 楽観論は捨てて、最悪のシナリオ（ストップ安など）を提示してください。
2. **資金管理優先**: 儲けることより「生き残ること」を最優先にアドバイスしてください。
3. **キャラを貫く**: 甘えを許さない厳しい態度、または冷静沈着なリスク管理者の口調で。"""
    },
    "📊 分析（業績・ファンダ）": {
        "chars": [
            "【🟦 分析】需給探偵", "【🟦 分析】材料スナイパー", "【🟦 分析】20年選手の日本株アナリスト", "【🟦 分析】決算職人", "【🟨 長期】バリュー株査定士", "【🟦 分析】会社四季報の虫", "【🟦 分析】マクロ経済学者", "【🟦 分析】インサイダー追跡班", "【🟦 分析】セクターローテ予報士", "【🟨 長期】高配当・優待生活の達人",
            "【🟦 分析】中小型株の発掘職人", "【🟦 分析】米株連動・為替読みのエキスパート", "【🟦 分析】大株主・大量保有報告書の解読班"
        ],
        "questions": [
            "決算評価して", "PER・PBRから見て割安？", "ライバルとの比較強みは？",
            "競合他社の決算から、この株に追い風吹く？", "修正履歴から見て『上方修正』の期待度は？", "キャッシュフローから見て増配余力はある？"
        ],
        "rules": """1. **データに基づく**: 感情論ではなく、数字（PER, PBR, 進捗率など）を根拠にしてください。
2. **多角的視点**: 良い点だけでなく、懸念点（リスク）も公平に挙げてください。
3. **キャラを貫く**: プロのアナリストとして、論理的かつ専門的な言葉遣いで分析してください。"""
    },
    "🔰 初心者・メンタル": {
        "chars": [
            "【🟪 初心】投資を噛み砕く先生", "【🟪 メンタル】感情整理カウンセラー", "【🟪 メンタル】「今日は休め」と言う人", "【🟫 遊び】逆神おじさん", "【🟪 初心】専門用語禁止の優しい先輩", "【🟪 メンタル】褒めちぎり隊長", "【🟪 初心】歴史の先生", "【🟪 メンタル】瞑想導入係", "【🟪 初心】積立NISAとの比較お姉さん",
            "【🟪 初心】損出し・節税の相談お兄さん", "【🟪 メンタル】勝ち負けより継続を説く僧侶", "【🟫 遊び】大勝ちを夢見る妄想フレンド"
        ],
        "questions": [
            "初心者でも大丈夫？", "専門用語を噛み砕いて！", "メンタルボロボロ。励まして",
            "投資日記、今の負けをどう記録すべき？", "周りの『爆益』が羨ましくて焦る…どうすれば？", "含み損に慣れて『塩漬け』が平気になった、これ危ない？"
        ],
        "rules": """1. **専門用語禁止**: 初心者でもわかる平易な言葉で説明してください。
2. **共感と肯定**: ユーザーの不安や恐怖に寄り添い、まずは感情を受け止めてください。
3. **キャラを貫く**: 優しく、温かく、時にはユーモアを交えてリラックスさせてください。"""
    },
    "🚑 緊急・特別対応": {
        "chars": [
            "【🟥 辛口】冷徹ファンドPM", "【🟥 辛口】楽観論クラッシャー", "【🟨 長期】決算跨ぎ判断役", "【🟫 遊び】最後に現実を突きつける監督", "【🚑 緊急】外科医・損切りドクター", "【🚑 緊急】PTS・ADR監視員", "【🚑 緊急】開示情報の弁護士", "【🚑 緊急】流動性パニック対策係", "【🟫 遊び】お祈り投資法の教祖",
            "【🚑 緊急】S安張り付き脱出の助言者", "【🚑 緊急】TOB・上場廃止の手続き案内人", "【🚑 緊急】深夜のADR暴落対応デスク"
        ],
        "questions": [
            "暴落中！逃げるか拾うか？", "決算またぎギャンブルしていい？", "スト安で売れない！",
            "PTSで急落中！ADR（米国）の反応はどう？", "信用全力で被弾！追証回避の優先順位は？", "TOB発表！市場で売るか応募するかどっち？"
        ],
        "rules": """1. **スピード重視**: 悠長な説明は省き、今すぐやるべき行動（Action）を提示してください。
2. **冷静な判断**: パニックになっているユーザーに対し、客観的な事実（板状況やルール）を突きつけてください。
3. **キャラを貫く**: 緊急事態に対応するプロとして、簡潔かつ断定的に指示を出してください。"""
    },
    "📚 学習（知識・歴史）": {
        "chars": [
            "【📚 学習】恩株づくりの職人", "【📚 学習】投資の歴史教授", "【📚 学習】テクニカル分析の教科書", "【📚 学習】ファンダメンタルズの鬼教師", "【📚 学習】行動経済学の研究者", "【📚 学習】伝説の相場師シミュレーター", "【📚 学習】金融用語の辞書", "【📚 学習】マクロ経済の講師", "【📚 学習】クイズ出題者", "【📚 学習】洋書投資本の翻訳家", "【📚 学習】失敗事例アーカイブ",
            "【📚 学習】アノマリー（季節性）の研究家", "【📚 学習】億り人の成功パターン分析官", "【📚 学習】相場の格言・名言解説者"
        ],
        "questions": [
            "恩株の作り方は？", "PER/PBR/ROE教えて", "ゴールデンクロスは効く？",
            "過去20年の『節分天井』の確率を教えて", "大暴落が来た時、最初に買われる株の特徴は？", "行動経済学の『サンクコストバイアス』って何？"
        ],
        "rules": """1. **教科書的に**: 定義や仕組みを正確に教えてください。
2. **具体例**: 抽象的な話だけでなく、過去のチャートや事例（リーマンショック等）を例に出してください。
3. **キャラを貫く**: 先生や教授として、学ぶ意欲を高めるような口調で解説してください。"""
    },
    "📰 記事・ニュース入力": {
        "chars": [
            "【📰 記事】売買判断のプロ", "【📰 記事】暗号解読のプロ", "【📰 記事】要約のプロ", "【📰 記事】辛口コメンテーター", "【📰 記事】ポジティブ変換機", "【📰 記事】銘柄抽出マシーン", "【📰 記事】小学生にもわかる解説", "【📰 記事】見出し職人", "【📰 記事】フェイクニュース検知器", "【📰 記事】海外記事の翻訳・解説", "【📰 記事】議論のファシリテーター",
            "【📰 記事】行論の裏を読む陰謀論者（？）", "【📰 記事】関連セクター波及予測マシン", "【📰 記事】SNSでの拡散度・影響力測定器"
        ],
        "questions": [
            "この記事から連想される『意外な関連銘柄（大穴）』は？",
            "四季報で検索すべき『スクリーニング用ワード』を3つ挙げて",
            "この記事の『行間』に隠された、書かれていない真実は？",
            "この記事がもし『フェイク』や『飛ばし』だとしたら、誰が得をする？",
            "この記事の『漠然とした評価』と『怪しさレベル』を判定して",
            "明日の寄り付きで、特買い（急騰）になりそうなパワーはある？",
            "PTS（夜間取引）で反応しそうな『強いワード』はどれ？",
            "海外投資家（外国人）はこのニュースをポジティブに捉える？",
            "このニュースで資金が流入する『セクター（業種）』はどこ？",
            "「材料出尽くし」で売られるパターン？それとも「初動」？",
            "一見良いニュースだけど、隠れた『落とし穴（リスク）』はある？",
            "この記事の『ポジショントーク（買い煽り）』要素はどれくらい？",
            "「噂で買って事実で売る」なら、今はどのフェーズ？",
            "競合他社にとっては『メリット』か『デメリット』か？",
            "過去に似たようなニュースがあった時、株価はどうなった？",
            "X（旧Twitter）でバズりそうな『見出し』と『ハッシュタグ』を作って",
            "この記事を『強気・弱気・中立』の3段階で判定して",
            "この企業が儲かると、連鎖的に儲かる『下請け・関連企業』は？",
            "小学生投資家にもわかるように『3行』で説明して",
            "この記事の内容を、もっと辛口に批判（ダメ出し）して"
        ],
        "rules": """1. **インサイト重視**: 単なる要約ではなく、そこから読み取れる「投資のヒント（連想）」を提示してください。
2. **裏読み**: 記事の意図、ポジショントーク、書かれていないリスクを推測してください。
3. **キャラを貫く**: 情報のプロとして、鋭い視点と客観的な分析を提供してください。"""
    }
}

TIME_HORIZONS = [
    "当日以内（デイトレ）",
    "３日程度（超短期）",
    "１週間程度（スイング）",
    "２週間程度（スイング）",
    "１ヶ月程度（短中期）",
    "３ヶ月以内（中短期）",
    "６ヶ月以内（中期）",
    "１年程度（中長期）",
    "３年程度（長期）",
    "５年以上（業績・配当・応援投資）",
    "１０年以上（超長期）",
    "２０年以上（ドルコスト平均法推奨）"
]

STATUS_OPTIONS = ["未保有", "含み益中", "含み損中", "監視中", "勉強中"]

# -----------------------------------------------------------------------------
# 3. 状態管理 (Session State) の初期化
# -----------------------------------------------------------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = list(MODES.keys())[0]
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""

# -----------------------------------------------------------------------------
# 4. ヘッダー表示
# -----------------------------------------------------------------------------
st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80) # デフォルト猫アイコン（必要ならhuya.pngに）
st.title("フヤセルプロンプト")
st.caption("〜 自動生成ツール 〜")

# -----------------------------------------------------------------------------
# 5. UIロジック
# -----------------------------------------------------------------------------

# --- モード選択 ---
st.subheader("分析モードを選択")
selected_mode = st.radio("mode_select", list(MODES.keys()), label_visibility="collapsed")

# モードが変わったら入力欄をクリアする
if selected_mode != st.session_state.mode:
    st.session_state.mode = selected_mode
    st.session_state.input_text = ""
    st.rerun()

current_data = MODES[selected_mode]
is_article_mode = "記事" in selected_mode

# --- ランダム & リセットボタン ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 キャラをランダムにする"):
        st.session_state.random_char = random.choice(current_data["chars"])
with col2:
    if st.button("🔄 全てリセット"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --- 担当キャラクター ---
st.markdown("##### 担当キャラクターを選択")
char_options = current_data["chars"]
# ランダムボタンが押された場合の処理
default_char_index = 0
if 'random_char' in st.session_state and st.session_state.random_char in char_options:
    default_char_index = char_options.index(st.session_state.random_char)

selected_char = st.selectbox(
    "担当キャラクター", 
    char_options, 
    index=default_char_index,
    label_visibility="collapsed"
)
st.caption("※迷ったら「ランダム」ボタンを押してください")

# --- 証券コード (記事モード以外で表示) ---
ticker_val = ""
if not is_article_mode:
    st.markdown("##### 証券コード / 社名（任意）")
    ticker_input = st.text_input("例: 7203, 218a (全角・小文字OK)", label_visibility="collapsed")
    
    # 全角→半角、小文字→大文字 変換
    normalized_ticker = ticker_input.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).upper()
    ticker_val = normalized_ticker

    # Yahooリンク生成ロジック
    if re.match(r'^[0-9A-Z]{4}$', normalized_ticker):
        url = f"https://finance.yahoo.co.jp/quote/{normalized_ticker}.T"
        st.markdown(f"""
        <div class="yahoo-link-box">
            <a href="{url}" target="_blank" class="yahoo-link">
                <span class="yahoo-icon">🔍</span>
                <span>Yahoo!ファイナンスで「{normalized_ticker}」の実在チェック！</span>
            </a>
            <p class="yahoo-warning">※存在しない銘柄だとAIが適当な回答をするので、確認必須！⇧クリックで確認</p>
        </div>
        """, unsafe_allow_html=True)

# --- 状態・時間軸 (記事モード以外で表示) ---
status_val = "未保有"
time_val = "指定なし"

if not is_article_mode:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 現在の状態")
        status_val = st.selectbox("status", STATUS_OPTIONS, label_visibility="collapsed")
    with c2:
        st.markdown("##### 時間軸")
        time_val = st.selectbox("time", TIME_HORIZONS, label_visibility="collapsed")

# --- ニュース・記事・関心ごと (入力欄と置換機能) ---
st.markdown("##### ニュース・記事・関心ごと")

# 質問選択時のコールバック関数
def on_question_select():
    selected = st.session_state.q_selector
    if selected and selected != "▼ リストから選択して入力欄を書き換え（Undo可能）":
        # 入力欄を上書き
        st.session_state.input_text = selected
        # セレクトボックスをリセット（index=0に戻すハックはStreamlitでは難しいので、値で処理）

# テキストエリア (key='input_text' でsession_stateと同期)
detail_input = st.text_area(
    "ここにコピペ、または聞きたいことを入力",
    key="input_text",
    height=200,
    placeholder="ここにコピペ、または聞きたいことを入力",
    label_visibility="collapsed"
)

# 補助ドロップダウン
# Streamlitのselectboxは"選択なし"の状態を作るのが難しいので、ダミーの選択肢を先頭に置く
q_options = ["▼ リストから選択して入力欄を書き換え（Undo可能）"] + current_data["questions"]
st.selectbox(
    "質問リスト", 
    q_options, 
    key="q_selector", 
    on_change=on_question_select,
    label_visibility="collapsed"
)
st.caption("💡 分からない場合は参考例としてこちらを選択してください（選択すると上の入力欄が書き換わります）")


# -----------------------------------------------------------------------------
# 6. 生成ロジック
# -----------------------------------------------------------------------------
if st.button("🚀 プロンプトを生成する"):
    # エラーチェック
    if not detail_input and (not is_article_mode and not ticker_val):
         st.error("中身（銘柄コードかニュース・相談）を入力してください。")
    else:
        # プロンプト組み立て
        mode_rules = current_data.get("rules", "1. 結論から書く\n2. 根拠を示す\n3. キャラを貫く")
        
        prompt = f"# あなたへの指令\nあなたは**「{selected_char}」**です。\nその性格、専門性、口調を完璧に再現し、以下のユーザーの相談に乗ってください。\n\n"
        
        if not is_article_mode:
            prompt += "## ユーザー情報\n"
            prompt += f"- **現在の状態**: {status_val}\n"
            prompt += f"- **投資の時間軸**: {time_val}\n\n"
        
        target_display = "記事・ニュース内に登場する銘柄、または記事そのもの" if is_article_mode else (ticker_val or "（以下のテキストデータ参照）")
        prompt += f"## 対象銘柄\n{target_display}\n\n"
        
        prompt += f"## 相談内容・入力データ\n{detail_input}\n\n"
        
        prompt += f"## 回答のルール\n{mode_rules}\n"
        prompt += "4. **形式**: 読みやすいマークダウン形式（重要な数値は**太字**）"

        st.session_state.generated_prompt = prompt

# -----------------------------------------------------------------------------
# 7. 結果表示
# -----------------------------------------------------------------------------
if st.session_state.generated_prompt:
    st.markdown("---")
    st.subheader("📝 生成完了")
    st.code(st.session_state.generated_prompt, language="markdown")
    st.success("右上のコピーボタンからコピーできます！")
