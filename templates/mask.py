import cv2
import pytesseract

def mask_sensitive_info(input_image_path, output_image_path):
    # Load image and convert to grayscale
    image = cv2.imread(input_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    field_labels = ['name', 'ssn', 'dob', 'address', 'id no', 'id']

    n = len(data['text'])

    for i in range(n):
        word = data['text'][i].strip().lower().replace(':', '')
        try:
            conf = int(float(data['conf'][i]))
        except:
            conf = 0

        if word in field_labels and conf > 60:
            label_top = data['top'][i]
            label_left = data['left'][i]
            label_height = data['height'][i]

            # Check all words on the same line and to the right
            for j in range(n):
                try:
                    conf_j = int(float(data['conf'][j]))
                except:
                    conf_j = 0

                if conf_j > 60:
                    val_top = data['top'][j]
                    val_left = data['left'][j]
                    if abs(val_top - label_top) < label_height and val_left > label_left + 30:
                        x, y = data['left'][j], data['top'][j]
                        w, h = data['width'][j], data['height'][j]
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

    # Save the masked image
    cv2.imwrite(output_image_path, image)
    return output_image_path