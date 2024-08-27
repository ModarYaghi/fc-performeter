import fitz  # Import PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io
from docx import Document  # import the Document class from python-docx

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path as needed


def convert_pdf_to_word(input_path, output_path):
    # Open the PDF file
    pdf_document = fitz.open(input_path)
    document = Document()  # Create a new Word document

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_num]
        # Render the page to an image
        pix = page.get_pixmap()
        # Convert the pixmap to an openable image for PIL
        img = Image.open(io.BytesIO(pix.tobytes()))
        # Perform OCR using Tesseract, specifying the language
        text = pytesseract.image_to_string(img, lang="ara")
        # extracted_text += text + "\n\n"  # Add spacing between pages
        document.add_paragraph(text)  # Add the text to the Word document

        print(f"Processed page {page_num + 1}/{len(pdf_document)}")

    # Save the extracted text to a Word file
    # with open(output_path, "w", encoding="utf-8") as file:
    #     file.write(extracted_text)
    document.save(output_path)
    print(f"Text extraction complete. Output saved to '{output_path}'.")


# Usage
pdf_input_path = "pdf_to_convert.pdf"
doc_output_path = "pdf_to_convert.docx"

convert_pdf_to_word(pdf_input_path, doc_output_path)
