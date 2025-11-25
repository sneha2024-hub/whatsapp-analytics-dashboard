import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

st.sidebar.title("WhatsApp Chat Analyzer")

# Upload chat file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    try:
        # Read and decode file
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        
        # Preprocess data
        df = preprocessor.preprocess(data)

        # Fetch unique users
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        # User selection
        selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

        # Date filter
        st.sidebar.title("Select Date Range")
        start_date = st.sidebar.date_input(
            "Start date",
            min(df['date']),
            min_value=min(df['date'])
        )
        end_date = st.sidebar.date_input(
            "End date",
            max(df['date']),
            min_value=min(df['date'])
        )

        # Filter DataFrame by date range
        if start_date <= end_date:
            df = df[(df['date'] >= pd.to_datetime(start_date)) &
                    (df['date'] <= pd.to_datetime(end_date))]
        else:
            st.sidebar.error("End date should be greater than or equal to the start date.")

        # Handle case where no data in selected range
        if df.empty:
            st.warning("No messages found in the selected date range. Try adjusting the filter.")
        else:
            if st.sidebar.button("Show Analysis"):

                # ---------- NEW: Extra derived columns for advanced insights ----------
                # Ensure message column is string
                df['message'] = df['message'].astype(str)

                # Message length (characters)
                df['message_length'] = df['message'].apply(len)

                # Hour and day name (for time-based insights)
                df['hour'] = df['date'].dt.hour
                df['day_name'] = df['date'].dt.day_name()

                # Night messages: between 10 PM and 3 AM
                night_msgs_df = df[(df['hour'] >= 22) | (df['hour'] <= 3)]
                night_messages_count = night_msgs_df.shape[0]

                # Average message length
                avg_message_length = round(df['message_length'].mean(), 2) if not df.empty else 0

                # Most active day
                most_active_day = df['day_name'].mode()[0] if not df['day_name'].empty else "N/A"
                # ---------------------------------------------------------------------

                # Stats Area
                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
                st.title("Top Statistics")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.header("Total Messages")
                    st.title(num_messages)
                with col2:
                    st.header("Total Words")
                    st.title(words)
                with col3:
                    st.header("Media Shared")
                    st.title(num_media_messages)
                with col4:
                    st.header("Links Shared")
                    st.title(num_links)

                # ---------- NEW: Conversation Insights ----------
                st.title("Conversation Insights")

                ci1, ci2, ci3 = st.columns(3)
                with ci1:
                    st.metric("Avg Message Length", f"{avg_message_length} chars")
                with ci2:
                    st.metric("Night Messages (10PM–3AM)", night_messages_count)
                with ci3:
                    st.metric("Most Active Day", most_active_day)
                # -----------------------------------------------

                # Monthly timeline
                st.title("Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # Daily timeline
                st.title("Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # Activity map
                st.title('Activity Map')
                col1, col2 = st.columns(2)

                with col1:
                    st.header("Most busy day")
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.header("Most busy month")
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                # Weekly activity map
                st.title("Weekly Activity Map")
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)

                # Most busy users (Group level)
                if selected_user == 'Overall':
                    st.title('Most Busy Users')
                    x, new_df = helper.most_busy_users(df)
                    fig, ax = plt.subplots()

                    col1, col2 = st.columns(2)

                    with col1:
                        ax.bar(x.index, x.values)
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        st.dataframe(new_df)

                # WordCloud
                st.title("Wordcloud")
                df_wc = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                ax.axis("off")
                st.pyplot(fig)

                # Most common words
                most_common_df = helper.most_common_words(selected_user, df)
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1])
                plt.xticks(rotation='vertical')

                st.title('Most Common Words')
                st.pyplot(fig)

                # Emoji analysis
                emoji_df = helper.emoji_helper(selected_user, df)
                st.title("Emoji Analysis")

                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    if not emoji_df.empty:
                        fig, ax = plt.subplots()
                        ax.pie(
                            emoji_df[1].head(),
                            labels=emoji_df[0].head(),
                            autopct="%0.2f"
                        )
                        st.pyplot(fig)
                    else:
                        st.info("No emojis found for the selected user / date range.")

    except UnicodeDecodeError:
        st.error("There was an error decoding the file. Please ensure it's a UTF-8 encoded text file.")
else:
    st.info("Please upload a WhatsApp chat file in UTF-8 format for analysis.")
