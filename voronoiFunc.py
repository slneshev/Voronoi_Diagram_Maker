import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union
from shapely.geometry import Point
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from pyproj import Transformer, CRS
import shapely.ops as ops
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import shapely.geometry.multipolygon
import os
import re
from math import sqrt, pi
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
def addAreaAndRadius(gdf, progressLabel):
    crs = CRS.from_epsg(4326)
    if 'Voronoi Polygon' in gdf.columns:
        progressLabel.setText('Changing geometry...')
        gdf.set_geometry(col="Voronoi Polygon", inplace=True)
        if 'geometry' in gdf.columns:
            gdf.drop(columns=['geometry'], inplace=True)
        progressLabel.setText('Done.')
        progressLabel.setText('Calculating area...')
        gdf['Area in squared km'] = gdf['Voronoi Polygon'].apply(lambda x: transf(x, crs).area) #slow row
        progressLabel.setText('Done.')
        gdf['Radius in metres'] = gdf['Area in squared km'].apply(lambda x: round(sqrt(x / pi), 3))
        progressLabel.setText('Calculating radius...')
        gdf['Area in squared km'] = gdf['Area in squared km'].apply(lambda x: round(x / 1e6, 3))
        progressLabel.setText('Finished.')
    else:
        progressLabel.setText('Calculating area...')
        gdf['Area in squared km'] = gdf['geometry'].apply(lambda x: transf(x, crs).area) #slow row
        progressLabel.setText('Done.')
        gdf['Radius in metres'] = gdf['Area in squared km'].apply(lambda x: round(sqrt(x / pi), 3))
        progressLabel.setText('Calculating radius...')
        gdf['Area in squared km'] = gdf['Area in squared km'].apply(lambda x: round(x / 1e6, 3))
        progressLabel.setText('Finished.')
    return gdf

def createVoronoiNotCombined(mapPath, longitude, latitude, soaPath, progressLabel):
    progressLabel.setText("Loading files...")
    sitesFile = pd.read_excel(open(soaPath, 'rb'))
    bulgMapData = gpd.read_file(mapPath)
    bulgMapData.to_crs("EPSG:4326", inplace=True)
    progressLabel.setText("Creating voronoi...")
    gdf, poly_shapes, pts, coords = voronoiCreator(longitude, latitude, sitesFile, bulgMapData, soaPath, progressLabel)
    progressLabel.setText('Done.')
    progressLabel.setText('Formating GDF...')
    gdf = gdfFormatter(gdf, coords, poly_shapes, pts, longitude, latitude)
    gdf.set_geometry(col="Voronoi Polygon", inplace=True)
    gdf.drop(columns="geometry", inplace=True)
    progressLabel.setText('Finished.')
    return gdf

