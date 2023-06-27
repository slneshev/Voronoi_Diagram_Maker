from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from functools import partial
from voronoiFunc import *
from plotter import Ui_plotter

# функция за мулти тред създава worker и thread и от там пуска определената функция в новия тред
# (ползвам го, за да не забива GUI-a при генериране на gdf и добавяне на area и радиус)
class Worker(QObject):
    finished = pyqtSignal() # сигнал, който се пуска при край на функцията
    geoDFupdate = pyqtSignal(object) # сигнал, който се пуска при готов gdf (съдържа самия gdf и се ползва за ъпдейт на този от основния клас)
    propUpdate = pyqtSignal(object) # сигнал, който се пуска при готово property (съдържа самото property и се ползва за ъпдейт на този от основния клас)

    # функция за създаване на threaded некомбиниран вороной
    def notCombined(self, gdf, long, lat, mapFile, sitesFile, progressLabel):
        gdf = createVoronoiNotCombined(mapPath=mapFile, longitude = long, latitude = lat, soaPath=sitesFile, progressLabel = progressLabel)
        self.finished.emit()
        self.geoDFupdate.emit(gdf)

    # функция за създаване на threaded комбиниран вороной
    def combined(self, gdf, prop, long, lat, mapFile, sitesFile, prop1Text, prop2Text, progressLabel):
        gdf, prop = createVoronoiCombined(mapPath = mapFile, soaPath = sitesFile, longitude = long, latitude = lat,
                                    propOne = prop1Text, propTwo = prop2Text, progressLabel = progressLabel)
        self.finished.emit()
        self.geoDFupdate.emit(gdf)
        self.propUpdate.emit(prop)

    # функция за добавяне на threaded area и радиус
    def addAreaAndRadiusFunc(self, gdf, progressLabel):
        gdf = addAreaAndRadius(gdf=gdf, progressLabel=progressLabel)
        self.finished.emit()
        self.geoDFupdate.emit(gdf)

