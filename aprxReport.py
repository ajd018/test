import arcpy
import csv
import collections
import pandas as pd

# aprx = arcpy.mp.ArcGISProject("C:/Users/adartez/Desktop/report/MMPK_EntergyElectric_AR.aprx")
aprx = arcpy.mp.ArcGISProject("//jdcapetsd840/d$/EpochField_DataPrep_400/data_staging/aprx/VTPK_EntergyElectric_AR/VTPK_EntergyElectric_AR.aprx")
Layerlist = []
scales = []
m = aprx.listMaps()[0]
layers = m.listLayers()
# iterate Layer names
for layer in layers:
    if layer.supports("dataSource"):
        d = [str(layer)]
        s = [str(layer.dataSource)]
        for LayerSplit in d:
            # seperating group name from layer name
            test = []
            SPLIT = LayerSplit.split("\\")
            # adding in datasources
            SPLIT.extend(s)
            # Cleaning up strings
            SPLIT = [s.replace(' - Containers', '') for s in SPLIT]
            SPLIT = [s.replace('1:', '') for s in SPLIT]
            SPLIT = [s.replace(',', '') for s in SPLIT]
            # adding annotation checker
            if 'Annotation' in str(SPLIT):
                SPLIT.insert(len(SPLIT), "Yes")
            else:
                SPLIT.insert(len(SPLIT), "No")
            # removing extra group name
            SPLIT = [x for x in SPLIT if x != 'Annotation']
            SPLIT = [x for x in SPLIT if x != 'Annotations']
            test.append(SPLIT)
            # pass layer list to global variable
            for c in test:
                Layerlist.append(c)

            splitList = []
            splitList.append(SPLIT[0])
            # pass scales to global variable
            for a in splitList:
                scales.append(a)

# create one of each scale and sort in order
myset = list(set(scales))
myset.sort(key=float)
# add scale list to each layer list
res = [sub + myset for sub in Layerlist]
# getting true/false for matching scale names.
TrueFalseList = [[x[1], x[2], x[3]] + [str(y==x[0]) for y in x[4:]] for x in res]
# swapping false with empty space for condensing list in next step
TrueFalseList = [[x.replace('False','') for x in l] for l in TrueFalseList]

# create dictionary from list. Condense layer list
csv_dict = collections.defaultdict(list)

for key,*rest in TrueFalseList:
    for i,r in enumerate(rest):
        if r:
            d = csv_dict[key]
            while i>=len(d):
                d.append("")
            d[i] = r

# create csv report from dict
out_path = 'C:/Users/adartez/Desktop/APRXreport.csv'
headernames = ["datasource", "annotation"] + myset
(pd.DataFrame.from_dict(data=csv_dict, orient='index', columns=headernames)
   .to_csv(out_path, header=True))