def fileNamer(exportPath, fileName, extension, separator = "_#"):
    separator = separator.replace('#', '')
    specialChars = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', '\\']
    if len(separator) == 1:
        if os.path.exists(exportPath+f"\{fileName}"+'.'+extension):
            fileLst = []
            for file in os.listdir(exportPath):
                if (separator in specialChars):
                    # когато разделителя е един от специалните
                    # символи трябва да се сложи \ преди променливата
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(f'{fileName}\{separator}\d*.{extension}', file):
                        fileLst.append(file)
                else:
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(f'{fileName}{separator}\d*.{extension}', file):
                        fileLst.append(file)
            if (len(fileLst) == 1) and (fileLst[0] == f'{fileName}.{extension}'):
                finalName = exportPath + f'/{fileName}{separator}1' + f'.{extension}'
            else:
                maxNum = 0
                for filename in fileLst:
                    numberAtTheEnd_ext = re.search(fr'\d+.{extension}', filename)  # изтегля всички числа накрая заедно с ext
                    # ползвам го по този начин, защото може да има други числа в името, които не са накрая
                    if numberAtTheEnd_ext is not None:
                        numberAtTheEnd = re.findall(r'\d*', numberAtTheEnd_ext.group(0))  # изтеглям поредния номер на файла
                        if int(numberAtTheEnd[0]) > maxNum:
                            maxNum = int(numberAtTheEnd[0])
                maxNum = maxNum + 1
                finalName = exportPath + f'/{fileName}{separator}' + str(maxNum) + f'.{extension}'
        else:
            finalName = exportPath + f'/{fileName}' + f'.{extension}'
    else:
        separatorFirstHalf = separator[0]
        separatorSecondHalf = separator[1]
        specialChars = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', '\\']
        if os.path.exists(exportPath + fr"\{fileName}" + '.' + extension):
            fileLst = []
            for file in os.listdir(exportPath):
                if (separatorFirstHalf in specialChars) and (separatorSecondHalf in specialChars):
                    # когато разделителя е един от специалните
                    # символи трябва да се сложи \ преди променливата
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(fr'{fileName}\{separatorFirstHalf}\d*\{separatorSecondHalf}.{extension}', file):
                        fileLst.append(file)
                else:
                    if re.findall(f'{fileName}.{extension}', file) or re.findall(fr'{fileName}{separatorFirstHalf}\d*{separatorSecondHalf}.{extension}', file):
                        fileLst.append(file)
            if (len(fileLst) == 1) and (fileLst[0] == f'{fileName}.{extension}'):
                finalName = exportPath + f'/{fileName}{separatorFirstHalf}1{separatorSecondHalf}' + f'.{extension}'
            else:
                maxNum = 0
                for filename in fileLst:
                    if (separatorFirstHalf in specialChars) and (separatorSecondHalf in specialChars):
                        numberAtTheEnd_ext = re.search(fr'\{separatorFirstHalf}\d+\{separatorSecondHalf}.{extension}', filename)  # изтегля всички числа накрая заедно с ext
                    # ползвам го по този начин, защото може да има други числа в името, които не са накрая
                    else:
                        numberAtTheEnd_ext = re.search(fr'{separatorFirstHalf}\d+{separatorSecondHalf}.{extension}', filename)  # изтегля всички числа накрая заедно с ext
                    if numberAtTheEnd_ext is not None:
                        numberAtTheEndLst = re.findall(r"\d*",numberAtTheEnd_ext.group())  # изтеглям поредния номер на файла
                        for ele in numberAtTheEndLst:
                            if ele != '':
                                numberAtTheEnd = ele
                        if int(numberAtTheEnd) > maxNum:
                            maxNum = int(numberAtTheEnd)
                maxNum = maxNum + 1
                finalName = exportPath + f'/{fileName}{separatorFirstHalf}' + str(maxNum) + f'{separatorSecondHalf}.{extension}'
        else:
            finalName = exportPath + f'/{fileName}' + f'.{extension}'
    return finalName

#excel export
def excelExport(gdf, exportPath, prop):
    if exportPath == "" or os.path.isdir(exportPath) is False:
        exportPath = desktop
    print('Exporting excel table in: ', exportPath)
    if len(prop) == 0:
        excelName = fileNamer(exportPath, 'Sites_On_Air_Voronoi', 'xlsx')
        gdf.to_excel(excelName)
        return False
    else:
        flag = False
        for value in gdf['geometry']:
            value = str(value)
            if len(value) > 32766:
                flag = True
                break
        if flag is True:
            writePath = fileNamer(exportPath, f'{prop}', 'txt')
            gdf.to_csv(writePath, index=False, sep='\t')
            return True
        else:
            excelName = fileNamer(exportPath, f'{prop}', 'xlsx')
            gdf.to_excel(excelName)
            return False
    print('Finished.')

#map info export
def mapInfoExport(gdf, mapInfoPath, prop):
    if mapInfoPath == "" or os.path.isdir(mapInfoPath) is False:
        mapInfoPath = desktop
    schema = create_mapinfo_schema(gdf)
    if len(prop) == 0:
        exportName = fileNamer(mapInfoPath, 'Sites_On_Air_Voronoi', 'tab')
    else:
        exportName = fileNamer(mapInfoPath, f'{prop}', 'tab')
    print('Exporting MapInfo files in: ',mapInfoPath)
    gdf.to_file(exportName, driver="MapInfo File", schema=schema, encoding='CP1252')
    print('Finished.')

