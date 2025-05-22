import pandas as pd
import camelot  # Library used for extracting tables from PDFs

# Load the PDF file
pdf_path = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\LBT2021.pdf"

# Use Camelot to extract tables from page 236 and 237 of the PDF
tables = camelot.read_pdf(pdf_path, pages="387-388", flavor="stream")

# Extract table data from both pages
# You may need to inspect each table if the data spans multiple tables
table_1 = tables[0].df  # Table from page 236
table_2 = tables[1].df  # Table from page 237

# Combine the data from both pages into one DataFrame
combined_table = pd.concat([table_1, table_2])

# Process the table to clean the data (if needed)
# Step 1: Take only columns 4, 5, and 6 (0-indexed: columns 3, 4, and 5)
df_adjusted = combined_table.iloc[:, [2, 3, 4]].copy()

# Step 2: Remove rows where column 5 or 6 is blank
df_adjusted.dropna(subset=[3, 4], inplace=True)


# Step 3: Convert values in columns 5 and 6 to numbers
def convert_to_number(value):
    try:
        return float(value)
    except ValueError:
        return None


df_adjusted[3] = df_adjusted[3].apply(convert_to_number)
df_adjusted[4] = df_adjusted[4].apply(convert_to_number)

# Step 4: Remove rows where conversion to number failed (i.e., where values are None)
df_adjusted.dropna(subset=[3, 4], inplace=True)
df_adjusted.columns = ["Flood Point", "Latitude", "Longitude"]


# Save the data to an Excel file
output_path = r"C:\Users\ibrah\OneDrive\Documents\Projects\Exploration\geospatial\data\flood_incidence_kuala_lumpur_cleaned_2021.xlsx"
df_adjusted.to_excel(output_path, index=False)

print(f"Data has been successfully extracted and saved to {output_path}")
