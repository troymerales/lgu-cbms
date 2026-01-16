import zipfile
import pandas as pd
import os

# Fix 1: The zip file name should have .zip extension
with zipfile.ZipFile("cbms_csv.zip", 'r') as zip_ref:
    zip_ref.extractall("unzipped")

# Fix 2: Create the unzipped directory if it doesn't exist
os.makedirs("unzipped", exist_ok=True)

# Fix 3: Use the correct zip file name and extract
with zipfile.ZipFile("cbms_csv.zip", 'r') as zip_ref:
    zip_ref.extractall("unzipped")

with pd.ExcelWriter("output.xlsx") as writer:
    for file in os.listdir("unzipped"):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join("unzipped", file))
            sheet_name = os.path.splitext(file)[0][:31]  # Excel sheet names ≤31 chars
            df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Successfully converted CSV files to Excel!")

