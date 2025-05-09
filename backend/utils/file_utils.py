import pytesseract
from PIL import Image
import PyPDF2
from docx import Document
import io

def extract_text_from_image(image_file) -> str:
    """
    Extracts text from an image file using Tesseract OCR.
    :param image_file: The image file to extract text from.
    """
    return pytesseract.image_to_string(Image.open(image_file))

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a PDF file.
    :param pdf_file: The PDF file to extract text from.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    return "".join(page.extract_text() for page in reader.pages)

def extract_text_from_docx(docx_file) -> str:
    """
    Extracts text from a DOCX file.
    :param docx_file: The DOCX file to extract text from.
    """
    doc = Document(docx_file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def extract_text_from_file(file) -> str:
    """
    Extracts text from a file based on its type.
    :param file: The file to extract text from.
    :return: Extracted text.
    """
    if file.filename.endswith(('.png', '.jpg')):
        return extract_text_from_image(file)
    elif file.filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        return extract_text_from_docx(file)
    raise ValueError("File không đúng định dạng (PNG/JPG/PDF/DOCX)")