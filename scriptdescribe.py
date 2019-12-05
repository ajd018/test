import arcpy
import os
import csv
from itertools import chain

# directory being reported
rootDir = '//jdcapetsd840/d$/EpochField_DataPrep_400/data_staging/aprxlayer/MMPK_EntergyElectric_AR'

# iterate through folders.
for dirName, subdirList, fileList in os.walk(rootDir):
    for file in fileList:
        if file.endswith(".aprx"):
            FullPath = (os.path.join(dirName, file))
            APRXname = file
            aprx = arcpy.mp.ArcGISProject(os.path.join(FullPath))
            m = aprx.listMaps()[0]
            layers = m.listLayers()
            # iterate Layer names
            scalelist = []
            TopReportList = []
            for layer in layers:
                if layer.supports("dataSource"):
                    # create list of layer names
                    d = [str(layer)]
                    for LayerSplit in d:
                        # seperating group name from layer name
                        SPLIT = LayerSplit.split("\\")
                        # create list of aprx names and data sources. extend list with group and layer names
                        ReportList = [str(APRXname), str(layer.dataSource)]
                        ReportList.extend(SPLIT)
                        # look for annotation layers
                        if 'Annotation' in str(ReportList):
                            ReportList.insert(len(ReportList), "Yes")
                        else:
                            ReportList.insert(len(ReportList), "No")
                        # remove annotation from position 2 in list
                        ReportList = [x for x in ReportList if x != 'Annotation']
                        ReportList = [x for x in ReportList if x != 'Annotations']
                        ReportList = [s.replace(',', '') for s in ReportList]
                        TopReportList.append(ReportList)
                        # sort by group number

                        sublist = []
                        sublist.append(ReportList[2])
                        for a in sublist:
                            scalelist.append(a)

                        

            myset = list(set(scalelist))
            g = [x.split(':')[1] for x in myset]
            words = [w.replace(' - Containers', '') for w in g]
            words.sort(key=float)
            TopReportList.append(words)
            print (TopReportList)

                    




