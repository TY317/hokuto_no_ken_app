import streamlit as st
import pandas as pd

##### ページの内容 #####
# AT後のボイスをカウント
# 出現率と解析値と比較

#################################
##### csvファイルの読み込み、なければ作る
#################################
columns_list = ["リン・バット", "シン", "サウザー", "ジャギ", "アミバ", "ケンシロウ", "ユリア"]
index_list = ["出現回数", "出現確率"]
data_list = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
# index_list = ["出現回数", "出現確率","備考"]
# data_list = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],["デフォルト","高設定示唆(弱)","高設定示唆(弱)","高設定示唆(中)","高設定示唆(強)","設定4以上","設定5以上"]]

#csvファイルのパスを定義
csv_file_path = "./pages/after_at_voice_count_df.csv"

try:
    df_voice_count = pd.read_csv(csv_file_path, index_col=0)

except FileNotFoundError:
    #通常時中段ベルの回数を保存するcsvファイル
    # columns_list = ["リン", "バット", "シン", "サウザー", "ジャギ", "アミバ", "ケンシロウ", "ユリア"]
    # df = pd.DataFrame(data=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
    #                   index=["出現回数", "出現確率"],
    #                   columns=columns_list)
    df =pd.DataFrame(data_list, index=index_list, columns=columns_list)
    # df.to_csv(csv_file_path, index=False)
    df.to_csv(csv_file_path)

    #csvファイルを読み込んでおく
    df_voice_count = pd.read_csv(csv_file_path, index_col=0)

##################################
##### AT後ボイスのカウント #########
##################################

st.subheader("AT後のボイス")
st.caption("・AT終了後にサブ液晶をタッチして確認")

with st.form(key="after_at_voice_count"):

    st.caption("ボイス種類を登録")

    #セレクトボックスを作成
    voice_select = st.selectbox("ボイス", columns_list)

    #登録ボタン
    submit_btn = st.form_submit_button("登録")

    #登録ボタンが押されたら選択内容に応じてカウントアップ
    if submit_btn:
        
        #ボイスの種類ごとに一致確認
        for column in df_voice_count.columns:
            
            #選択内容とカラム名が一致したらカウントアップ処理
            if column == voice_select:
                #指定のカラムの数値を+1する
                df_voice_count.at[index_list[0], column] += 1

                #csvに保存する
                df_voice_count.to_csv(csv_file_path)
            else:
                pass
        
        #####各ボイスの現在の出現率を算出する
        #全ボイスの回数を出しておく
        voice_sum = df_voice_count.loc[index_list[0]].sum()

        #各ボイスの出現確率をデータフレームに入れる
        for column in df_voice_count.columns:

            #出現確率の計算
            probability_occurrence = df_voice_count.at[index_list[0], column] / voice_sum

            # #出現確率を%表記の文字列に変える
            # probability_occurrence = f"{probability_occurrence * 100:.1f}%"
            
            #データフレーム内に入れる
            df_voice_count.at[index_list[1], column] = probability_occurrence

        #csvに保存する
        df_voice_count.to_csv(csv_file_path)

# st.write(df_voice_count.columns)

##### %部分を文字列表記にしたデータフレームを起こしそれを結果として表示させる
#データフレームをコピー
df_result = df_voice_count.copy()

#%表記に変換する
df_result.loc[index_list[1]] = df_result.loc[index_list[1]].apply(lambda x: f"{x *100:.1f}%")

#各ボイスの説明を追加する
df_result.loc["備考"] = ["デフォルト","高設定示唆(弱)","高設定示唆(弱)","高設定示唆(中)","高設定示唆(強)","設定4以上","設定5以上"]



# st.dataframe(df_voice_count)
st.caption("現在の実戦値")
st.dataframe(df_result)

##################################
##### 解析情報の表示 #########
##################################

#解析値データフレームの作成
columns_list_theoretical = ["シン", "サウザー", "ジャギ", "アミバ"]
index_list_theoretical = ["設定1", "設定2", "設定4", "設定5", "設定6"]
data_list_theoretical = [["5.65%","5.04%","3.36%","1.22%"],
                         ["6.10%","5.34%","3.81%","1.53%"],
                         ["6.26%","6.26%","6.26%","6.26%"],
                         ["6.71%","6.71%","6.71%","6.71%"],
                         ["7.17%","7.17%","7.17%","7.17%"]]
df_theoretical = pd.DataFrame(data_list_theoretical, index=index_list_theoretical, columns=columns_list_theoretical)

#データフレームの表示
st.caption("解析値　※1G連時は確率違うため注意")
st.dataframe(df_theoretical)