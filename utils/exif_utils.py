from PIL import Image
import exifread


def _convert_to_degrees(value):
    d = float(value[0].num) / float(value[0].den)
    m = float(value[1].num) / float(value[1].den)
    s = float(value[2].num) / float(value[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def extract_exif(image_path):
    data = {}

    with open(image_path, "rb") as f:
        tags = exifread.process_file(f)

    try:
        lat = tags.get("GPS GPSLatitude")
        lat_ref = tags.get("GPS GPSLatitudeRef")
        lon = tags.get("GPS GPSLongitude")
        lon_ref = tags.get("GPS GPSLongitudeRef")

        if lat and lon:
            latitude = _convert_to_degrees(lat.values)
            longitude = _convert_to_degrees(lon.values)

            if lat_ref.values != "N":
                latitude = -latitude
            if lon_ref.values != "E":
                longitude = -longitude

            data["latitude"] = latitude
            data["longitude"] = longitude
    except Exception:
        pass

    data["camera"] = str(tags.get("Image Model", "Unknown"))
    data["timestamp"] = str(tags.get("EXIF DateTimeOriginal", "Unknown"))
    data["altitude"] = str(tags.get("GPS GPSAltitude", "Unknown"))

    return data
