import pandas as pd
from fpdf import FPDF
import textwrap

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Filtered Questions', 0, 1, 'C')

def export_csv_to_pdf(input_csv, output_pdf):
    """
    Exports a CSV file to a nicely formatted table in a PDF.

    Args:
        input_csv: Path to the input CSV file.
        output_pdf: Path to the output PDF file.
    """
    try:
        df = pd.read_csv(input_csv)

        # Create a PDF object with landscape orientation
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()

        # Set font
        pdf.set_font("Arial", size=10)

        # Add a table header
        col_width = pdf.w / (len(df.columns) + 1)
        row_height = pdf.font_size
        for col in df.columns:
            pdf.cell(col_width, row_height * 2, col, border=1)

        pdf.ln(row_height * 2)

        # Add table rows
        for row in df.itertuples():
            current_y = pdf.get_y()  # Get initial y-position for the row
            for i, col in enumerate(row[1:]):
                # Calculate x-position for each cell
                x_position = pdf.l_margin + i * col_width  
                pdf.set_xy(x_position, current_y) # Set cursor position

                wrapped_text = textwrap.fill(str(col), width=int(col_width / (pdf.font_size / 2)))
                pdf.multi_cell(col_width, row_height, wrapped_text.encode('latin-1', 'replace').decode('latin-1'), border=1, align='L')

                # Update current_y to the highest point reached by multi_cell
                current_y = max(current_y, pdf.get_y()) 

            pdf.ln(current_y - pdf.get_y() + row_height * 2)  # Move to the next row

            # Add new page if needed
            if pdf.get_y() > pdf.h - 20:  # 20mm margin
                pdf.add_page()
                # Reset font for new page
                pdf.set_font('Arial', size=10)
                # Repeat headers
                for col in df.columns:
                    pdf.cell(col_width, row_height, str(col)[:30], border=1)
                pdf.ln(row_height)

        # Save the PDF
        pdf.output(output_pdf)
        print(f"Successfully created PDF: {output_pdf}")

    except FileNotFoundError:
        print(f"Error: Input CSV file '{input_csv}' not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
input_csv = 'filtered_questions.csv'
output_pdf = 'filtered_questions.pdf'
export_csv_to_pdf(input_csv, output_pdf)