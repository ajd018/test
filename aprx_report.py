import arcpy
import csv


aprx = arcpy.mp.ArcGISProject("c:/users/adartez/desktop/report/MMPK_EntergyElectric_AR.aprx")
newlist = []
scales = []

#listNavn = list(set(list(str(lyr) for lyr in m.listLayers())))
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
            for c in test:
                newlist.append(c)

            splitList = []
            splitList.append(SPLIT[0])
            for a in splitList:
                scales.append(a)


myset = list(set(scales))
myset.sort(key=float)
res = [sub + myset for sub in newlist]
# getting true/false for matching scale names. Also customizing new list position display
new_list = [[x[1], x[2], x[3]] + [str(y==x[0]) for y in x[4:]] for x in res]


# create csv
with open("c:/users/adartez/desktop/output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    headernames = ["LayerName", "datasource", "annotation"] + myset
    print (headernames)
    writer.writerows([headernames])
    writer.writerows(new_list)






