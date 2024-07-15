import pandas as pd
import sys
import io

# Path to the Parquet file
file_path = 'src/data/DEFUNCIONES_2003_2024.parquet'

# Load the Parquet file into a DataFrame
df = pd.read_parquet(file_path)

# Filter the DataFrame for the years 2014 to 2023
filtered_df = df[(df['AÑO'] >= 2014) & (df['AÑO'] <= 2023)]

# Determine the correct age based on EDAD_TIPO and EDAD_CANT
filtered_df['EDAD'] = filtered_df.apply(lambda row: row['EDAD_CANT'] if row['EDAD_TIPO'] == 1 else 0, axis=1)

# Group by 'COMUNA' and 'EDAD' and count the number of deaths
summary_df = filtered_df.groupby(['COMUNA', 'EDAD']).size().reset_index(name='defunciones')

# Rename the 'COMUNA' column to 'comuna'
summary_df.rename(columns={'COMUNA': 'comuna', 'EDAD':'edad'}, inplace=True)

# Create an in-memory buffer
buffer = io.BytesIO()

# Convert the DataFrame to a Parquet file in memory
summary_df.to_parquet(buffer, engine='pyarrow')

# Write the buffer content to sys.stdout
sys.stdout.buffer.write(buffer.getvalue())
