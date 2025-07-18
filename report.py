import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Step 1: Data ko read aur analyze karna
def analyze_data(csv_file):
    """CSV file se data read karta hai aur basic analysis karta hai."""
    try:
        df = pd.read_csv(csv_file)
        # Basic analysis: Calculate the grand total
        grand_total = df['Total'].sum()
        return df, grand_total
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return None, None

# Step 2: PDF report generate karne ke liye class banana
class PDF(FPDF):
    def header(self):
        # Report ka Header/Title set karna
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Sales Report', 0, 1, 'C')
        # Line break
        self.ln(10)

    def footer(self):
        # Page ke neeche jaana
        self.set_y(-15)
        # Font set karna
        self.set_font('Arial', 'I', 8)
        # Page number
        page_num_text = f'Page {self.page_no()}'
        self.cell(0, 10, page_num_text, 0, 0, 'C')

    def create_table(self, data_df):
        """DataFrame se table banata hai."""
        # Table header
        self.set_font('Arial', 'B', 12)
        col_width = self.w / 4.5 # Column ki width
        header = list(data_df.columns)
        for h in header:
            self.cell(col_width, 10, h, 1, 0, 'C')
        self.ln()

        # Table data
        self.set_font('Arial', '', 12)
        for index, row in data_df.iterrows():
            for item in row:
                self.cell(col_width, 10, str(item), 1, 0, 'L')
            self.ln()

    def add_summary(self, total):
        """Report mein summary add karta hai."""
        self.ln(10) # Thoda space
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Summary:', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        summary_text = f"The grand total of all sales is: ${total:,.2f}"
        self.multi_cell(0, 10, summary_text)


if __name__ == "__main__":
    # Input file
    data_file = "sales_data.csv"

    # Data ko process karna
    sales_df, grand_total = analyze_data(data_file)

    if sales_df is not None:
        # PDF object banana
        pdf = PDF('P', 'mm', 'A4') # P = Portrait, mm = millimeters, A4 = page size
        pdf.add_page()

        # Report generation date
        pdf.set_font('Arial', '', 10)
        today_date = datetime.now().strftime("%B %d, %Y")
        pdf.cell(0, 10, f"Report generated on: {today_date}", 0, 1, 'R')
        pdf.ln(5)

        # Data table banana
        pdf.create_table(sales_df)

        # Summary add karna
        pdf.add_summary(grand_total)

        # PDF file save karna
        output_filename = "Sales_Report.pdf"
        pdf.output(output_filename)

        print(f"Success! Report saved as {output_filename}")
        print(f"Data from '{data_file}' has been processed.")
        print(f"Calculated Grand Total: ${grand_total:,.2f}")
    else:
        print("Could not generate report due to data loading error.")