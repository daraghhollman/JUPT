import struct
import functools
import numpy as np
from datetime import datetime


def ReadLabel(labelFilePath):

    with open(labelFilePath) as labelFile:
        fileKeys = [line.strip("\n/* RJW, ") for line in labelFile if line.startswith("/* RJW")]
        fileKeys = [line.strip(" */\n") for line in fileKeys]

        fileFormat = fileKeys[0:2]
        fileKeys = fileKeys[2:]

    labelInfo = {}
    structFormat = "="
    for i, key in enumerate(fileKeys):
    
        name, format, numberOfDimensions, *shape = key.split(", ")

        # Creates format to read the binary, i.e. "= 21c 1B 21c 1b 1H 3072f..."
        structFormat = f"{structFormat} {functools.reduce(lambda x, y: x*y, map(int, shape))}{format}"
        structClass = struct.Struct(structFormat)

        labelInfo[name] = {
            "format": format,
            "numberOfDimensions": int(numberOfDimensions),
            "shape": tuple(map(int, shape))
        }
    return (labelInfo, structClass)


def ReadBinary(binaryFilePath, structClass, labelInfo, labelsWanted="notImplemented"):
    
    time = []
    spectra = []
    with open(binaryFilePath, "rb") as binaryFile:
        while True:
            # if n == 3:
                # break

            chunk = binaryFile.read(structClass.size)
            if not chunk:
                break

            data = structClass.unpack(chunk)

            dataPosition = 0

            dataDictionary = labelInfo
            for name in labelInfo.keys():
                length = functools.reduce(lambda x, y: x*y, labelInfo[name]["shape"])

                dataDictionary[name]["data"] = data[dataPosition:(dataPosition+length)]
                dataPosition += length


            utc = dataDictionary["DIM0_UTC"]["data"]
            convertedUtc = datetime.strptime(''.join([time.decode('utf-8') for time in utc]), '%Y-%jT%H:%M:%S.%f').strftime("%Y-%m-%dT%H:%M:%S.%f")
            # print(convertedUtc)

            time.append(convertedUtc)
            spectra.append(np.array(dataDictionary["DATA"]["data"]).reshape(dataDictionary["DATA"]["shape"]))
        
    return {
        "time": time,
        "spectra": spectra
    }
