import streamlit as st
import pandas as pd
from Top import columns_list, index_list, data_list, csv_file_path

##### ページの内容 #####
# AT後のボイスをカウント
# 出現率と解析値と比較

#################################
##### csvファイルの読み込み
#################################
try:
    df_voice_count = pd.read_csv(csv_file_path, index_col=0)

except FileNotFoundError:
    st.caption("Topページで新規作成を押して下さい")

##################################
##### AT後ボイスのカウント #########
##################################

st.subheader("AT後のボイス")
st.caption("・AT終了後にサブ液晶をタッチして確認")

#ボイスの選択肢をセッション管理するための変数設定
if "voice_select" not in st.session_state:
    st.session_state.voice_select = ""

#セレクトボックスを作成
st.session_state.voice_select = st.selectbox("ボイス", columns_list)

#選択肢に応じてセリフを参考として表示させる
if st.session_state.voice_select == columns_list[0]:
    st.caption("リン：ケン、会いたかった")
    st.caption("バット：おいおい、置いてかないでくれよ")

elif st.session_state.voice_select == columns_list[1]:
    st.caption("お前が思っているほど北斗神拳は無敵ではない")

elif st.session_state.voice_select == columns_list[2]:
    st.caption("退かぬ!媚びぬ!省みぬ!")

elif st.session_state.voice_select == columns_list[3]:
    st.caption("ケンシロウ、俺の名を言ってみろ！")

elif st.session_state.voice_select == columns_list[4]:
    st.caption("ふむ...この秘孔ではないらしい")

elif st.session_state.voice_select == columns_list[5]:
    st.caption("戦うのが北斗神拳伝承者としての宿命だ！")

elif st.session_state.voice_select == columns_list[6]:
    st.caption("待ち続けるのが私の宿命。そしてケンとの約束")

#登録ボタン
submit_btn = st.button("登録")

#登録ボタンが押されたら選択内容に応じてカウントアップ
if submit_btn:
    
    # st.caption("test")
    #ボイスの種類ごとに一致確認
    for column in df_voice_count.columns:
        
        #選択内容とカラム名が一致したらカウントアップ処理
        if column == st.session_state.voice_select:
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