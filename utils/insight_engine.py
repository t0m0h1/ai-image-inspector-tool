def generate_insights(detections, exif):
    insights = []

    if detections:
        for d in detections:
            insights.append(
                f"Detected {d['label']} with {int(d['confidence'] * 100)}% confidence."
            )
    else:
        insights.append("No significant objects detected.")

    if "latitude" in exif and "longitude" in exif:
        insights.append("Image contains valid GPS location data.")

    if exif.get("altitude") != "Unknown":
        insights.append("Altitude data is available.")

    return insights
