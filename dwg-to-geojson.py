# -------------------------------------------------------------------------------
# Name:        DWG to JSON
# Purpose:     Convert user provided dwg file to geoJSON format
#
# Author:      Abdur Rahman Muhammad Abdul Majid
#
# Created:     05/06/2022
# Copyright:   (c) amuhammad 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------

# Import arcpy site-package
#
# sourcery skip: use-fstring-for-formatting
import arcpy
import os
import re
from arcgis2geojson import arcgis2geojson

# Read the parameter values:
#  1: input DWG file
#  2: input Geometry type
dwgFilePath = arcpy.GetParameterAsText(0)
geometryType = arcpy.GetParameterAsText(1)


arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

# Output parameter values:
#  1: output JSON file path
outJsonFile = arcpy.GetParameterAsText(2)

# root directory in your sever where you are publishing the script
rootPath = "C:\\Documents\\scratch"

# get file name and its path in separate varibles
filename = os.path.basename(dwgFilePath)
filePath = os.path.dirname(dwgFilePath)

# replace any hyphens/dash('-') in file name with underscore('_') as not allowed in valid shp file name
filename = filename.replace("-", "_")

# new file name complete path
newFileNamePath = filePath + '\\' + filename

# rename file
os.rename(dwgFilePath, newFileNamePath)

# file only file name and remove the extension to be used for naming new files
filename = re.sub('.dwg$', '', filename, flags=re.IGNORECASE)

dwgFilePath = newFileNamePath + '\\' + geometryType

outputFilename = "{0}_DWG_{1}.shp".format(filename, geometryType)

arcpy.FeatureClassToShapefile_conversion(dwgFilePath, rootPath)

# get list of file after file conversion to shapefile
filesAfterShapefile = os.listdir(rootPath)

# generate complete path for the new shapefile
shpFilePath = rootPath + outputFilename

# generate new file name for the JSON file
outJsonFilePath = rootPath + filename + ".json"

arcpy.FeaturesToJSON_conversion(shpFilePath, outJsonFilePath, format_json=None,
                                include_z_values=None, include_m_values=None, geoJSON=False)

geoJsonFilePath = rootPath + filename + ".geojson"

# create a file and add write the converted json to geojson
with open(geoJsonFilePath, 'w') as geoJsonFile, open(outJsonFilePath, 'r') as jsonFile:
    for line in jsonFile:
        testvar = line
        output = arcgis2geojson(testvar)
        geoJsonFile.write(output)

# get list of file only with the current file name for clean up
newFileList = [
    file for file in filesAfterShapefile if file.startswith(filename)]

# delete unwanted file
for file in newFileList:
    # fileText, fileExtension = os.path.splitext(file)
    # if(fileExtension != '.json'):
    tempFilePath = rootPath + file
    os.remove(tempFilePath)

arcpy.SetParameterAsText(2, geoJsonFilePath)
