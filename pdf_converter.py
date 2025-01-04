import PyPDF2
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER



input_list = [
    {
        'file name': 'Aster_DM_Healthcare_2024',
        'pages': ["18-24", "31-49", "51-60", "68-96", "280-369"]
    },
    {
        'file name': 'Authum_2024',
        'pages': ["3-12", "22-23", "30-41", "229-296"]
    },
    # {
    #     'file name': 'Craftsman_Automation_2024',
    #     'pages': ["2-23", "28-30", "99-127"]
    # },
    # {
    #     'file name': 'Equitas_Small_Finance_Bank_2024',
    #     'pages': ["30-114", "172-181", "196-197",  "254-323"]
    # },
    # {
    #     'file name': 'FSN_2024',
    #     'pages': ["2-40", "55-59", "196-197",  "247-316"]
    # },
]

def create_custom_text_page(output_pdf_path, custom_text="test text"):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    
    # Define the heading style
    styles = getSampleStyleSheet()
    heading_style = styles['Title']
    heading_style.fontName = 'Helvetica-Bold'
    heading_style.fontSize = 24
    heading_style.leading = 42
    heading_style.alignment = TA_CENTER
    heading_style.textColor = colors.darkblue
    
    # Draw the centered heading
    text = custom_text.replace("input_pdf/", "")
    text_width = c.stringWidth(text, heading_style.fontName, heading_style.fontSize)
    c.setFont(heading_style.fontName, heading_style.fontSize)
    c.setFillColor(heading_style.textColor)
    c.drawString((width - text_width) / 2.0, height / 2.0, text)
    c.save()

def select_pages(input_pdf_path, selected_pages, output_pdf_path="output_pdf/output.pdf"):
    # Open the input PDF file
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        writer = PyPDF2.PdfWriter()
        
        custom_text_pdf_path = "custom_text.pdf"
        create_custom_text_page(custom_text_pdf_path, f'Pages for: {input_pdf_path}')
        
        custom_text_reader = PyPDF2.PdfReader(custom_text_pdf_path)
        writer.add_page(custom_text_reader.pages[0])

        # Process the selected pages
        for page in selected_pages:
            if '-' in page:
                start, end = map(int, page.split('-'))
                for i in range(start - 1, end):
                    writer.add_page(reader.pages[i])
            else:
                writer.add_page(reader.pages[int(page) - 1])

        # Write the output PDF file'
        with open(output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

        print(f'Selected pages have been written to {output_pdf_path}')


def generate_pdfs(input_list):
    for annual_report in input_list:
        input_file_name = annual_report['file name']
        selected_pages = annual_report['pages']
        input_pdf_path = 'input_pdf/{}.pdf'.format(input_file_name)
        output_pdf_path = 'output_pdf/{}.pdf'.format(input_file_name)
        select_pages(input_pdf_path, selected_pages, output_pdf_path)


def combine_pdfs(folder_path, output_path):
    # Create a PdfMerger object
    merger = PyPDF2.PdfMerger()

    # Iterate through all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            merger.append(file_path)
            if os.path.exists(file_path): 
                # Delete the file 
                os.remove(file_path) 
                print(f"{file_path} has been deleted.") 
                
            else: 
                print(f"The file {file_path} does not exist.")

    # Write out the merged PDF
    merger.write(output_path)
    merger.close()

def make_final_pdf():
    folder_path = 'output_pdf'  # Replace with the path to your folder
    output_path = 'final_pdf/combined.pdf'  # Replace with the desired output path
    combine_pdfs(folder_path, output_path)
    print(f"PDFs combined into {output_path}")

generate_pdfs(input_list)
make_final_pdf()