#прави plot на комбинирания voronoi
def plotting(figSavePath, ext, proper, gdf, numCol, polyLabelFont, polyFontWght, polyBorderWidth,
             polyEdgeColor, polyTextColor, polyHaloLineWidth, polyHaloColor, legendLoc, legendFontSize,
             legendTitleFontSize, legendMarkerScale, legendFrameOn, legendFancyBox, legendFaceColor,
             legendLabelColor, legendMarkerFirst, legendOption, polyCmapBelow10, polyCmapBelow20,
             polyCmapAbove20, figAxis, flag, dpi_from_input):
    if figSavePath == "" or os.path.isdir(figSavePath) is False:
        figSavePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    try:
        dpi_from_input = int(dpi_from_input)
    except:
        dpi_from_input = 1200
    if flag is True:
        try:
            numCol = int(numCol)
        except:
            numCol = 1
        try:
            polyLabelFont = int(polyLabelFont)
        except:
            polyLabelFont = 4
        try:
            polyBorderWidth = int(polyBorderWidth)
        except:
            polyBorderWidth = 0.2
        if polyEdgeColor == "":
            polyEdgeColor = 'black'
        if polyTextColor == "":
            polyTextColor = 'black'
        try:
            polyHaloLineWidth = int(polyHaloLineWidth)
        except:
            polyHaloLineWidth = 0.4
        if polyHaloColor == "":
            polyHaloColor = 'white'
        if legendFontSize == "":
            legendFontSize = 2
        try:
            legendTitleFontSize = int(legendTitleFontSize)
        except:
            legendTitleFontSize = 3
        try:
            legendMarkerScale = int(legendMarkerScale)
        except:
            legendMarkerScale = 0.2
        if legendFaceColor == "":
            legendFaceColor = 'inherit'
        if legendLabelColor == "":
            legendLabelColor = 'black'
        if polyCmapBelow10 == "":
            polyCmapBelow10 = 'tab10'
        if polyCmapBelow20 == "":
            polyCmapBelow20 = 'tab20'
        if polyCmapAbove20 == "":
            polyCmapAbove20 = 'hsv'
        picSavePath = figSavePath #"C:\\Users\\a1bg511027\\Desktop\\"
        picSaveName = proper
        pictureSave = fileNamer(picSavePath, picSaveName, ext)
        lenGdf = len(gdf)
        numberOfColumns = numCol #бройка колони за легенда
        polygonLabelFont = polyLabelFont #размер на шрифта на лейбъла на полигона
        fontWeight = polyFontWght #вид на текста на лейбъла в полигона light/heavy
        lineWdth = polyBorderWidth #дебелина на границите на полигона
        edgeColour = polyEdgeColor #цвят на границите на полигона
        textColor = polyTextColor #цвят на текста в полигона
        haloLineWidth = polyHaloLineWidth #големина на лиините на halo ефекта
        haloColor = polyHaloColor #цвят на хало ефекта
        if lenGdf<=10:
            colorMap = polyCmapBelow10
        elif lenGdf>10 and lenGdf <=20:
            colorMap = polyCmapBelow20
        elif lenGdf>20:
            colorMap = polyCmapAbove20
        legendProperties = {
            'loc': legendLoc, #позиция на легендата
            'bbox_to_anchor': (1,0.5), #изважда легендата извън картинката
            'title': proper, #задава заглавие на легендата спрямо property
            'ncol': numberOfColumns, #задава бройка колони
            'fontsize': legendFontSize, #размер на шрифта
            'title_fontsize': legendTitleFontSize, #размер на заглавието на легендата
            'markerscale': legendMarkerScale, #размер на маркера на легендата
            'frameon': legendFrameOn, #дали легендата да има фрейм
            'fancybox': legendFancyBox, #слага закръглени ръбове на легендата
            'facecolor': legendFaceColor, #background color на легендата
            'labelcolor': legendLabelColor, #цвят на текста на легендата
            'markerfirst': legendMarkerFirst
        }

        fig, ax = plt.subplots(dpi = dpi_from_input)
        gdf.plot(
            ax = ax,
            column = proper,
            legend = legendOption,
            cmap = colorMap,
            edgecolor = edgeColour,
            linewidth = lineWdth,
            legend_kwds = legendProperties
        )
        for idx, row in gdf.iterrows():
            if type(row['geometry']) == shapely.geometry.multipolygon.MultiPolygon:
                poly = row['geometry'].geoms
                for eachPoly in poly:
                    plt.annotate(text = row[proper], xy = eachPoly.centroid.coords[0],
                                 horizontalalignment = 'center', fontsize = polygonLabelFont, color = textColor, weight = fontWeight, path_effects=[pe.withStroke(linewidth=haloLineWidth, foreground=haloColor)]) #dobavi halo
            else:
                plt.annotate(text=row[proper], xy=row['geometry'].centroid.coords[0],
                             horizontalalignment='center', fontsize=polygonLabelFont, color = textColor, weight=fontWeight, path_effects=[pe.withStroke(linewidth=haloLineWidth, foreground=haloColor)])  # dobavi halo
    else:
        pictureSave = fileNamer(figSavePath, 'Voronoi Diagram', ext)
        try:
            polyBorderWidth = int(polyBorderWidth)
        except:
            polyBorderWidth = 0.2
        if polyEdgeColor == "":
            polyEdgeColor = 'black'
        lineWdth = polyBorderWidth #дебелина на границите на полигона
        edgeColour = polyEdgeColor #цвят на границите на полигона
        lenGdf = len(gdf)
        if polyCmapBelow10 == "":
            polyCmapBelow10 = 'tab10'
        if polyCmapBelow20 == "":
            polyCmapBelow20 = 'tab20'
        if polyCmapAbove20 == "":
            polyCmapAbove20 = 'hsv'
        if lenGdf<=10:
            colorMap = polyCmapBelow10
        elif lenGdf>10 and lenGdf <=20:
            colorMap = polyCmapBelow20
        elif lenGdf>20:
            colorMap = polyCmapAbove20
        # width, height
        fig, ax = plt.subplots(dpi=dpi_from_input)
        gdf.plot(ax = ax,
                 cmap=colorMap,
                 edgecolor=edgeColour,
                 linewidth=lineWdth)
    if figAxis == False:
        ax.axis("off")
    else: ax.axis("on")
    fig.savefig(pictureSave, bbox_inches = 'tight')
    plt.close(fig)

