import streamlit as st
import pandas as pd

st.title("スマスロ北斗の拳")

##### 新規作成ボタンを押すとデータをすべてリセットする

columns_list = ["リン・バット", "シン", "サウザー", "ジャギ", "アミバ", "ケンシロウ", "ユリア"]
index_list = ["出現回数", "出現確率"]
data_list = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
csv_file_path = "./pages/after_at_voice_count_df.csv"

#フォームの作成
with st.form(key='new_play'):

    #説明書き
    st.caption("※ 新規作成ボタンを押すとデータがすべて0リセットされます!")
    st.caption("※ 同時に他の人が利用しているとその人のデータも0リセットされます!恨みっこなしです!")

    #新規作成ボタンの設定
    start_btn = st.form_submit_button("新規作成")

    #ボタンが押されたらcsvファイルをリセットし保存
    if start_btn:

        ##### AT初当り用
        #AT初当り用のデータフレームを保存するcsvファイル
        AT_get_df = pd.DataFrame(columns=["ゲーム数", "推測モード", "当選契機"])
        # AT_get_df = pd.DataFrame(columns=["a", "b", "c"])
        AT_get_df.to_csv("./pages/AT_get_df.csv", index=False)

        ##### 通常時中段ベル用
        #通常時中段ベルの回数を保存するcsvファイル
        nomal_center_bell_df = pd.DataFrame(data=[0],columns=["中段ベル回数"])
        # nomal_center_bell_df = pd.DataFrame(columns=["中段ベル回数"])
        nomal_center_bell_df.to_csv("./pages/nomal_center_bell_df.csv", index=False)

        ##### 天国中弱レア用
        #天国中レア役の回数保存するcsvファイル
        normal_rea_df = pd.DataFrame(data=[[0, 0]], columns=["弱スイカ回数", "角チェ回数"])
        normal_rea_df.to_csv("./pages/normal_rea_df.csv", index=False)

        ##### AT中の中段ベル用
        #AT中の中段ベルの回数を保存するcsvファイル
        at_center_bell_df = pd.DataFrame(data=[0], columns=["中段ベル回数"])
        # at_center_bell_df = pd.DataFrame(columns=["中段ベル回数"])
        at_center_bell_df.to_csv("./pages/at_center_bell_df.csv", index=False)

        ##### AT後のボイスカウント用
        # columns_list = ["リン・バット", "シン", "サウザー", "ジャギ", "アミバ", "ケンシロウ", "ユリア"]
        # index_list = ["出現回数", "出現確率"]
        # data_list = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        # index_list = ["出現回数", "出現確率","備考"]
        # data_list = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],["デフォルト","高設定示唆(弱)","高設定示唆(弱)","高設定示唆(中)","高設定示唆(強)","設定4以上","設定5以上"]]
        # csv_file_path = "./pages/after_at_voice_count_df.csv"
        df =pd.DataFrame(data_list, index=index_list, columns=columns_list)
        df.to_csv(csv_file_path)

        #csvファイルのパスを定義
        # csv_file_path = "./pages/after_at_voice_count_df.csv"
        # df = pd.DataFrame(data=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
        #                 index=["出現回数", "出現確率"],
        #                 columns=columns_list)
        # df.to_csv(csv_file_path, index=False)
        
st.caption("ver1.0.0")
st.caption("   ・新規作成")