class Ui_voronoi(object):

    def __init__(self):
        self.propLst = []
        self.gdf = pd.DataFrame()
        self.prop = []
        self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.combinedVoroFlag = None
        self.pointsOutSideBoundary = None
        self.long = None
        self.lat = None

    # отваря втория прозорец
    def open_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_plotter()
        self.ui.setupUi(voronoiPlotterWindow=self.window, voronoiCreatorGUI=voronoiCreatorGUI)
        self.ui.gdfForExport = self.gdf
        self.ui.propForExport = self.prop
        self.ui.combinedVoronoiFlag = self.combinedVoroFlag
        self.window.show()
        voronoiCreatorGUI.hide()

    # добавя area и радиус, като преди това изключва целия GUI
    def areaAndRadiusAdded(self):
        props = [self.countryMapLabel, self.countryMapOpener, self.mapFileName,
                 self.sitesFileName, self.soaLabel, self.soaOpener,
                 self.label, self.yesRadioButton, self.noRadioButton,
                 self.nextVoronoiButton]
        for prop in props:
            prop.setEnabled(True)
        self.progressLabel.setText('Progress: Done')

    # функция, която показва, че вороноя е готов
    def voronoiCreated(self):
        if self.gdf is None:
            props = [self.countryMapLabel, self.countryMapOpener, self.mapFileName,
                     self.sitesFileName, self.soaLabel, self.soaOpener,
                     self.label, self.yesRadioButton, self.noRadioButton]
            for prop in props:
                prop.setEnabled(True)
            self.progressLabel.setText('There were points outside the border!\n'
                                       'A file with them is saved inside the folder\n'
                                       'with the Sites on air file!')
        else:
            props = [self.countryMapLabel, self.countryMapOpener, self.mapFileName,
                     self.sitesFileName, self.soaLabel, self.soaOpener,
                     self.label, self.yesRadioButton, self.noRadioButton,
                     self.nextVoronoiButton, self.addAreaAndRadius, self.warningLabel]
            for prop in props:
                prop.setEnabled(True)
            self.progressLabel.setText('Progress: Done')

    # функция, която добавя area и радиус
    def addAreaAndRadiusFunction(self):
        self.progressLabel.setText('Progress: Loading...')
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.addAreaAndRadiusFunc, self.gdf, self.progressLabel))
        self.disableYesNo()
        props = [self.countryMapLabel, self.countryMapOpener, self.mapFileName, self.soaOpener,
                 self.soaLabel, self.sitesFileName, self.label, self.voronoiColLabel, self.voronoiFromColumnsLabel,
                 self.oneRadioButton, self.twoRadioButton, self.yesRadioButton, self.noRadioButton,
                 self.prop1, self.prop2, self.createVoronoiButton, self.addAreaAndRadius, self.nextVoronoiButton, self.warningLabel]
        for prop in props:
            prop.setDisabled(True)
        self.worker.geoDFupdate.connect(self.updateGDF)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(self.areaAndRadiusAdded)

    # функция, която създава вороноя
    def createVoronoiFunc(self):
        self.long = self.longitudeComboBox.currentText()
        self.lat = self.latitudeComboBox.currentText()
        self.progressLabel.setText('Progress: Loading...')
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        # ако е избрано да не се комбинира вороноя
        if self.noRadioButton.isChecked():
            self.thread.started.connect(partial(self.worker.notCombined,self.gdf, self.long, self.lat,
                                                self.mapFileName.text(), self.sitesFileName.text(), self.progressLabel))
            self.disableYesNo()
            props = [self.countryMapLabel, self.countryMapOpener, self.mapFileName, self.soaOpener,
                     self.soaLabel, self.sitesFileName, self.label, self.voronoiColLabel, self.voronoiFromColumnsLabel,
                     self.oneRadioButton, self.twoRadioButton, self.yesRadioButton, self.noRadioButton,
                     self.prop1, self.prop2, self.createVoronoiButton, self.nextVoronoiButton, self.longitudeComboBox,
                     self.latitudeComboBox, self.lat_long_Label]
            for prop in props:
                prop.setDisabled(True)
            self.worker.geoDFupdate.connect(self.updateGDF)
            self.combinedVoroFlag = False

        # ако е избрано да се комбинира вороноя
        elif self.yesRadioButton.isChecked():
            self.thread.started.connect(partial(self.worker.combined,self.gdf, self.prop, self.long, self.lat, self.mapFileName.text(),
                                                self.sitesFileName.text(), self.prop1.currentText(),
                                                self.prop2.currentText(), self.progressLabel))
            self.disableYesNo()
            props = [self.countryMapLabel, self.countryMapOpener, self.mapFileName, self.soaOpener,
                     self.soaLabel, self.sitesFileName, self.label, self.voronoiColLabel, self.voronoiFromColumnsLabel,
                     self.oneRadioButton, self.twoRadioButton, self.yesRadioButton, self.noRadioButton,
                     self.prop1, self.prop2, self.createVoronoiButton, self.nextVoronoiButton, self.longitudeComboBox,
                     self.latitudeComboBox, self.lat_long_Label]
            for prop in props:
                prop.setDisabled(True)
            self.worker.geoDFupdate.connect(self.updateGDF)
            self.worker.propUpdate.connect(self.updateProp)
            self.combinedVoroFlag = True
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(self.voronoiCreated)

    # слотове за сигнала от worker class-a, ползвам ги, за да ъпдейтвам property и gdf
    def updateProp(self, propUpdated):
        self.prop = propUpdated

    def updateGDF(self, geoDfUpdated):
        self.gdf = geoDfUpdated

    # функция за изключване на радио бутоните yes и no, когато са в една група
    def disableYesNo(self):
        self.separateVoronoiButtonGroup.setExclusive(False)
        if self.yesRadioButton.isChecked():
            self.yesRadioButton.setChecked(False)
        if self.noRadioButton.isChecked():
            self.noRadioButton.setChecked(False)
        self.separateVoronoiButtonGroup.setExclusive(True)

    # функция, която проверява двете property, ако са с еднакво име не позволява да се създаде вороной и обратно
    def enableCreateVoronoi_notCombined(self):
        if self.longitudeComboBox.currentText() == self.latitudeComboBox.currentText():
            self.createVoronoiButton.setDisabled(True)
            if self.yesRadioButton.isChecked():
                self.oneRadioButton.setDisabled(True)
                self.twoRadioButton.setDisabled(True)
                self.voronoiFromColumnsLabel.setDisabled(True)
        else:
            if self.yesRadioButton.isChecked():
                self.oneRadioButton.setEnabled(True)
                self.twoRadioButton.setEnabled(True)
                self.voronoiFromColumnsLabel.setEnabled(True)

    def enableCreateVoronoi(self):
        if self.prop1.currentText() == self.prop2.currentText():
            self.createVoronoiButton.setDisabled(True)
        else: self.createVoronoiButton.setEnabled(True)

    # функция, която изключва двата радио бутона за една и две колони от вороноя
    def disableOneTwo(self):
        self.numColButtonGroup.setExclusive(False)
        if self.oneRadioButton.isChecked():
            self.oneRadioButton.setChecked(False)
        if self.twoRadioButton.isChecked():
            self.twoRadioButton.setChecked(False)
        self.numColButtonGroup.setExclusive(True)

    # функция, която се използва за изключване на бутона за създаване на вороной при условие, че
    # не е избран файл или липсват ключови файлове от map/shp група
    # *Note: ако не се лъжа ги използвах, за да ресетвам функциите като се сменя избора на yes/no бутоните
    def noDisable(self):
        self.disableOneTwo()
        props = [self.voronoiColLabel, self.voronoiFromColumnsLabel, self.oneRadioButton, self.twoRadioButton,
                 self.prop1, self.prop2, self.addAreaAndRadius, self.warningLabel, self.voronoiColLabel]
        for prop in props:
            prop.setDisabled(True)
        self.prop1.clear()
        self.prop2.clear()
        if self.mapFileName.text().endswith("directory!"):
            props = [self.lat_long_Label, self.latitudeComboBox, self.longitudeComboBox,
                     self.voronoiFromColumnsLabel, self.oneRadioButton, self.twoRadioButton,
                     self.voronoiColLabel, self.prop1, self.prop2, self.createVoronoiButton,
                     self.createVoronoiButton]
            for prop in props:
                prop.setDisabled(True)
        else:
            self.latitudeComboBox.setEnabled(True)
            self.longitudeComboBox.setEnabled(True)
            self.lat_long_Label.setEnabled(True)
            if len(self.propLst) > 0:
                self.latitudeComboBox.clear()
                self.longitudeComboBox.clear()
                self.latitudeComboBox.addItems(self.latLst)
                self.longitudeComboBox.addItems(self.longLst)
                self.createVoronoiButton.setEnabled(True)
            elif len(self.propLst) == 0:
                self.latitudeComboBox.clear()
                self.longitudeComboBox.clear()
                self.latitudeComboBox.addItem("Error!")
                self.longitudeComboBox.addItem("Error!")
                self.createVoronoiButton.setDisabled(True)
            else:
                return
    # *Note: ако не се лъжа ги използвах, за да ресетвам функциите като се сменя избора на yes/no бутоните
    def yesEnable(self):
        if self.mapFileName.text().endswith("directory!"):
            props = [self.lat_long_Label, self.latitudeComboBox, self.longitudeComboBox,
                     self.voronoiFromColumnsLabel, self.oneRadioButton, self.twoRadioButton,
                     self.voronoiColLabel, self.prop1, self.prop2, self.createVoronoiButton]
            for prop in props:
                prop.setDisabled(True)
        else:
            self.disableOneTwo()
            props = [self.lat_long_Label, self.latitudeComboBox, self.longitudeComboBox]
            for prop in props:
                prop.setEnabled(True)
            self.prop1.setDisabled(True)
            self.prop2.setDisabled(True)
            self.voronoiColLabel.setDisabled(True)
            self.prop1.clear()
            self.prop2.clear()
            self.createVoronoiButton.setDisabled(True)
            self.addAreaAndRadius.setDisabled(True)
            self.warningLabel.setDisabled(True)
            if len(self.propLst) > 0:
                self.latitudeComboBox.clear()
                self.longitudeComboBox.clear()
                self.latitudeComboBox.addItems(self.latLst)
                self.longitudeComboBox.addItems(self.longLst)
                props = [self.voronoiFromColumnsLabel, self.oneRadioButton, self.twoRadioButton]
                for prop in props:
                    prop.setEnabled(True)
            elif len(self.propLst) == 0:
                self.latitudeComboBox.clear()
                self.longitudeComboBox.clear()
                self.latitudeComboBox.addItem("Error!")
                self.longitudeComboBox.addItem("Error!")
                self.createVoronoiButton.setDisabled(True)
                props = [self.voronoiFromColumnsLabel, self.oneRadioButton, self.twoRadioButton]
                for prop in props:
                    prop.setDisabled(True)
            else:
                return

    # функция отваряща файлов браузър за sites on air файлове
    def browseSiteFiles(self):
        self.disableYesNo()
        self.voronoiFromColumnsLabel.setDisabled(True)
        self.disableOneTwo()
        self.voronoiColLabel.setDisabled(True)
        self.prop1.setDisabled(True)
        self.prop2.setDisabled(True)
        self.prop1.clear()
        self.prop2.clear()
        self.longitudeComboBox.clear()
        self.latitudeComboBox.clear()
        fname = QFileDialog.getOpenFileName(None, "Open file", self.desktop,
                                            "Excel Files(*.xlsx);;Excel /95 (*.xls);;CSV Files (*.csv)")
        if fname[0].lower().endswith(('.xls', '.xlsx', '.csv')):
            self.sitesFileName.setText(fname[0])
            df_Sites_On_Air = pd.read_excel(self.sitesFileName.text(), nrows = 0)
            self.propLst = df_Sites_On_Air.columns.to_list()
            if len(self.propLst) != 0:
                self.longLst = []
                self.latLst = []
                for item in self.propLst:
                    if 'lon' in item.lower():
                        self.longLst.append(item)
                    if 'lat' in item.lower():
                        self.latLst.append(item)
        elif fname[0] == '':
            return
        else:
            self.sitesFileName.setText("File is with wrong format!")

    # попълват дроп меню 1 и 2 според първия ред  на отворения sits on air
    def fillProp1(self):
        if len(self.propLst) > 0:
            self.prop1.clear()
            self.prop2.clear()
            self.prop1.addItems(self.propLst)
            self.createVoronoiButton.setEnabled(True)
        elif len(self.propLst) == 0:
            self.prop1.clear()
            self.prop2.clear()
            self.prop1.addItem("Error!")
            self.createVoronoiButton.setDisabled(True)
        else:
            return

    def fillProp2(self):
        if len(self.propLst) > 0:
            self.prop1.clear()
            self.prop2.clear()
            self.prop1.addItems(self.propLst)
            self.prop2.addItems(self.propLst)
        elif len(self.propLst) == 0:
            self.prop1.clear()
            self.prop2.clear()
            self.prop1.addItem("Error!")
            self.prop2.addItem("Error!")
            self.createVoronoiButton.setDisabled(True)
        else:
            return

    # ползват се за забрана и отбрана на дроп менютата
    def twoRadioButtonEnable(self):
        self.voronoiColLabel.setEnabled(True)
        self.prop1.setEnabled(True)
        self.prop2.setEnabled(True)

    def oneRadioButtonEnable(self):
        self.voronoiColLabel.setEnabled(True)
        self.prop1.setEnabled(True)
        self.prop2.setEnabled(False)

    # функция отваряща файлов браузър за map/shp файлове
    def browseMapFiles(self):
        self.disableYesNo()
        self.voronoiFromColumnsLabel.setDisabled(True)
        self.disableOneTwo()
        self.voronoiColLabel.setDisabled(True)
        self.prop1.setDisabled(True)
        self.prop2.setDisabled(True)
        self.prop1.clear()
        self.prop2.clear()
        self.longitudeComboBox.clear()
        self.latitudeComboBox.clear()
        fname = QFileDialog.getOpenFileName(None, "Open file", self.desktop,
                                            "Tab Files (*.tab);;Shape Files (*.shp)")
        if fname[0].lower().endswith(('.tab', '.shp')):
            if fname[0].lower().endswith('.tab'):
                path = fname[0].split('/')
                tabFileName = path.pop().lower()
                tabFileName = tabFileName.replace('.tab','')
                path = '/'.join(path)
                fileLst = []
                for file in os.listdir(path):
                    fileLst.append(file)
                requiredFiles = [tabFileName+'.dat', tabFileName+'.id', tabFileName+'.map']
                for file in fileLst:
                    file = file.lower()
                    if file in requiredFiles:
                        requiredFiles.remove(file)
                    if len(requiredFiles) == 0:
                        break
                if len(requiredFiles) > 0:
                    requiredFiles = ', '.join(requiredFiles)
                    self.mapFileName.setText(f'Missing {requiredFiles} from directory!')
                else: self.mapFileName.setText(fname[0])
            else:
                path = fname[0].split('/')
                shpFileName = path.pop().lower()
                shpFileName = shpFileName.replace('.shp','')
                path = '/'.join(path)
                fileLst = []
                for file in os.listdir(path):
                    fileLst.append(file)
                requiredFiles = [shpFileName+'.cpg', shpFileName+'.dbf', shpFileName+'.prj', shpFileName+'.shx']
                for file in fileLst:
                    file = file.lower()
                    if file in requiredFiles:
                        requiredFiles.remove(file)
                    if len(requiredFiles) == 0:
                        break
                if len(requiredFiles) > 0:
                    requiredFiles = ', '.join(requiredFiles)
                    self.mapFileName.setText(f'Missing {requiredFiles} from directory!')
                else: self.mapFileName.setText(fname[0])

        elif fname[0] == '':
            return

    def setupUi(self, voronoiCreatorGUI):

        voronoiCreatorGUI.setObjectName("voronoiCreatorGUI")
        voronoiCreatorGUI.resize(700,500)
        voronoiCreatorGUI.setMinimumSize(QtCore.QSize(0, 0))
        voronoiCreatorGUI.setMaximumSize(QtCore.QSize(16777215, 16777215))
        voronoiCreatorGUI.setDocumentMode(False)

        self.centralwidget = QtWidgets.QWidget(voronoiCreatorGUI)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.voronoiGridLayout = QtWidgets.QGridLayout()
        self.voronoiGridLayout.setContentsMargins(5, 5, 5, 5)
        self.voronoiGridLayout.setSpacing(10)
        self.voronoiGridLayout.setObjectName("voronoiGridLayout")

        # ==================SITES ON AIR LABEL, OPENER AND LINE EDIT==================
        # SITES ON AIR LABEL
        self.soaLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.soaLabel.setFont(font)
        self.soaLabel.setObjectName("soaLabel")
        self.voronoiGridLayout.addWidget(self.soaLabel, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.voronoiGridLayout.addWidget(self.label, 6, 1, 1, 1)

        # SITES ON AIR OPENER BUTTON/FILE BROWSER
        self.soaOpener = QtWidgets.QPushButton(self.centralwidget)
        self.soaOpener.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.soaOpener.setFont(font)
        self.soaOpener.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.soaOpener.setObjectName("soaOpener")
        self.soaOpener.clicked.connect(self.browseSiteFiles)
        self.voronoiGridLayout.addWidget(self.soaOpener, 4, 2, 1, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        # VORONOI FROM SELECTED COLUMNS LABEL
        self.voronoiFromColumnsLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.voronoiFromColumnsLabel.setFont(font)
        self.voronoiFromColumnsLabel.setObjectName("voronoiFromColumnsLabel")
        self.voronoiGridLayout.addWidget(self.voronoiFromColumnsLabel, 9, 1, 1, 2,
                                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.voronoiFromColumnsLabel.setDisabled(True)

        # SITES ON AIR TEXT EDIT/PATH AND FILE NAME
        self.sitesFileName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.sitesFileName.setFont(font)
        self.sitesFileName.setObjectName("sitesFileName")
        self.voronoiGridLayout.addWidget(self.sitesFileName, 5, 1, 1, 2)
        self.gridLayout.addLayout(self.voronoiGridLayout, 0, 0, 1, 1)

        # ==================COUNTRY MAP LABEL,TITLE, OPENER AND LINE EDIT==================
        # COUNTRY MAP LABEL
        self.countryMapLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.countryMapLabel.setFont(font)
        self.countryMapLabel.setObjectName("countryMapLabel")
        self.voronoiGridLayout.addWidget(self.countryMapLabel, 2, 1, 1, 1)

        # TITLE
        self.title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setAutoFillBackground(False)
        self.title.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title.setLineWidth(1)
        self.title.setMidLineWidth(0)
        self.title.setObjectName("title")
        self.voronoiGridLayout.addWidget(self.title, 0, 1, 1, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # COUNTRY MAP OPEN BUTTON
        self.countryMapOpener = QtWidgets.QPushButton(self.centralwidget)
        self.countryMapOpener.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.countryMapOpener.setFont(font)
        self.countryMapOpener.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.countryMapOpener.setObjectName("countryMapOpener")
        self.countryMapOpener.clicked.connect(self.browseMapFiles)
        self.voronoiGridLayout.addWidget(self.countryMapOpener, 2, 2, 1, 1,
                                         QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        # MAP FILE NAME LINE EDIT
        self.mapFileName = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.mapFileName.setFont(font)
        self.mapFileName.setObjectName("mapFileName")
        self.voronoiGridLayout.addWidget(self.mapFileName, 3, 1, 1, 2)

        # VORONOI NUMBER OF COLUMNS LABEL
        self.voronoiColLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.voronoiColLabel.setFont(font)
        self.voronoiColLabel.setObjectName("voronoiColLabel")
        self.voronoiColLabel.setDisabled(True)
        self.voronoiGridLayout.addWidget(self.voronoiColLabel, 11, 1, 1, 2,
                                         QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # ==================PROPERTIES==================
        self.prop_HLayout = QtWidgets.QHBoxLayout()
        self.prop_HLayout.setObjectName("prop_HLayout")

        # PROPERTY 1
        self.prop1 = QtWidgets.QComboBox(self.centralwidget)
        self.prop1.setObjectName("prop1")
        self.prop_HLayout.addWidget(self.prop1)
        self.prop1.setDisabled(True)
        self.prop1.currentTextChanged.connect(self.enableCreateVoronoi)
        # PROPERTY 2
        self.prop2 = QtWidgets.QComboBox(self.centralwidget)
        self.prop2.setObjectName("prop2")
        self.prop_HLayout.addWidget(self.prop2)
        self.prop2.currentTextChanged.connect(self.enableCreateVoronoi)
        self.voronoiGridLayout.addLayout(self.prop_HLayout, 12, 1, 1, 2)
        self.prop2.setDisabled(True)

        # ==================LAT, LONG LABEL AND COMBO BOXES==================
        self.location_HLayout = QtWidgets.QHBoxLayout()
        self.location_HLayout.setObjectName(u"location_HLayout")

        # LAT, LONG LABEL
        self.lat_long_Label = QtWidgets.QLabel(self.centralwidget)
        self.lat_long_Label.setObjectName(u"lat_long_Label")
        self.lat_long_Label.setDisabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lat_long_Label.setFont(font)

        self.voronoiGridLayout.addWidget(self.lat_long_Label, 7, 1, 1, 2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        # LAT COMBO BOX
        self.latitudeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.latitudeComboBox.setObjectName(u"latitudeComboBox")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.latitudeComboBox.setFont(font)
        self.latitudeComboBox.setDisabled(True)
        self.location_HLayout.addWidget(self.latitudeComboBox)
        self.latitudeComboBox.currentTextChanged.connect(self.enableCreateVoronoi_notCombined)
        # LONG COMBO BOX
        self.longitudeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.longitudeComboBox.setObjectName(u"longitudeComboBox")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.longitudeComboBox.setFont(font)
        self.longitudeComboBox.setDisabled(True)
        self.longitudeComboBox.currentTextChanged.connect(self.enableCreateVoronoi_notCombined)
        self.location_HLayout.addWidget(self.longitudeComboBox)
        self.voronoiGridLayout.addLayout(self.location_HLayout, 8, 1, 1, 2)

        # ==================ONE AND TWO COLUMNS BUTTONS==================
        # CREATING BUTTON GROUP
        self.one_two_RadioButtons_HLayout = QtWidgets.QHBoxLayout()
        self.one_two_RadioButtons_HLayout.setObjectName("one_two_RadioButtons_HLayout")

        # ONE RADIO BUTTON
        self.oneRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.oneRadioButton.setFont(font)
        self.oneRadioButton.setObjectName("oneRadioButton")
        self.numColButtonGroup = QtWidgets.QButtonGroup(voronoiCreatorGUI)
        self.numColButtonGroup.setObjectName("numColButtonGroup")
        self.numColButtonGroup.addButton(self.oneRadioButton)
        self.one_two_RadioButtons_HLayout.addWidget(self.oneRadioButton, 0,
                                                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.oneRadioButton.setDisabled(True)
        self.oneRadioButton.toggled.connect(self.oneRadioButtonEnable)
        self.oneRadioButton.toggled.connect(self.fillProp1)

        # TWO RADIO BUTTON
        self.twoRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.twoRadioButton.setFont(font)
        self.twoRadioButton.setObjectName("twoRadioButton")
        self.numColButtonGroup.addButton(self.twoRadioButton)
        self.one_two_RadioButtons_HLayout.addWidget(self.twoRadioButton, 0,
                                                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.voronoiGridLayout.addLayout(self.one_two_RadioButtons_HLayout, 10, 1, 1, 2)
        self.twoRadioButton.setDisabled(True)
        self.twoRadioButton.toggled.connect(self.twoRadioButtonEnable)
        self.twoRadioButton.toggled.connect(self.fillProp2)

        # ==================YES AND NO COLUMNS BUTTONS==================
        # YES RADIO BUTTON
        self.yes_no_Combined_HLayout = QtWidgets.QHBoxLayout()
        self.yes_no_Combined_HLayout.setObjectName("yes_no_Combined_HLayout")
        self.yesRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.yesRadioButton.setFont(font)
        self.yesRadioButton.setObjectName("yesRadioButton")
        self.yesRadioButton.clicked.connect(self.yesEnable)
        self.separateVoronoiButtonGroup = QtWidgets.QButtonGroup(voronoiCreatorGUI)
        self.separateVoronoiButtonGroup.setObjectName("separateVoronoiButtonGroup")
        self.separateVoronoiButtonGroup.addButton(self.yesRadioButton)
        self.yes_no_Combined_HLayout.addWidget(self.yesRadioButton)

        # NO RADIO BUTTON
        self.noRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.noRadioButton.setFont(font)
        self.noRadioButton.setObjectName("noRadioButton")
        self.separateVoronoiButtonGroup.addButton(self.noRadioButton)
        self.yes_no_Combined_HLayout.addWidget(self.noRadioButton)
        self.voronoiGridLayout.addLayout(self.yes_no_Combined_HLayout, 6, 2, 1, 1)
        voronoiCreatorGUI.setCentralWidget(self.centralwidget)
        self.noRadioButton.toggled.connect(self.noDisable)

        # ==================NEXT BUTTON/CREATING VORONOI BUTTON==================
        self.actionButtons_HLayout = QtWidgets.QHBoxLayout()
        self.actionButtons_HLayout.setObjectName(u"actionButtons_HLayout")
        self.createVoronoiButton = QtWidgets.QPushButton(self.centralwidget)
        self.createVoronoiButton.setObjectName(u"createVoronoiButton")
        self.createVoronoiButton.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.createVoronoiButton.setFont(font)
        self.createVoronoiButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.createVoronoiButton.setDisabled(True)
        self.createVoronoiButton.clicked.connect(self.createVoronoiFunc)
        self.actionButtons_HLayout.addWidget(self.createVoronoiButton, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.progressLabel = QtWidgets.QLabel(self.centralwidget)
        self.progressLabel.setObjectName(u"progressLabel")
        self.progressLabel.setFont(font)
        self.progressLabel.setText('Progress: None')

        self.voronoiGridLayout.addWidget(self.progressLabel, 14, 1, 1, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.voronoiGridLayout, 1, 0, 1, 1)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.addAreaAndRadius = QtWidgets.QPushButton(self.centralwidget)
        self.addAreaAndRadius.setObjectName(u"addAreaAndRadius")
        self.addAreaAndRadius.setFont(font)
        self.addAreaAndRadius.setDisabled(True)
        self.actionButtons_HLayout.addWidget(self.addAreaAndRadius, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.addAreaAndRadius.clicked.connect(self.addAreaAndRadiusFunction)
        self.addAreaAndRadius.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.warningLabel = QtWidgets.QLabel(self.centralwidget)
        self.warningLabel.setObjectName(u"warningLabel")
        self.warningLabel.setFont(font)
        self.warningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.actionButtons_HLayout.addWidget(self.warningLabel, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.warningLabel.setDisabled(True)

        self.nextVoronoiButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextVoronoiButton.setObjectName(u"nextVoronoiButton")
        self.nextVoronoiButton.setMinimumSize(QtCore.QSize(75, 25))
        self.nextVoronoiButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.nextVoronoiButton.setFont(font)
        self.nextVoronoiButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.nextVoronoiButton.setDisabled(True)
        self.nextVoronoiButton.clicked.connect(self.open_window)

        self.actionButtons_HLayout.addWidget(self.nextVoronoiButton, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.voronoiGridLayout.addLayout(self.actionButtons_HLayout, 13, 1, 1, 2)
        self.retranslateUi(voronoiCreatorGUI)
        QtCore.QMetaObject.connectSlotsByName(voronoiCreatorGUI)

    def retranslateUi(self, voronoiCreatorGUI):
        _translate = QtCore.QCoreApplication.translate
        voronoiCreatorGUI.setWindowTitle(_translate("voronoiCreatorGUI", "Voronoi Creator"))
        self.nextVoronoiButton.setText(_translate("voronoiCreatorGUI", "Next >>"))
        self.addAreaAndRadius.setText(_translate("voronoiCreatorGUI", u"Add Area and Radius"))
        self.warningLabel.setText(_translate("voronoiCreatorGUI", u"Warning: Adding area and \n"
                                                                " radius takes a while."))
        self.createVoronoiButton.setText(_translate("voronoiCreatorGUI", "Create Voronoi"))
        self.soaLabel.setText(_translate("voronoiCreatorGUI", "Open Sites on air file: "))
        self.label.setText(_translate("voronoiCreatorGUI", "Generate separte voronoi diagram or combined?"))
        self.mapFileName.setText(_translate("voronoiCreatorGUI", self.desktop))
        self.voronoiColLabel.setText(
            _translate("voronoiCreatorGUI", "Select the column/s from which the voronoi will be created"))
        self.countryMapLabel.setText(_translate("voronoiCreatorGUI", "Open country map file: "))
        self.title.setText(_translate("voronoiCreatorGUI", "Voronoi Creator"))
        self.oneRadioButton.setText(_translate("voronoiCreatorGUI", "1"))
        self.twoRadioButton.setText(_translate("voronoiCreatorGUI", "2"))
        self.soaOpener.setText(_translate("voronoiCreatorGUI", "Open"))
        self.voronoiFromColumnsLabel.setText(
            _translate("voronoiCreatorGUI", "Select the number of column from which the voronoi will be created"))
        self.yesRadioButton.setText(_translate("voronoiCreatorGUI", "Yes"))
        self.noRadioButton.setText(_translate("voronoiCreatorGUI", "No"))
        self.countryMapOpener.setText(_translate("voronoiCreatorGUI", "Open"))
        self.sitesFileName.setText(_translate("voronoiCreatorGUI", self.desktop))
        self.lat_long_Label.setText(_translate("voronoiCreatorGUI", 'Select latitude column on the left and longitude column on the right.'))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QtGui.QIcon('voronoi-diagram.png'))
    voronoiCreatorGUI = QtWidgets.QMainWindow()
    ui = Ui_voronoi()
    ui.setupUi(voronoiCreatorGUI)
    voronoiCreatorGUI.show()
    sys.exit(app.exec_())
