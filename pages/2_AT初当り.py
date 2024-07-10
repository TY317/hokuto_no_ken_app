import streamlit as st
import pandas as pd

##### ページの内容 #####
# ATの当選ゲーム数と契機をメモ
# 当選回数と当選ゲーム数の合算から当選確率を算出

########################################
##### マイナス、1行削除のための変数・関数定義
########################################

#マイナス、1行削除のチェック状態用の変数
if "minus_check" not in st.session_state:
    st.session_state["minus_check"] = False
    minus_check = st.session_state["minus_check"]

def toggle_minus_check():
    st.session_state["minus_check"] = not st.session_state["minus_check"]

#ボタンの表示文字列の設定
if st.session_state["minus_check"]:
    button_str = "1行削除"
    button_type = "primary"
else:
    button_str = "登録"
    button_type = "secondary"

##############################
##### 当選ゲーム数と契機のメモ
##############################
st.subheader("AT当選ゲーム数と当選契機のメモ")

#csvファイルを読み込み、データフレームに格納する
df = pd.read_csv("./pages/AT_get_df.csv")

##### 初当りのデータを入力し、登録するフォーム
with st.form(key='bonus_data_input'):

    st.caption("初当りデータ入力")

    # 3列のカラムを作成
    col1, col2, col3 = st.columns(3)

    #当選ゲーム数の入力
    with col1:
        # st.subheader("ゲーム数")
        game_num = st.number_input(label=df.columns[0], step=1)

    #推測モードの入力
    with col2:
        # st.subheader("推測モード")
        mode = st.multiselect(df.columns[1],
                            ["天国","通常","地獄","?"])
        
        #1つの文字列にしておく
        joined_mode = ",".join(mode)

    #当選契機の入力
    with col3:
        # st.subheader("当選契機")
        koyaku = st.multiselect(df.columns[2],
                                ["中チェ","強スイカ","チャンス目","弱スイカ","角チェ","確定役","謎", "天井"])
        
        #1つの文字列にしておく
        joined_koyaku = ",".join(koyaku)
        
    #登録ボタン
    submit_btn = st.form_submit_button(button_str, type=button_type)

    ##### 登録ボタン押されたらデータフレームにデータ追加
    if submit_btn:
        if st.session_state["minus_check"]:
            #####最後の1行を削除する
            try:
                df.drop(df.index[-1], inplace=True)
            except IndexError:
                pass
        
        else:
            #入力されたデータをデータフレームにする
            df_new = pd.DataFrame({df.columns[0]: [game_num],
                                    df.columns[1]: [joined_mode],
                                    df.columns[2]: [joined_koyaku]})
            
            #すでにあるデータと入力されたデータを合体させたデータフレームにする
            df = pd.concat([df, df_new])

        #csvに保存する
        df.to_csv("./pages/AT_get_df.csv", index=False)

#当選履歴データの表示
st.dataframe(df)

##### 初当り確率の算出と解析データの表示
st.subheader("AT初当り確率")

#2列に画面分割
col1, col2 = st.columns(2)

#初当り確率の算出
with col1:
    st.caption("現在値")
    #ゲーム数カラム内のデータの数を取得
    at_times = int(df[df.columns[0]].count())

    #初当りが0回ならスキップ
    if at_times > 0:
        #初当りゲーム数の合計値を取得
        sum_games = int(df[df.columns[0]].sum())

        #平均初当りゲーム数を算出
        ave_games = int(sum_games / at_times)

        #算出結果の表示
        st.info(f"1/{ave_games}")
    
    else:
        pass

#解析データの表示
with col2:
    # st.subheader("AT初当り確率")
    st.caption("解析値")

    #####表をデータフレームで作成
    #カラム名を設定
    colomn_name = ["バトルボーナス初当り"]

    #インデックス名を設定
    index_name = ["設定1", "設定2", "設定4", "設定5", "設定6"]

    #確率データを設定
    bb_data = ["1/383.4", "1/370.5", "1/297.8", "1/258.7", "1/235.1"]

    #データフレーム作成
    bb_df = pd.DataFrame(bb_data, index=index_name, columns=colomn_name)

    #データフレームの表示
    st.dataframe(bb_df)
    # st.image("./pictures/AT初当り確率.bmp")

##### マイナスのチェックボックス表示
st.checkbox("マイナスカウント、1行削除", value=st.session_state["minus_check"], on_change=toggle_minus_check)
