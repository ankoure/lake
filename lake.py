#Stage 1 Raster math (Greater Than x Stage Value)

# Import system modules
import arcpy
from arcpy import env
from arcpy.ia import *
from arcpy.sa import *
# Set environment settings
env.workspace = "D:\\SalemState\\Python\\FinalProject\\Test.gdb"
arcpy.env.overwriteOutput=True
#need to pull lake stage as an external function i.e from a csv or rdb
lakestage = 250
lakestagestr = str(lakestage)
lakebathym = "D:\\SalemState\\Python\\FinalProject\\Test.gdb\\DL_Bathym"
outputgdb = "D:\\SalemState\\Python\\FinalProject\\Test.gdb\\"
GTEname = "GTE_" + lakestagestr 

# Set local variables
#This should be hardcoded and specified at beginning of work
inRaster1 = lakebathym
#inRaster2 = lakestage variable for int value of lakestage
inRaster2 = lakestage

# Execute GreaterThanEqual
outGTE = GreaterThanEqual(inRaster1, inRaster2)

# Save the output 
outGTE.save(outputgdb + GTEname)



#Stage 2 raster to polygon
#Convert Lake Stage raster to Polygon
GTEPolyname = "Poly_" + lakestagestr  
# Set local variables
inRaster = outGTE
outPolygons = outputgdb + GTEPolyname
field = "Value"

# Execute RasterToPolygon
RatoPoly = arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)
#save
RatoPolyname = "RatoPoly_" + lakestagestr

#RatoPoly.save(outputgdb + RatoPolyname)

# #Stage 3 Feature Class to Feature Class 
# # Removes unesscary data from raster, only preserves values = 0 where the new lake stage exists.  
# FeaExName = RatoPolyname + "_FeaEx"
# # Set local variables
# inFeatures = outPolygons
# outLocation = outputgdb
# #Need Name function for outFeatureClass
# outFeatureClass = FeaExName
# delimitedField = arcpy.AddFieldDelimiters(arcpy.env.workspace, "Gridcode")
# expression = delimitedField + "0"
# # Execute FeatureClassToFeatureClass
# FeaEx = arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)
# FeaEx.save(outputgdb + FeaExName)


# Name: ExtractFeaturesByLocationAndAttribute.py
# Description: Extract features to a new feature class based on a spatial 
# relationships to another layer, and an attribute query
FeaExName = "FeaEx_" + lakestagestr
FeaEx = arcpy.SelectLayerByAttribute_management(outPolygons, 'NEW_SELECTION', '"gridcode" = 0')
# Write the selected features to a new featureclass
arcpy.CopyFeatures_management(FeaEx, FeaExName)



# Name: PolygonToRaster_Ex_02.py
# Description: Converts polygon features to a raster dataset.

# Set local variables
PoRaName = "PotoRa_" + lakestagestr
inFeatures = FeaExName
valField = "gridcode"
outRaster = outputgdb + PoRaName
assignmentType = "CELL_CENTER"
priorityField = "NONE"
cellSize = 1

# Execute PolygonToRaster
#arcpy.PolygonToRaster_conversion("D:\\SalemState\\Python\\FinalProject\\Thesis.gdb\\newlakestage", "gridcode", "D:\\SalemState\\Python\\FinalProject\\Thesis.gdb\\newlakestageraster.tiff", "CELL_CENTER","NONE", 1)
PoRa = arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
#PoRa.save(outputgdb + PoRaName)


# Name: Cutfill_Ex_02.py
# Description: Calculates the volume and area of cut and 
#              fill locations.
# Requirements: Spatial Analyst Extension

#Local variables for Cutfill
inBeforeRaster = lakebathym
inAfterRaster =  outRaster
zFactor = 0.5
cutfillname = "cutfill_" + lakestagestr
# Execute CutFill
outCutFill = CutFill(inBeforeRaster, inAfterRaster, zFactor)
outCutFill.save(outputgdb + cutfillname)