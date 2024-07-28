import pandas as pd

# Load the data from the Excel file
file_path = r'Desktop\Pune_Flats_Project/Flats_unique.xlsx'
flats_data_cleaned = pd.read_excel(file_path)

# Handle missing values
flats_data_cleaned['Carpet Area'] = flats_data_cleaned['Carpet Area'].replace('Not specified', '0 sqft').fillna('0 sqft')
flats_data_cleaned['Status'] = flats_data_cleaned['Status'].replace('Not specified', 'Unknown').fillna('Unknown')


# Function to clean and convert rate
def convert_rate(rate):
    if 'Cr' in rate:
        rate = rate.replace('₹', '').replace(' Cr', '').strip()
        return float(rate) * 10000000
    elif 'Lac' in rate:
        rate = rate.replace('₹', '').replace(' Lac', '').strip()
        return float(rate) * 100000
    else:
        return None

# Apply the function to the rate column
flats_data_cleaned['rate'] = flats_data_cleaned['rate'].apply(convert_rate)

# 'Carpet Area' column is treated as strings before cleaning
flats_data_cleaned['Carpet Area'] = flats_data_cleaned['Carpet Area'].astype(str)

# Convert 'Carpet Area' to numerical
flats_data_cleaned['Carpet Area'] = flats_data_cleaned['Carpet Area'].str.replace(' sqft', '')
flats_data_cleaned['Carpet Area'] = pd.to_numeric(flats_data_cleaned['Carpet Area'], errors='coerce').fillna(0)

# Regular expression pattern to extract area
pattern = r'in\s+(.*?)\s*,'

# Apply the pattern to extract the area
flats_data_cleaned['Area'] = flats_data_cleaned['flat_name'].str.extract(pattern, expand=True)

# Extract additional features from 'flat_name' and 'Floor'
flats_data_cleaned['Bedrooms'] = flats_data_cleaned['flat_name'].str.extract('(\d+) BHK').fillna(0).astype(int)
flats_data_cleaned['Total Floors'] = flats_data_cleaned['Floor'].str.extract('out of (\d+)').fillna(0).astype(float)
flats_data_cleaned['Current Floor'] = flats_data_cleaned['Floor'].str.extract('(\d+|Ground)').replace('Ground', '0').fillna(0).astype(int)

# Convert categorical columns to category type
categorical_columns = ['society_name', 'Status', 'Transaction', 'Furnishing', 'Facing', 'Overlooking', 'Ownership']
for col in categorical_columns:
    flats_data_cleaned[col] = flats_data_cleaned[col].astype('category')

# get cleaned data
flats_data_cleaned.to_excel("Flats_Cleaned_Data.xlsx", index=False)