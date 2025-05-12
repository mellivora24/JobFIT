import re
import PyPDF2
import pytesseract
from PIL import Image
from docx import Document

def extract_text_from_image(image_file) -> str:
    """
    Trich xuất văn bản từ tệp hình ảnh.
    :param image_file: Tệp hình ảnh để trích xuất văn bản.
    """
    return pytesseract.image_to_string(Image.open(image_file))


def extract_text_from_pdf(pdf_file) -> str:
    """
    Trich xuất văn bản từ tệp PDF.
    :param pdf_file: Tệp PDF để trích xuất văn bản.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    return "".join(page.extract_text() for page in reader.pages)


def extract_text_from_docx(docx_file) -> str:
    """
    Trich xuất văn bản từ tệp DOCX.
    :param docx_file: Tệp DOCX để trích xuất văn bản.
    """
    doc = Document(docx_file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def extract_text_from_file(file) -> list:
    """
    Trich xuất văn bản từ tệp (hình ảnh, PDF, DOCX) và phân đoạn văn bản thành các phần.
    :param file: Tệp để trích xuất văn bản.
    :return: Danh sách các phần văn bản đã phân đoạn.
    """
    # Trich xuất văn bản từ tệp
    if hasattr(file, 'filename'):
        if file.filename.endswith(('.png', '.jpg', '.jpeg')):
            raw_text = extract_text_from_image(file)
        elif file.filename.endswith('.pdf'):
            raw_text = extract_text_from_pdf(file)
        elif file.filename.endswith('.docx'):
            raw_text = extract_text_from_docx(file)
        else:
            raise ValueError("File không đúng định dạng (PNG/JPG/PDF/DOCX)")
    else:
        # Nếu file không phải là tệp, giả sử nó là một chuỗi văn bản
        raw_text = file if isinstance(file, str) else str(file)

    # Phân đoạn văn bản
    return segment_text(raw_text)


def segment_text(text) -> list:
    """
    Phân đoạn văn bản thành các phần nhỏ hơn dựa trên các quy tắc phân đoạn.
    :param text: Văn bản cần phân đoạn.
    :return: Danh sách các phần văn bản đã phân đoạn.
    """
    # Sử dụng regex để phân đoạn văn bản thành các phần nhỏ hơn
    segments = re.split(r'\n\s*\n', text)

    # Loại bỏ các phần trống và khoảng trắng thừa
    segments = [seg.strip() for seg in segments if seg.strip()]

    # Nếu không có phần nào được phân đoạn, trả về văn bản gốc
    if not segments:
        return [text.strip()] if text.strip() else []

    return segments
