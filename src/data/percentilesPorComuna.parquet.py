import pandas as pd
import numpy as np
import sys
import io

# Path to the Parquet file
file_path = 'src/data/DEFUNCIONES_2003_2024.parquet'
#file_path = './DEFUNCIONES_2003_2024.parquet'

# Load the Parquet file into a DataFrame
df = pd.read_parquet(file_path)

# Filter the DataFrame for the years 2014 to 2023
filtered_df = df[(df['AÑO'] >= 2014) & (df['AÑO'] <= 2023)].copy()

# Determine the correct age based on EDAD_TIPO and EDAD_CANT
filtered_df.loc[:, 'EDAD'] = filtered_df.apply(lambda row: row['EDAD_CANT'] if row['EDAD_TIPO'] == 1 else 0, axis=1)

# Define a function to calculate the required percentiles
def calculate_percentiles(group):
    percentiles = {
        'comuna': group.name,
        'p50': np.percentile(group['EDAD'], 50),
        'p25': np.percentile(group['EDAD'], 25),
        'p75': np.percentile(group['EDAD'], 75),
        'p100': np.max(group['EDAD']),
        'n': len(group)
    }
    return pd.Series(percentiles)

# Group by 'COMUNA' and apply the function
result_by_comuna = filtered_df.groupby('COMUNA', group_keys=False).apply(calculate_percentiles).reset_index(drop=True)

# Calculate the percentiles for the entire dataset
result_chile = pd.Series({
    'comuna': 'Chile',
    'p50': np.percentile(filtered_df['EDAD'], 50),
    'p25': np.percentile(filtered_df['EDAD'], 25),
    'p75': np.percentile(filtered_df['EDAD'], 75),
    'p100': np.max(filtered_df['EDAD']),
    'n': len(filtered_df)
})

# Combine the results for all comunas and Chile
final_result = pd.concat([result_by_comuna, result_chile.to_frame().T], ignore_index=True)

# Display the final result
#print(final_result)

# Create an in-memory buffer
buffer = io.BytesIO()

# Convert the DataFrame to a Parquet file in memory
final_result.to_parquet(buffer, engine='pyarrow')

# Write the buffer content to sys.stdout
sys.stdout.buffer.write(buffer.getvalue())