#връща gdf с добавен voronoi poly накрая напаснат спрямо географските координати
def gdfFormatter(gdf_format, coordinates, polygon_shapes, points, longitude, latitude):
    dictVoroID_Coords = {}
    for voroID, pt in points.items():
        for i in range(len(coordinates)):
            if pt[0] == i:
                dictVoroID_Coords[voroID] = [coordinates[i, 0], coordinates[i, 1]]
    df_VoroID_Coords = pd.DataFrame.from_dict(dictVoroID_Coords, orient='index')
    df_VoroID_Coords['Coords'] = df_VoroID_Coords.apply(lambda row: str(row[0]) + "_" + str(row[1]), axis=1)
    df_poly_shapes = pd.DataFrame(columns=['Voronoi Polygon'])
    df_poly_shapes['Voronoi Polygon'] = polygon_shapes.values()
    df_Voronoi = df_VoroID_Coords.merge(df_poly_shapes, left_index=True, right_index=True)
    gdf_format["Coords"] = gdf_format.apply(lambda row: str(row[longitude]) + "_" + str(row[latitude]), axis=1)
    gdf_format = gdf_format.merge(df_Voronoi[['Coords', 'Voronoi Polygon']], left_on="Coords" ,right_on="Coords")  # , suffixes="")
    gdf_format.drop(columns="Coords", inplace=True)
    return gdf_format

# modify default GeoDataFrame schema to work correctly with MapInfo
def create_mapinfo_schema(gdf):
    print("Begin creating scheme.")
    schema = gpd.io.file.infer_schema(gdf)  # ordinarily this is inferred within gpd.to_file()
    # print(schema)
    for col, dtype in schema["properties"].items():
        # print(col, dtype)
        if dtype == 'int' or dtype == 'int64':
            schema["properties"][col] = 'int32'
        elif dtype == 'str':
            x = gdf[col].str.len().max()
            if x is np.nan:
                x = 1
            schema["properties"][col] = 'str:' + str(x)
    print('Finished.')
    return schema


#връща речник напаснат на база Property(според, което ще комбинираме във фигурата):Полигона, който се образува
def dictProp_Poly_from_df(prop, propSet, gdframe):
    dictProperty_Polygon = dict.fromkeys(propSet)
    for attri in dictProperty_Polygon.keys():
        polyLst = []
        for index, row in gdframe.iterrows():
            if row[prop] == attri:
                polyLst.append(row["Voronoi Polygon"])
        dictProperty_Polygon[attri] = polyLst
    for attri, polyLst in dictProperty_Polygon.items():
        multiPoly = unary_union(polyLst)
        dictProperty_Polygon[attri]=multiPoly
    return dictProperty_Polygon


