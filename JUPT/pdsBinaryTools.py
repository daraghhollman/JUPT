import functools
import struct
from datetime import datetime

import numpy as np


def ReadLabel(labelFilePath):
    with open(labelFilePath) as labelFile:
        fileKeys = [
            line.strip("\n/* RJW, ") for line in labelFile if line.startswith("/* RJW")
        ]
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
            "shape": tuple(map(int, shape)),
        }
    return (labelInfo, structClass)


def ReadBinary(binaryFilePath, structClass, labelInfo, labelsWanted="notImplemented"):
    startTime = []
    midTime = []
    endTime = []
    spectra = []
    dataUnits = []
    energyScale = []
    pitchAngleScale = []
    timeOfFlightScale = []
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
                length = functools.reduce(lambda x, y: x * y, labelInfo[name]["shape"])

                dataDictionary[name]["data"] = data[
                    dataPosition : (dataPosition + length)
                ]
                dataPosition += length

            utcStart = dataDictionary["DIM0_UTC_LOWER"]["data"]
            utcMid = dataDictionary["DIM0_UTC"]["data"]
            utcEnd = dataDictionary["DIM0_UTC_UPPER"]["data"]

            convertedUtcStart = datetime.strptime(
                "".join([time.decode("utf-8") for time in utcStart]),
                "%Y-%jT%H:%M:%S.%f",
            ).strftime("%Y-%m-%dT%H:%M:%S.%f")
            convertedUtcMid = datetime.strptime(
                "".join([time.decode("utf-8") for time in utcMid]), "%Y-%jT%H:%M:%S.%f"
            ).strftime("%Y-%m-%dT%H:%M:%S.%f")
            convertedUtcEnd = datetime.strptime(
                "".join([time.decode("utf-8") for time in utcEnd]), "%Y-%jT%H:%M:%S.%f"
            ).strftime("%Y-%m-%dT%H:%M:%S.%f")

            startTime.append(convertedUtcStart)
            midTime.append(convertedUtcMid)
            endTime.append(convertedUtcEnd)

            spectra.append(
                np.array(dataDictionary["DATA"]["data"]).reshape(
                    dataDictionary["DATA"]["shape"]
                )
            )
            dataUnits.append(dataDictionary["DATA_UNITS"]["data"])
            energyScale.append(
                np.array(dataDictionary["DIM1_E"]["data"]).reshape(
                    dataDictionary["DIM1_E"]["shape"]
                )
            )

            if "DIM3_PITCH_ANGLES" in dataDictionary:
                pitchAngleScale.append(
                    np.array(dataDictionary["DIM3_PITCH_ANGLES"]["data"]).reshape(
                        dataDictionary["DIM3_PITCH_ANGLES"]["shape"]
                    )
                )

            if "DIM3_TOF" in dataDictionary:
                timeOfFlightScale.append(
                    np.array(dataDictionary["DIM3_TOF"]["data"]).reshape(
                        dataDictionary["DIM3_TOF"]["shape"]
                    )
                )

    return {
        "startTime": startTime,
        "midTime": midTime,
        "endTime": endTime,
        "data": spectra,
        "data units": dataUnits[0],
        "energy scale": energyScale[0],
        "pitch angle scale": pitchAngleScale,
        "time of flight": timeOfFlightScale,
    }
