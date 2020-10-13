from PIL import Image, ImageFile
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif(image: Image.isImageType):
    props = {}
    i = Image.open(image)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        props[decoded] = value

    return props


def extractCoordinates(image: Image.isImageType) -> list: 
    exifValue = get_exif(image)
    latRef = exifValue['GPSInfo'][1]
    longitRef = exifValue['GPSInfo'][3]
    lat = exifValue['GPSInfo'][2]
    longit = exifValue['GPSInfo'][4]

    # geocoding
    gpsData = {
        'GPSLatitude': exifValue['GPSInfo'][2],
        'GPSLongitude': exifValue['GPSInfo'][4],
        'GPSLatitudeRef': exifValue['GPSInfo'][1],
        'GPSLongitudeRef': exifValue['GPSInfo'][3],
    }
    
    if "GPSLatitude" in gpsData:
        lat = gpsData["GPSLatitude"]
        lat = decimalCoordinatesToDegress(lat)
    if "GPSLongitude" in gpsData:
        longit = gpsData["GPSLongitude"]
        longit = decimalCoordinatesToDegress(longit)
    if "GPSLatitudeRef" in gpsData:
        latRef = gpsData["GPSLatitudeRef"]
    if "GPSLongitudeRef" in gpsData:
        longitRef = gpsData["GPSLongitudeRef"]

    if latRef is not None and latRef != "N":
        lat = 0 - lat
    if longitRef is not None and longitRef != "E":
        longit = 0 - longit

    return lat, longit


def decimalCoordinatesToDegress(coord):
    dec = float(coord[0][0])/float(coord[0][1])
    minut = float(coord[1][0])/float(coord[1][1])
    sec = float(coord[2][0])/float(coord[2][1])
    return dec+(minut/60.0)+(sec/3600.0)


def show_exif(image):
    """ Полный экзиф"""
    exif = get_exif(image)
    try:
        exif_to_print = (
            "Модель: " + exif["Make"] + " " + exif["Model"]
            + "\nСофт: " + str(exif["Software"])
            + "\nISO: " + str(int(exif["ISOSpeedRatings"]))
            + "\nВыдержка: " + str(exif['ExposureTime']._val)
            + "\nДиафрагма: " + "f/" + str(exif["FNumber"])
            + "\nФокусное расстояние: " + str(exif["FocalLength"]) + " mm"
        )
    except:
        exif_to_print = (
            "Модель: " + exif["Make"] + " " + exif["Model"]
            + "\nISO: " + str(int(exif["ISOSpeedRatings"]))
            + "\nВыдержка: " + str(exif["ExposureTime"])
            + "\nДиафрагма: " + "f/" + str(exif["FNumber"])
            + "\nФокусное расстояние: " + str(exif["FocalLength"]) + " mm"
        )

    return exif_to_print


ImageFile.LOAD_TRUNCATED_IMAGES = True


# Crop
def crop_image(image, n=1, size=None):

    # Crop center of image 100%

    imageObject = Image.open(image)
    size = imageObject.size
    W = size[0]
    H = size[1]
    left = int(W / 4)
    upper = int(H / 4)
    right = int(W / 2) + left
    lower = int(H / 2) + upper
    cropped = imageObject.crop((left, upper, right, lower))
    file_name_x1 = f"{image}_cropx{n*2}.jpeg"
    cropped.save(fp=file_name_x1)

    # Добавляем условие если нужно х4 сделать

    if n != 1:
        imageObject = Image.open(file_name_x1)
        size = imageObject.size
        W = size[0]
        H = size[1]
        left = int(W / 4)
        upper = int(H / 4)
        right = int(W / 2) + left
        lower = int(H / 2) + upper
        cropped = imageObject.crop((left, upper, right, lower))
        file_name = f"{image}_cropx{n*2}.jpeg"
        cropped.save(fp=file_name)

    return cropped
