import cv2


def analyse_image(image_path):
    """
    Placeholder for AI object detection.
    Replace with YOLO / ML model later.
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Dummy detection example
    detections = [
        {
            "label": "building",
            "confidence": 0.82,
            "box": [int(width * 0.2), int(height * 0.3), 200, 150]
        }
    ]

    return detections
