# -------------------------------------------------------------------------------
# Name:        DWG to JSON
# Purpose:     Convert user provided dwg file to geoJSON format
#
# Author:      Abdur Rahman Muhammad Abdul Majid
#
# Created:     05/06/2022
# Copyright:   (c) amuhammad 2022
# Licence:     MIT (see LICENSE)
# -------------------------------------------------------------------------------

# Import arcpy site-package
import arcpy
import os
import shutil
from arcgis2geojson import arcgis2geojson

# Read the parameter values:
#  0: input DWG file
#  1: input Geometry type
dwgFilePath = arcpy.GetParameterAsText(0)
geometryType = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

# Output parameter value:
#  2: output GeoJSON file path (set at the end of the script)

# folder for temporary and output files
rootPath = arcpy.env.scratchFolder

# Hyphens are not allowed in shapefile names, so work on a copy of the DWG
# with underscores. The user's input file is not touched.
filename = os.path.basename(dwgFilePath).replace("-", "_")
workDwgPath = os.path.join(rootPath, filename)
shutil.copyfile(dwgFilePath, workDwgPath)

# file name without the extension, used for naming new files
filename = os.path.splitext(filename)[0]

dwgFeatureClass = os.path.join(workDwgPath, geometryType)

outputFilename = "{0}_DWG_{1}.shp".format(filename, geometryType)

arcpy.FeatureClassToShapefile_conversion(dwgFeatureClass, rootPath)

# list of files after the shapefile conversion, used for clean up
filesAfterShapefile = os.listdir(rootPath)

shpFilePath = os.path.join(rootPath, outputFilename)
outJsonFilePath = os.path.join(rootPath, filename + ".json")

arcpy.FeaturesToJSON_conversion(shpFilePath, outJsonFilePath, format_json=None,
                                include_z_values=None, include_m_values=None, geoJSON=False)

geoJsonFilePath = os.path.join(rootPath, filename + ".geojson")

# convert the Esri JSON to GeoJSON
with open(outJsonFilePath, 'r') as jsonFile:
    geoJson = arcgis2geojson(jsonFile.read())
with open(geoJsonFilePath, 'w') as geoJsonFile:
    geoJsonFile.write(geoJson)

# delete the temporary files created by this run
os.remove(outJsonFilePath)
for file in filesAfterShapefile:
    if file.startswith(filename) and file != filename + ".geojson":
        os.remove(os.path.join(rootPath, file))

arcpy.SetParameterAsText(2, geoJsonFilePath)