#приема като вход Sites_On_Air и файл с шейпа на България и създава Voronoi
#връща:
#gdf - sites on air, но в gdf формат
#poly_shapes - речник на база voronoi ID:polygon
#pts - речник на база voronoi ID: point ID (мисля)
#coords - координатите на всички точки, по които е направен voronoi-a
def voronoiCreator(longitude, latitude, sitesOnAirFile, bulgMapFile, soaPath, progressLabel):
    geometry = [Point(xy) for xy in zip(sitesOnAirFile[longitude], sitesOnAirFile[latitude])]
    gdf = gpd.GeoDataFrame(sitesOnAirFile, geometry=geometry, crs="EPSG:4326")
    coordinates = points_to_coords(gdf.geometry)
    boundary_shape = unary_union(bulgMapFile.geometry)
    outsidePoints = []
    for coord in coordinates:
        coord = Point(coord)
        inside = coord.within(boundary_shape)
        if inside is False:
            coord = [coord.x, coord.y]
            outsidePoints.append(coord)
    if len(outsidePoints) > 0:
        dfOutSide = pd.DataFrame()
        for coord in outsidePoints:
            tempDf = (gdf.loc[(gdf['Longitude'] == coord[0]) & (gdf['Latitude'] == coord[1])])
            dfOutSide = pd.concat([dfOutSide, tempDf], axis=0)
        soaPath = soaPath.split('/')
        soaPath.pop(-1)
        soaPath = '\\'.join(soaPath)
        #soaPath = soaPath + '\\Sites_On_Air_OutsidePoints.xlsx'
        soaName = fileNamer(soaPath, 'Sites_On_Air_OutsidePoints', 'xlsx')
        dfOutSide.to_excel(soaName)
        progressLabel.setText("There were sites outside the border, they are extracted to separate Excel file and\nsaved under the location "
              "of Sites on air file. Voronoi will be generated without them.")
        gdf = pd.concat([gdf, dfOutSide]).drop_duplicates(keep=False)
        coordinates = points_to_coords(gdf.geometry)

    poly_shapes, pts = voronoi_regions_from_coords(coordinates, boundary_shape)
    return gdf, poly_shapes, pts, coordinates


#трансформира подадения полигон с цел правилно изчисление на площта му
def transf(geom, crs):
    transformer = Transformer.from_crs(
        crs ,
        CRS(proj='aea',
            lat_1=geom.bounds[1],
            lat_2=geom.bounds[3]
            ),
        always_xy=True
    )
    geom_area = ops.transform(transformer.transform, geom)
    return geom_area


def createVoronoiCombined(mapPath, soaPath, longitude, latitude, propOne, propTwo, progressLabel):
    bulgMapPath = mapPath #'C:\\Users\\a1bg511027\\Desktop\\Voronoi\\BG Border Fixed\\BgBorder2019_noIslands.TAB'
    sitesOnAirPath = soaPath #'C:\\Users\\a1bg511027\\Desktop\\Voronoi\\Sites On Air\\Sites_On_AirORIG.xlsx'
    if sitesOnAirPath.lower().endswith('.csv'):
        sitesFile = pd.read_csv(soaPath)
    else:
        sitesFile = pd.read_excel(open(sitesOnAirPath, 'rb'))
    bulgMapData = gpd.read_file(bulgMapPath)
    bulgMapData.to_crs("EPSG:4326", inplace=True)
    prop1 = propOne
    progressLabel.setText('Dropping columns based on properties...')
    if len(propTwo) > 0:
        prop2 = propTwo
        prop = prop1 + '_' + prop2
        sitesFile.dropna(subset=[prop1, prop2], inplace=True)
        sitesFile[prop] = sitesFile.apply(lambda row: str(row[prop1]) + "_" + str(row[prop2]), axis=1)
        sitesFile[prop] = sitesFile[prop].str.rstrip('.0')
    else:
        prop = prop1
        sitesFile.dropna(subset=[prop], inplace=True)
        sitesFile[prop] = sitesFile[prop].astype(str)
    sitesFile.reset_index(drop=True, inplace=True)
    propertySet = set(sitesFile[prop])
    progressLabel.setText('Done.')
    progressLabel.setText('Creating voronoi...')
    gdf, poly_shapes, pts, coords = voronoiCreator(longitude, latitude, sitesFile, bulgMapData, soaPath, progressLabel)
    progressLabel.setText('Done.')
    progressLabel.setText('Formating GDF stage 1/2...')
    gdf = gdfFormatter(gdf, coords, poly_shapes, pts, longitude, latitude)
    progressLabel.setText('Done.')
    #print('Result: gdf data types\n', gdf.dtypes)
    progressLabel.setText('Formating GDF stage 2/2...')
    gdf = formatGdfForPlotting(prop, propertySet, gdf)
    #print('Result: final gdf data types\n', gdf.dtypes)
    progressLabel.setText('Finished.')
    return gdf, prop

def formatGdfForPlotting(prop, propertySet, gdf):
    dictProperty_MultiPolygon = dictProp_Poly_from_df(prop, propertySet, gdf)
    gdf_plot = gpd.GeoDataFrame(columns=[prop, 'geometry'], crs="EPSG:4326")
    gdf_plot[prop], gdf_plot['geometry'] = dictProperty_MultiPolygon.keys(), dictProperty_MultiPolygon.values()
    gdf_plot[prop] = gdf_plot[prop].astype(str)
    gdf_plot[prop] = gdf_plot[prop].str.rstrip('.0')
    return gdf_plot