import cv2
import easyocr

# Load the EasyOCR reader once
reader = easyocr.Reader(["en"], gpu=False)

def preprocess_image(image_path: str):
    """Improve image quality for OCR."""
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    blur = cv2.medianBlur(gray, 3)

    # Increase contrast (optional)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

def extract_text(image_path: str) -> str:
    """
    Extract text from a food label image using EasyOCR with preprocessing.
    """
    processed_img = preprocess_image(image_path)

    # EasyOCR can also take numpy arrays
    results = reader.readtext(processed_img, detail=0)

    return " ".join(results)
