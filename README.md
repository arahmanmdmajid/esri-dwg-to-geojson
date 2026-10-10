# esri-dwg-to-geojson

An ArcPy script tool that converts one geometry type of an AutoCAD DWG file into GeoJSON (WGS 84).

## What it does

1. Takes a DWG file and a geometry type (for example `Polyline`).
2. Converts that CAD feature class to a shapefile.
3. Converts the shapefile to Esri JSON.
4. Converts the Esri JSON to GeoJSON with [arcgis2geojson](https://pypi.org/project/arcgis2geojson/).
5. Deletes the temporary shapefile files and returns the path of the `.geojson` file.

The output coordinate system is set to WGS 84 (EPSG:4326).

## Requirements

- ArcGIS with `arcpy` (written for ArcGIS Desktop 10.8, Python 2.7). Not tested in ArcGIS Pro.
- Python package `arcgis2geojson`:

```
pip install -r requirements.txt
```

## Parameters

Set these up when you add the script as a script tool:

| # | Name | Type | Notes |
|---|------|------|-------|
| 0 | Input DWG file | File | Path to the `.dwg` file |
| 1 | Geometry type | String | A CAD feature class name: `Point`, `Polyline`, `Polygon`, `Annotation` or `MultiPatch` |
| 2 | Output file | File (derived output) | Set by the script to the `.geojson` path |

## Usage

1. In ArcGIS, add `dwg-to-geojson.py` as a script tool with the three parameters above.
2. Run it with a DWG file and a geometry type.
3. Read the GeoJSON file from the output parameter.

The script can also be published as a geoprocessing service. See the note on the scratch folder below.

## Notes

- Temporary files and the output are written to the ArcGIS scratch folder (`arcpy.env.scratchFolder`).
- The input DWG is copied to the scratch folder first. Your original file is not changed.
- Run it once per geometry type. A DWG with several geometry types needs one run for each.

## License

[MIT](LICENSE)
