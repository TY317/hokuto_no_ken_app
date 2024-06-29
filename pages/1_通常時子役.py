import streamlit as st
import pandas as pd
import os
import random
import uuid
import getpass
from streamlit_cookies_manager import EncryptedCookieManager
import datetime

##### ページの内容 #####
# 通常時の中段ベルカウント用
# 参考に設定差のある子役確率を表示

#################################
##### csvファイルの読み込み、なければ作る
#################################
#csvファイルのパスを定義
csv_file_path = "./pages/nomal_center_bell_df.csv"

try:
    df = pd.read_csv(csv_file_path)

except FileNotFoundError:
    #通常時中段ベルの回数を保存するcsvファイル
    nomal_center_bell_df = pd.DataFrame(data=[0],columns=["中段ベル回数"])
    nomal_center_bell_df.to_csv(csv_file_path, index=False)

    #csvファイルを読み込んでおく
    df = pd.read_csv(csv_file_path)

#################################
##### 通常時中段ベルのカウント ####
#################################

st.subheader("通常時の中段ベル確率")
st.caption("・押し順は 中・右・左 を遵守")
st.caption("・通常時ゲーム数はマイスロを参照してください")

#csvファイルを読み込み、データフレームに格納する
# df = pd.read_csv("./pages/nomal_center_bell_df.csv")

##### 中段ベルのカウント用ボタンを押すとカウントアップするフォーム
with st.form(key="nomal_center_bell_count"):

    #2列に画面分割
    col1, col2 = st.columns(2)

    ##### 左画面
    with col1:
        st.caption("中段ベルカウント")

        #カウントボタン
        count_btn = st.form_submit_button("カウント")

        ####カウントボタンが押されたらカウントアップさせてcsv保存
        if count_btn:
        
            #現在のカウント数を取得する
            current_count = df.loc[0, df.columns[0]]

            #現在のカウントに1を足す
            new_count = current_count + 1

            #データフレーム内の数値データを置き換える
            df.at[0, df.columns[0]] = new_count

            #csvに保存する
            df.to_csv(csv_file_path, index=False)

    ##### 右画面
    with col2:
        #現在回数の表示
        st.caption("中段ベル回数")
        st.info(df.loc[0, df.columns[0]])


#####################################
##### 中段ベルの確率算出 #############
#####################################

##### 算出ボタンを押したら現在の確率が出てきて、参考情報と合わせて表示させる
with st.form(key="nomal_center_bell_result"):
    #2列に画面分割
    col1, col2 = st.columns(2)

    ##### 左画面：ゲーム数入力と算出ボタン、結果表示
    with col1:
        
        #通常時ゲーム数の入力欄
        normal_games = st.number_input(label="通常時ゲーム数", step=1)

        #算出ボタン
        submit_btn = st.form_submit_button("算出")

        ##### 算出ボタンが押されたら確率を算出して表示
        if submit_btn:
            #現在の中段ベル回数を取得
            current_count = df.loc[0, df.columns[0]]

            #1以上なら算出して表示
            if current_count > 0:
                #確率の算出
                ave_games = int(normal_games / current_count)

                #結果の表示
                st.caption("現在値")
                st.info(f"1/{ave_games}")
    
    ##### 右画面:参考情報の表示
    with col2:
        st.caption("解析値(※実戦値)")

        #データフレームで作成
        colomn_name = ["通常時の中段ベル出現率"]
        index_name = ["設定1", "設定6"]
        cb_data = ["1/160", "1/100"]
        cb_data_df = pd.DataFrame(cb_data, index=index_name, columns=colomn_name)

        #データフレームの表示
        st.dataframe(cb_data_df)

##################################
##### 子役確率を参考表示(データはマイスロで見れる)
##################################

st.caption("子役出現率の情報(現在値はマイスロで確認)")

#データフレーム作成して表示
df_koyakuave = pd.DataFrame({"スイカ合算": ["1/86.1", "1/85.7", "1/82.6", "1/78.3", "1/76.1"],
                       "中段チェリー": ["1/210.1", "1/204.8", "1/199.8", "1/195.0", "1/190.5"],
                       "リーチ目役": ["1/16384", "1/13107", "1/10922", "1/9362", "1/8192"]},
                       index=["設定1", "設定2", "設定4", "設定5", "設定6"])
st.dataframe(df_koyakuave)

###################################
##### 天国中の弱レア役のカウント #####
###################################
st.subheader("天国中の弱レア役ヒット率")
st.caption("・モードは演出から推測")

#csvファイルのパスを定義
csv_file_path_rea = "./pages/normal_rea_df.csv"

##### csvファイルの読み込み
try:
    df_rea = pd.read_csv(csv_file_path_rea)

except FileNotFoundError:
    #通常時中段ベルの回数を保存するcsvファイル
    normal_rea_df = pd.DataFrame(data=[0, 0],columns=["弱スイカ回数", "角チェ回数"])
    normal_rea_df.to_csv("./pages/normal_rea_df.csv", index=False)

    #csvファイルを読み込んでおく
    df_rea = pd.read_csv(csv_file_path_rea)

##### 中段ベルのカウント用ボタンを押すとカウントアップするフォーム
with st.form(key="normal_rea_count"):

    #2列に画面分割
    col1, col2 = st.columns(2)

    ##### 左画面
    with col1:
        st.caption("天国中弱レア役")

        #カウントボタン
        suika_count_btn = st.form_submit_button("天国中弱スイカ")
        cherry_count_btn = st.form_submit_button("天国中角チェ")

        ####カウントボタンが押されたらカウントアップさせてcsv保存
        if suika_count_btn:
        
            #現在のカウント数を取得する
            suika_current_count = df_rea.loc[0, df_rea.columns[0]]

            #現在のカウントに1を足す
            suika_new_count = suika_current_count + 1

            #データフレーム内の数値データを置き換える
            df_rea.at[0, df_rea.columns[0]] = suika_new_count

            #csvに保存する
            df_rea.to_csv(csv_file_path_rea, index=False)
        
        ####カウントボタンが押されたらカウントアップさせてcsv保存
        if cherry_count_btn:
        
            #現在のカウント数を取得する
            cherry_current_count = df_rea.loc[0, df_rea.columns[1]]

            #現在のカウントに1を足す
            cherry_new_count = cherry_current_count + 1

            #データフレーム内の数値データを置き換える
            df_rea.at[0, df_rea.columns[1]] = cherry_new_count

            #csvに保存する
            df_rea.to_csv(csv_file_path_rea, index=False)

    ##### 右画面
    with col2:
        #弱スイカ　現在回数の表示
        st.caption("天国中弱スイカ")
        st.info(df_rea.loc[0, df_rea.columns[0]])

        #角チェリー　現在回数の表示
        st.caption("天国中角チェリー")
        st.info(df_rea.loc[0, df_rea.columns[1]])

##################################
##### 天国中の弱レア役ヒット率を参考表示
##################################

st.caption("天国滞在時の前兆移行率")

#データフレーム作成して表示
df_rea_kaiseki = pd.DataFrame({"弱スイカ": ["10.66%", "10.78%", "16.02%", "17.86%", "19.16%"],
                               "角チェリー": ["1.75%", "1.85%", "3.87%", "5.43%", "7.14%"]},
                               index=["設定1", "設定2", "設定4", "設定5", "設定6"])
st.dataframe(df_rea_kaiseki)