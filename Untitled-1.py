import arcpy


aprx = arcpy.mp.ArcGISProject("c:/users/adartez/desktop/MMPK_EntergyElectric_AR.aprx")

scales = []
#listNavn = list(set(list(str(lyr) for lyr in m.listLayers())))
m = aprx.listMaps()[0]
layers = m.listLayers()
# iterate Layer names
for layer in layers:
    if layer.supports("dataSource"):
        d = [str(layer)]
        for LayerSplit in d:
            # seperating group name from layer name
            SPLIT = LayerSplit.split("\\")
            splitList = []
            splitList.append(SPLIT[0])
            for a in splitList:
                scales.append(a)
myset = list(set(scales))
g = [x.split(':')[1] for x in myset]
words = [w.replace(' - Containers', '') for w in g]
comma = [s.replace(',', '') for s in words]
comma.sort(key=float)
print (comma)


