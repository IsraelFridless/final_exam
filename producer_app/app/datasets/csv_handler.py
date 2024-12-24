import pandas as pd
import os

def merge_files():
    current_dir = os.getcwd()
    file1 = os.path.join(current_dir, 'RAND_Database_of_Worldwide_Terrorism_Incidents.csv')
    file2 = os.path.join(current_dir, 'globalterrorismdb_0718dist.csv')

    df1 = pd.read_csv(file1, encoding='iso-8859-1')
    df2 = pd.read_csv(file2, encoding='iso-8859-1', low_memory=False)

    df2 = df2.drop_duplicates(subset=[col for col in df2.columns if col != 'eventid'], keep='first')

    df1.rename(columns={
        'Date': 'date',
        'City': 'city',
        'Country': 'country_txt',
        'Perpetrator': 'gname',
        'Weapon': 'attacktype1_txt',
        'Injuries': 'nwound',
        'Fatalities': 'nkill',
        'Description': 'summary'
    }, inplace=True)

    try:
        df1['date'] = pd.to_datetime(df1['date'], format='%d-%b-%y')
        df1['iyear'] = df1['date'].dt.year
        df1['imonth'] = df1['date'].dt.month
        df1['iday'] = df1['date'].dt.day
        df1.drop(columns=['date'], inplace=True)
    except Exception as e:
        print(f"Date parsing error: {e}")
        return

    df1['attacktype1_txt'] = df1['attacktype1_txt'].replace('Explosives', 'Bombing/Explosion')

    missing_cols = set(df2.columns) - set(df1.columns)
    if missing_cols:
        df1 = pd.concat([df1, pd.DataFrame(columns=list(missing_cols))], axis=1)

    df1 = df1[df2.columns]

    numeric_columns = ['nperps', 'nkill', 'nwound']
    for col in numeric_columns:
        df1[col] = pd.to_numeric(df1[col], errors='coerce')
        df2[col] = pd.to_numeric(df2[col], errors='coerce')

    merged_df = pd.concat([df2, df1], ignore_index=True, sort=False)
    merged_df = merged_df.drop_duplicates(subset=['country_txt', 'gname', 'city', 'iyear', 'imonth', 'iday', 'nperps', 'nkill', 'nwound'], keep='first')

    output_file = os.path.join(current_dir, "merged_file.csv")
    merged_df.to_csv(output_file, index=False)

    print(f"Successfully merged files. Output saved at: {output_file}")
    return merged_df


if __name__ == '__main__':
    merge_files()