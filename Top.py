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

    #####################################
    ##### csvの最終更新日を確認し、本日内に更新あれば「使用中」表示をする機能を追加
    #####################################
    st.caption("※ データの最終更新が本日だと「本日使用中」表示になります")
    import os
    from datetime import datetime, timedelta

    #csvが保存されているフォルダのパスを定義
    csv_folder_path = "./pages/"

    #フォルダ内の全ファイルリストを取得
    files = os.listdir(csv_folder_path)
    # st.write(files)

    #csvファイルのみを対象にしたリストを作る
    csv_files = [file for file in files if file.endswith(".csv")]
    # st.write(csv_files)

    # 最も最近の更新日時を保存する変数を初期化
    most_recent_date = None

    #最も最近の更新日時を取得する
    for csv_file in csv_files:
        file_path = os.path.join(csv_folder_path, csv_file)

        #最終更新日時を取得
        mtime = os.path.getmtime(file_path)

        #人間が読める形式に変換
        last_modified_date = datetime.fromtimestamp(mtime)

        #9時間を加算して日本時間に変換
        last_modified_date = last_modified_date + timedelta(hours=9)
        # st.write(last_modified_date)

        #更新日時が最も最近だったら変数に入れる
        if most_recent_date is None or last_modified_date > most_recent_date:
            most_recent_date = last_modified_date
    # st.write(most_recent_date)

    #現在日時を取得
    today = datetime.now()

    #9時間を加算して日本時間に変換
    today = today + timedelta(hours=9)
    
    #本日の日付を取得
    today = today.date()

    # st.write(today)

    #最新更新日が本日と同じなら「本日使用中」、違えば「本日未使用」を表示
    if most_recent_date is not None and most_recent_date.date() == today:
        st.markdown(":red-background[本日使用中]")
    else:
        st.markdown(":green-background[本日未使用]")

    ###################################
    ###################################
    ###################################

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
        
########################################
##### バージョン情報 ####################
########################################
st.caption("ver1.1.0")
st.caption("   ・カウントのマイナス、記録の1行削除機能の追加")
st.caption("ver1.0.1")
st.caption("   ・本日未使用・使用中の表示機能追加")
st.caption("ver1.0.0")
st.caption("   ・新規作成")