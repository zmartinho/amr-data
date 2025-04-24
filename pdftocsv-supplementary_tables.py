import pdfplumber
import pandas as pd
import os

# Path to the PDF file
pdf_path = 'EU2023paper.pdf'

# Define the start and end page numbers
start_page = 85
end_page = 173

# Folder to save the CSV files
output_folder = 'EURawData'

# Create the folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Generate a list of page numbers within the range
page_numbers = list(range(start_page, end_page + 1))

# Function to extract the country title from the second line of the previous page
def extract_country_name(pdf, page_number):
    # Convert 1-based page number to 0-based index
    zero_based_page_number = page_number - 2  # Previous page in zero-based index
    
    # Check if the previous page number is valid
    if zero_based_page_number < 0:
        return "Unknown_Country"  # Handle case where there is no previous page
    
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        if zero_based_page_number < len(pdf.pages):
            # Select the previous page
            prev_page = pdf.pages[zero_based_page_number]
            
            # Extract text from the previous page
            text = prev_page.extract_text()
            
            # Assuming the country title is on the second line
            lines = text.split('\n')
            if len(lines) > 1:
                return lines[1].strip()  # Adjust based on your PDF's layout
    return "Unknown_Country"

# Loop through the specified page numbers
for page_number in page_numbers:
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Extract the country name from the previous page
        country_name = extract_country_name(pdf, page_number)
        
        # Convert 1-based page number to 0-based index
        zero_based_page_number = page_number - 1
        
        # Check if the page number is valid
        if zero_based_page_number < len(pdf.pages):
            # Select the current page
            page = pdf.pages[zero_based_page_number]
            
            # Extract table data
            table = page.extract_table()
            
            # Check if the table was successfully extracted
            if table:
                # Convert to DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                
                # Define the CSV file path with country name in the name and save it in the folder
                csv_filename = f'{country_name}_page_{page_number}.csv'
                csv_path = os.path.join(output_folder, csv_filename)
                
                # Save DataFrame to CSV
                df.to_csv(csv_path, index=False)
                
                print(f"Page {page_number} data has been saved to {csv_path}")
            else:
                print(f"No table found on page {page_number}")
        else:
            print(f"Page number {page_number} is out of range")

