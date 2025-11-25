import re
import pandas as pd

def preprocess(data):
    """
    Cleans and structures WhatsApp chat data into a pandas DataFrame.
    Supports 12-hour timestamp formats like:
    12/05/24, 10:45 pm - User: Message
    """

    # Updated regex to support:
    # - Single or double-digit day/month
    # - AM/PM in any case
    # - Different dash characters (-, –, —)
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APMapm]{2}\s[-–—]\s'

    # Split messages & extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Normalize unicode spaces like \u202f used by WhatsApp sometimes
    df['message_date'] = df['message_date'].str.replace(r'\u202f', ' ', regex=True)

    # Try multiple date formats (WhatsApp varies across regions)
    possible_formats = [
        '%d/%m/%y, %I:%M %p - ',
        '%d/%m/%y, %I:%M %p – ',
        '%d/%m/%y, %I:%M %p — ',
    ]

    parsed_dates = None
    for fmt in possible_formats:
        try:
            parsed_dates = pd.to_datetime(df['message_date'], format=fmt, errors='raise')
            break
        except:
            parsed_dates = None

    # If none matched, fall back to 'coerce'
    if parsed_dates is None:
        parsed_dates = pd.to_datetime(df['message_date'], errors='coerce')

    df['date'] = parsed_dates

    # Warn if any failed to parse
    if df['date'].isna().any():
        print("⚠️ Warning: Some dates could not be parsed and were set to NaT.")

    # Extract user & message
    users = []
    messages_list = []

    for message in df['user_message']:
        # Split at first "Username: message"
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  
            # Proper user-message format
            users.append(entry[1])
            messages_list.append(" ".join(entry[2:]))
        else:
            # System notification
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)

    # Extract date/time features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create hour period labels (00-1, 1-2, ..., 23-00)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
