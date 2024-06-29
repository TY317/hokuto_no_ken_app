import streamlit as st
import pandas as pd

##### ページの内容 #####
# 通常時の中段ベルカウント用

#################################
##### AT中の中段ベルのカウント ####
#################################

st.subheader("AT中の中段ベル確率")
st.caption("・押し順は 中・右・左 を遵守")
st.caption("・子役パート中のみ対象")
st.caption("・ベル回数とバトルボーナス消化セット数から算出する")

#csvファイルを読み込み、データフレームに格納する
df = pd.read_csv("./pages/at_center_bell_df.csv")

##### 中段ベルのカウント用ボタンを押すとカウントアップするフォーム
with st.form(key="at_center_bell_count"):

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
            df.to_csv("./pages/at_center_bell_df.csv", index=False)

    ##### 右画面
    with col2:
        #現在回数の表示
        st.caption("中段ベル回数")
        st.info(df.loc[0, df.columns[0]])

#####################################
##### 中段ベルの確率算出 #############
#####################################

##### 算出ボタンを押したら現在の確率が出てきて、参考情報と合わせて表示させる
with st.form(key="at_center_bell_result"):
    #2列に画面分割
    col1, col2 = st.columns(2)

    ##### 左画面：ゲーム数入力と算出ボタン、結果表示
    with col1:

        #バトルボーナスセット数の入力欄
        bb_set_times = st.number_input(label="バトルボーナスセット数", step=1)

        #算出ボタン
        submit_btn = st.form_submit_button("算出")

        ##### 算出ボタンが押されたら確率を算出して表示
        if submit_btn:
            #現在の中段ベル回数を取得
            current_count = df.loc[0, df.columns[0]]

            #1以上なら算出して表示
            if current_count > 0:
                #確率の算出
                ave_games = int((bb_set_times * 30) / current_count)

                #結果の表示
                st.caption("現在値")
                st.info(f"1/{ave_games}")
    
    ##### 右画面:参考情報の表示
    with col2:
        st.caption("解析値(※実戦値)")

        #データフレームで作成
        colomn_name = ["AT中の中段ベル出現率"]
        index_name = ["設定1", "設定6"]
        cb_data = ["1/400", "1/200"]
        cb_data_df = pd.DataFrame(cb_data, index=index_name, columns=colomn_name)

        #データフレームの表示
        st.dataframe(cb_data_df)