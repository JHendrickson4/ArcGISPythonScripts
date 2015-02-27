import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

if arcpy.env.overwriteOutput:
  print "Overwrite Output is true!"
else:
  print "Overwrite Output is false!"

#Start Code here

print "Set Variables"
env.workspace = raw_input("Workspace path: ")
datapath = env.workspace
mxd = arcpy.mapping.MapDocument(raw_input("Map document path: "))
LayerName = raw_input("Enter the layer name to be symbolized: ")
SymValue = raw_input("Enter the field name to be used for symbolization: ")
ClassNum =  raw_input("Enter the number of classes to be set for the GRADUATED COLORS: ")
CalcValue = raw_input("Enter the field name for the resulting calculated class ID value: ")

print "Start Processing"
## List layers in the map document, adjust the symbology classes, 
## and use the symbol class values to calculate a value in the attribute table
for df in arcpy.mapping.ListDataFrames(mxd, "*"):
  for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.name == LayerName:
      if lyr.symbologyType == "GRADUATED_COLORS":
        lyr.symbology.valueField = SymValue
        lyr.symbology.numClasses = int(ClassNum)
        for idx, item in enumerate(lyr.symbology.classBreakValues):
          if idx <= len(lyr.symbology.classBreakValues):
            try:
              print "Class number " + str(idx+1)
              Selection = SymValue + " >= " + str(round(lyr.symbology.classBreakValues[idx],6)) + " AND " + SymValue + " <= " + str(round(lyr.symbology.classBreakValues[(idx+1)],6))
              print Selection
              arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", Selection)
              arcpy.CalculateField_management(lyr, CalcValue, str(idx+1), "PYTHON_9.3")
            except:
              print "The previous class (" + "Class number " + str(idx+1)+ ") was NULL, thus resulting in a value of 0"
              Selection = SymValue + " IS NULL"
              print Selection
              arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", Selection)
              arcpy.CalculateField_management(lyr, CalcValue, 0, "PYTHON_9.3")
              arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
mxd.save()
del mxd
print "Process Completed"


