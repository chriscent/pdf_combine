import PyPDF2
import os

input_list = [
    {
        'file name': 'aster_annul_report_24',
        'pages': ["31-35", "39-50"]
    },
    {
        'file name': 'Natco_pharma_24',
        'pages': ["31-35", "39-50"]
    }
]

def select_pages(input_pdf_path, selected_pages, output_pdf_path="output_pdf/output.pdf"):
    # Open the input PDF file
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        writer = PyPDF2.PdfWriter()

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

# Example usage


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
