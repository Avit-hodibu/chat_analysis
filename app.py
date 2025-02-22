import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    # read file as bytes
    bytes_data =uploaded_file.getvalue()
    #convert to bytes_data stream to string
    data = bytes_data.decode("utf-8")
    df= preprocessor.perprocess(data)

    st.dataframe(df)

    # fetch users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis of ", user_list)

    #show analysis
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_msg, num_link_msg= helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_msg)

        with col4:
            st.header("Total Link Shared")
            st.title(num_link_msg)

        # find the busiest user in group
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x, new_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()


            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

'''
        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
'''