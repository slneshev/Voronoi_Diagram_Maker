from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from voronoiFunc import *
from plotOptions import Ui_plotOptions
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from functools import partial

# функция за мулти тред създава worker и thread и от там пуска определената функция в новия тред
# (ползвам го, за да не забива GUI-a при генериране на fig, excel, mapinfo)
class Worker(QObject):
    finished = pyqtSignal()  # сигнал, който се пуска при край на функцията
    flag = pyqtSignal(bool)

    def excelOrTxtSave(self, gdf, path, prop):
        flag = excelExport(gdf,path,prop)
        self.finished.emit()
        self.flag.emit(flag)

    def figureSave(self, figPath, extension, propForExport, gdfForExport, legendNumCol, polyLabelFont, polyTextStyle, 
                   polyBorderLineW, polyBorderColor, polyTextColor, polyHaloLineW, polyHaloColor, legendLoc,
                   legendFontSize, legendTitleFontSize, legendMarkerSize,legendFrame, legendFancyBox,
                   legendBackgroundColor, legendTextColor, legendMarkerFirst, legendOptions, polyCmapB10, polyCmapB20,
                   polyCmapA20, figAxis, dpi, combinedVoronoiFlag):
        plotting(figSavePath=figPath, ext = extension, proper=propForExport, gdf=gdfForExport,
                 numCol=legendNumCol, polyLabelFont=polyLabelFont, polyFontWght=polyTextStyle, polyBorderWidth=polyBorderLineW,
                 polyEdgeColor=polyBorderColor, polyTextColor=polyTextColor, polyHaloLineWidth=polyHaloLineW, polyHaloColor=polyHaloColor,
                 legendLoc=legendLoc, legendFontSize=legendFontSize, legendTitleFontSize=legendTitleFontSize, legendMarkerScale=legendMarkerSize,
                 legendFrameOn=legendFrame, legendFancyBox=legendFancyBox, legendFaceColor=legendBackgroundColor, legendLabelColor=legendTextColor,
                 legendMarkerFirst=legendMarkerFirst, legendOption=legendOptions, polyCmapBelow10=polyCmapB10, polyCmapBelow20=polyCmapB20,
                 polyCmapAbove20=polyCmapA20, figAxis=figAxis, dpi_from_input=dpi, flag = combinedVoronoiFlag)
        self.finished.emit()

    def mapInfoSave(self, gdfForExport, mapInfoPath, propForExport):
        mapInfoExport(gdf=gdfForExport, mapInfoPath=mapInfoPath, prop=propForExport)
        self.finished.emit()


class Ui_plotter(object):
    def __init__(self):
        self.flag = None
        self.excelSaveLocation = ''
        self.excelSavedTimes = 1
        self.txtSavedTimes = 1
        self.mapInfoSavedTimes = 1
        self.figSavedTimes = 1
        self.figSaveLocation = ''
        self.mapInfoSaveLocation = ''
        self.combinedVoronoiFlag = None
        self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.gdfForExport = pd.DataFrame()
        self.propForExport = []
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiSettings = Ui_plotOptions()
        self.uiSettings.setupUi(self.settingsWindow)
        self.legendOptions = self.uiSettings.legendTrue.isChecked()
        self.legendNumCol = self.uiSettings.ncolLineEdit.text()
        self.legendLoc = self.uiSettings.locComboBox.currentText()
        self.legendMarkerSize = self.uiSettings.markerScaleLineEdit.text()
        self.legendFontSize = self.uiSettings.title_fontsizeLineEdit.text()
        self.uiSettings.titleLineEdit.setText(str(self.propForExport))
        self.legendTitle = self.uiSettings.titleLineEdit.text()
        self.legendTitleFontSize = self.uiSettings.titleFontSizeLineEdit.text()
        self.legendBackgroundColor = self.uiSettings.facecolorLineEdit.text()
        self.legendTextColor = self.uiSettings.labelcolorLineEdit.text()
        self.legendMarkerFirst = self.uiSettings.markerfirstTrue.isChecked()
        self.legendFrame = self.uiSettings.frameOnTrue.isChecked()
        self.legendFancyBox = self.uiSettings.fancyboxTrue.isChecked()
        self.polyCmapB10 = self.uiSettings.cmap10LineEdit.text()
        self.polyCmapB20 = self.uiSettings.cmap10_20LineEdit.text()
        self.polyCmapA20 = self.uiSettings.cmap20LineEdit.text()
        self.polyBorderColor = self.uiSettings.edgeColourLineEdit.text()
        self.polyBorderLineW = self.uiSettings.lineWdthLineEdit.text()
        self.polyTextStyle = self.uiSettings.fontWeightComboBox.currentText()
        self.polyTextColor = self.uiSettings.textColorLineEdit.text()
        self.polyLabelFont = self.uiSettings.polyLabelFontLineEdit.text()
        self.polyHaloLineW = self.uiSettings.haloLineWidthLineEdit.text()
        self.polyHaloColor = self.uiSettings.haloColorLineEdit.text()
        self.figAxis = self.uiSettings.yesAxisRadioButton.isChecked()
        self.dpi = self.uiSettings.dpiLineEdit.text()

    def open_settings(self):
        # тези два листа са при случай, че е избрано да не се комбинира вороноя
        # първо ги заключва, а тези с възможност за избор или въвеждане ги чисти
        # оставил съм общите опции за фигурата и полигоните отключена
        props = [self.uiSettings.legendOptionsLabel, self.uiSettings.ncolLabel, self.uiSettings.ncolLineEdit, self.uiSettings.polyLabelFontLineEdit,
                 self.uiSettings.polyLabelFont, self.uiSettings.labelcolorLabel, self.uiSettings.labelcolorLineEdit, self.uiSettings.haloLineWidthLineEdit,
                 self.uiSettings.legendLabel, self.uiSettings.locLabel, self.uiSettings.locComboBox, self.uiSettings.markerScaleLabel,
                 self.uiSettings.markerScaleLineEdit, self.uiSettings.title_fontsizeLineEdit, self.uiSettings.titleFontSizeLineEdit, self.uiSettings.title_fontsizeLabel, self.uiSettings.titleFontSizeLabel,
                 self.uiSettings.titleLabel, self.uiSettings.titleLineEdit, self.uiSettings.facecolorLabel, self.uiSettings.facecolorLineEdit, self.uiSettings.textColorLineEdit, self.uiSettings.textColorLabel,
                 self.uiSettings.markerfirstLabel, self.uiSettings.frameOnLabel, self.uiSettings.fancyboxLabel, self.uiSettings.fancyboxTrue, self.uiSettings.fancyboxFalse,
                 self.uiSettings.fontWeightLabel, self.uiSettings.fontWeightComboBox, self.uiSettings.markerfirstTrue, self.uiSettings.markerfirstFalse,
                 self.uiSettings.textColorLabel, self.uiSettings.haloColorLabel, self.uiSettings.haloColorLineEdit, self.uiSettings.haloLineWidthLabel, self.uiSettings.haloLineWidthLabel,
                 self.uiSettings.legendTrue, self.uiSettings.legendFalse, self.uiSettings.frameOnFalse, self.uiSettings.frameOnTrue]

        propsForClear = [self.uiSettings.ncolLineEdit, self.uiSettings.polyLabelFontLineEdit,
                    self.uiSettings.labelcolorLineEdit, self.uiSettings.haloLineWidthLineEdit,
                    self.uiSettings.locComboBox,self.uiSettings.markerScaleLineEdit, self.uiSettings.title_fontsizeLineEdit,
                    self.uiSettings.titleFontSizeLineEdit, self.uiSettings.titleLineEdit, self.uiSettings.facecolorLineEdit,
                    self.uiSettings.textColorLineEdit, self.uiSettings.fontWeightComboBox,self.uiSettings.haloColorLineEdit]

        if self.combinedVoronoiFlag is False:

            self.uiSettings.legendButtonGroup.setExclusive(False)
            if self.uiSettings.legendTrue.isChecked():
                self.uiSettings.legendTrue.setChecked(False)
            if self.uiSettings.legendFalse.isChecked():
                self.uiSettings.legendFalse.setChecked(False)
            self.uiSettings.legendButtonGroup.setExclusive(True)

            self.uiSettings.markerFirstButtonGroup.setExclusive(False)
            if self.uiSettings.markerfirstTrue.isChecked():
                self.uiSettings.markerfirstTrue.setChecked(False)
            if self.uiSettings.markerfirstFalse.isChecked():
                self.uiSettings.markerfirstFalse.setChecked(False)
            self.uiSettings.markerFirstButtonGroup.setExclusive(True)

            self.uiSettings.frameButtonGroup.setExclusive(False)
            if self.uiSettings.frameOnTrue.isChecked():
                self.uiSettings.frameOnTrue.setChecked(False)
            if self.uiSettings.frameOnFalse.isChecked():
                self.uiSettings.frameOnFalse.setChecked(False)
            self.uiSettings.frameButtonGroup.setExclusive(True)

            self.uiSettings.fancyBoxButtonGroup.setExclusive(False)
            if self.uiSettings.fancyboxTrue.isChecked():
                self.uiSettings.fancyboxTrue.setChecked(False)
            if self.uiSettings.fancyboxFalse.isChecked():
                self.uiSettings.fancyboxFalse.setChecked(False)
            self.uiSettings.fancyBoxButtonGroup.setExclusive(True)

            for prop in propsForClear:
                prop.clear()

            for prop in props:
                prop.setDisabled(True)

        self.settingsWindow.show()
        self.legendOptionsOld = self.uiSettings.legendTrue.isChecked()
        self.legendNumColOld = self.uiSettings.ncolLineEdit.text()
        self.legendLocOld = self.uiSettings.locComboBox.currentText()
        self.legendMarkerSizeOld = self.uiSettings.markerScaleLineEdit.text()
        self.legendFontSizeOld = self.uiSettings.title_fontsizeLineEdit.text()
        self.polyLabelFontOld = self.uiSettings.polyLabelFontLineEdit.text()
        self.legendTitleOld = self.uiSettings.titleLineEdit.text()
        self.legendTitleFontSizeOld = self.uiSettings.titleFontSizeLineEdit.text()
        self.legendBackgroundColorOld = self.uiSettings.facecolorLineEdit.text()
        self.legendTextColorOld = self.uiSettings.labelcolorLineEdit.text()
        self.legendMarkerFirstOld = self.uiSettings.markerfirstTrue.isChecked()
        self.legendFrameOld = self.uiSettings.frameOnTrue.isChecked()
        self.legendFancyBoxOld = self.uiSettings.fancyboxTrue.isChecked()
        self.polyCmapB10Old = self.uiSettings.cmap10LineEdit.text()
        self.polyCmapB20Old = self.uiSettings.cmap10_20LineEdit.text()
        self.polyCmapA20Old = self.uiSettings.cmap20LineEdit.text()
        self.polyBorderColorOld = self.uiSettings.edgeColourLineEdit.text()
        self.polyBorderLineWOld = self.uiSettings.lineWdthLineEdit.text()
        self.polyTextStyleOld = self.uiSettings.fontWeightComboBox.currentText()
        self.polyTextColorOld = self.uiSettings.textColorLineEdit.text()
        self.polyHaloLineWOld = self.uiSettings.haloLineWidthLineEdit.text()
        self.polyHaloColorOld = self.uiSettings.haloColorLineEdit.text()
        self.figAxisOld = self.uiSettings.yesAxisRadioButton.isChecked()
        self.dpiOld = self.uiSettings.dpiLineEdit.text()

    def backButtonOperation(self, voronoiGui, plotterW):
        voronoiGui.show()
        plotterW.hide()

    def flagUpdate(self, flag):
        self.flag = flag
    
    def excelOrTxtSaved(self):
        if self.figureDisabled is True:
            props = [self.figPathLabel, self.figPath, self.yesSaveFigButton,
                     self.noSaveFigButton, self.saveFigLabel, self.browseFigPushButton,
                     self.figExtensionLabel, self.radioButtonJPG, self.radioButtonPng,
                     self.settingsPushButton]
            for prop in props:
                prop.setEnabled(True)
            if self.radioFlag is True:
                self.saveFigPushButton.setEnabled(True)
        else:
            props = [self.yesSaveFigButton,self.noSaveFigButton, self.saveFigLabel]
            for prop in props:
                prop.setEnabled(True)

        if self.mapDisabled is True:
            props = [self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton,
                     self.mapExportLabel, self.mapInfoPath, self.browseMapPushButton,
                     self.exportPushButton]
            for prop in props:
                prop.setEnabled(True)
        else:
            props = [self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton]
            for prop in props:
                prop.setEnabled(True)

        props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton,
                 self.excelPath, self.excelPathLabel, self.browseExcelPushButton,
                 self.backPushButton, self.saveExcelPushButton]
        for prop in props:
            prop.setEnabled(True)
        if self.flag is False:
            if self.mapInfoSavedTimes == 1:
                self.savingLabel.setText(f"Excel file saved {self.excelSavedTimes} time!")
                self.excelSavedTimes = self.excelSavedTimes + 1
            else:
                self.savingLabel.setText(f"Excel file saved {self.excelSavedTimes} times!")
                self.excelSavedTimes = self.excelSavedTimes + 1
        else:
            if self.txtSavedTimes == 1:
                self.savingLabel.setText(f"Polygons were too big and the output was saved into .txt file format. \n"
                                         f"Text file is saved {self.txtSavedTimes} time!")
                self.txtSavedTimes = self.txtSavedTimes + 1
            else:
                self.savingLabel.setText(f"Polygons were too big and the output was saved into .txt file format. \n"
                                         f"Text file is saved {self.txtSavedTimes} times!")
                self.txtSavedTimes = self.txtSavedTimes + 1

    def saveExcelFile(self):
        self.figureDisabled = False
        self.mapDisabled = False
        self.radioFlag = False
        self.savingLabel.setText("Saving Excel or Txt file...")
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.excelOrTxtSave, self.gdfForExport, self.excelPath.text(), self.propForExport))
        if self.saveFigLabel.isEnabled() and self.yesSaveFigButton.isChecked():
            if self.radioButtonPng.isChecked() or self.radioButtonJPG.isChecked():
                self.radioFlag = True
            self.figureDisabled = True
        if self.mapExportLabel.isEnabled() and self.yesSaveMIButton.isChecked():
            self.mapDisabled = True
        props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton,
                 self.excelPathLabel, self.browseExcelPushButton, self.excelPath,
                 self.saveFigLabel, self.yesSaveFigButton, self.noSaveFigButton,
                 self.figPath, self.figPathLabel, self.browseFigPushButton,
                 self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton,
                 self.mapExportLabel, self.mapInfoPath, self.browseMapPushButton,
                 self.backPushButton, self.saveExcelPushButton, self.saveFigPushButton,
                 self.settingsPushButton, self.exportPushButton,self.radioButtonJPG,
                 self.radioButtonPng, self.figExtensionLabel]
        for prop in props:
            prop.setDisabled(True)
        self.worker.flag.connect(self.flagUpdate)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(self.excelOrTxtSaved)

    def saveFig(self):
        if self.uiSettings.saveFlag is True:
            self.legendOptions = self.uiSettings.legendTrue.isChecked()
            self.legendNumCol = self.uiSettings.ncolLineEdit.text()
            self.legendLoc = self.uiSettings.locComboBox.currentText()
            self.legendMarkerSize = self.uiSettings.markerScaleLineEdit.text()
            self.legendFontSize = self.uiSettings.title_fontsizeLineEdit.text()
            self.legendTitle = self.uiSettings.titleLineEdit.text()
            self.legendTitleFontSize = self.uiSettings.titleFontSizeLineEdit.text()
            self.legendBackgroundColor = self.uiSettings.facecolorLineEdit.text()
            self.legendTextColor = self.uiSettings.labelcolorLineEdit.text()
            self.legendMarkerFirst = self.uiSettings.markerfirstTrue.isChecked()
            self.legendFrame = self.uiSettings.frameOnTrue.isChecked()
            self.legendFancyBox = self.uiSettings.fancyboxTrue.isChecked()
            self.polyCmapB10 = self.uiSettings.cmap10LineEdit.text()
            self.polyCmapB20 = self.uiSettings.cmap10_20LineEdit.text()
            self.polyCmapA20 = self.uiSettings.cmap20LineEdit.text()
            self.polyBorderColor = self.uiSettings.edgeColourLineEdit.text()
            self.polyBorderLineW = self.uiSettings.lineWdthLineEdit.text()
            self.polyTextStyle = self.uiSettings.fontWeightComboBox.currentText()
            self.polyTextColor = self.uiSettings.textColorLineEdit.text()
            self.polyLabelFont = self.uiSettings.polyLabelFontLineEdit.text()
            self.polyHaloLineW = self.uiSettings.haloLineWidthLineEdit.text()
            self.polyHaloColor = self.uiSettings.haloColorLineEdit.text()
            self.figAxis = self.uiSettings.yesAxisRadioButton.isChecked()
            self.dpi = self.uiSettings.dpiLineEdit.text()

        else:
            self.legendOptions = self.legendOptionsOld
            self.legendNumCol = self.legendNumColOld
            self.legendLoc = self.legendLocOld
            self.legendMarkerSize = self.legendMarkerSizeOld
            self.legendFontSize = self.legendFontSizeOld
            self.legendTitle = self.legendTitleOld
            self.legendTitleFontSize = self.legendTitleFontSizeOld
            self.legendBackgroundColor = self.legendBackgroundColorOld
            self.legendTextColor = self.legendTextColorOld
            self.legendMarkerFirst = self.legendMarkerFirstOld
            self.legendFrame = self.legendFrameOld
            self.legendFancyBox = self.legendFancyBoxOld
            self.polyCmapB10 = self.polyCmapB10Old
            self.polyCmapB20 = self.polyCmapB20Old
            self.polyCmapA20 = self.polyCmapA20Old
            self.polyBorderColor = self.polyBorderColorOld
            self.polyBorderLineW = self.polyBorderLineWOld
            self.polyTextStyle = self.polyTextStyleOld
            self.polyTextColor = self.polyTextColorOld
            self.polyLabelFont = self.polyLabelFontOld
            self.polyHaloLineW = self.polyHaloLineWOld
            self.polyHaloColor = self.polyHaloColorOld
            self.figAxis = self.figAxisOld
            self.dpi = self.dpiOld

        if self.radioButtonPng.isChecked():
            self.extension = 'png'
        else: self.extension = 'jpg'
        # format за подаване на данните към функцията
        self.legendNumCol = self.legendNumCol.strip()
        self.polyLabelFont = self.polyLabelFont.strip()
        self.polyTextStyle = self.polyTextStyle.lower().strip()
        self.polyBorderLineW = self.polyBorderLineW.strip()
        self.polyBorderColor = self.polyBorderColor.lower().strip()
        self.polyTextColor = self.polyTextColor.lower().strip()
        self.polyHaloLineW = self.polyHaloLineW.strip()
        self.polyHaloColor = self.polyHaloColor.lower().strip()
        self.legendFontSize = self.legendFontSize.strip()
        self.legendTitleFontSize = self.legendTitleFontSize.strip()
        self.legendMarkerSize = self.legendMarkerSize.strip()
        self.legendBackgroundColor = self.legendBackgroundColor.strip()
        self.legendTextColor = self.legendTextColor.lower().strip()
        self.polyCmapB10 = self.polyCmapB10.lower().strip()
        self.polyCmapB20 = self.polyCmapB20.lower().strip()
        self.polyCmapA20 = self.polyCmapA20.lower().strip()
        self.legendLoc = self.legendLoc.lower()
        self.savingLabel.setText("Saving figure...")
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.figureSave, self.figPath.text(), self.extension, self.propForExport, self.gdfForExport,
                 self.legendNumCol, self.polyLabelFont, self.polyTextStyle, self.polyBorderLineW,
                 self.polyBorderColor, self.polyTextColor, self.polyHaloLineW, self.polyHaloColor,
                 self.legendLoc, self.legendFontSize, self.legendTitleFontSize, self.legendMarkerSize,
                 self.legendFrame, self.legendFancyBox, self.legendBackgroundColor, self.legendTextColor,
                 self.legendMarkerFirst, self.legendOptions, self.polyCmapB10, self.polyCmapB20,
                 self.polyCmapA20,self.figAxis, self.dpi, self.combinedVoronoiFlag))

        self.mapDisabled = False
        self.excelDisabled = False
        if self.saveXlsLabel.isEnabled() and self.yesSaveXlsxButton.isChecked():
            self.excelDisabled = True
        if self.mapExportLabel.isEnabled() and self.yesSaveMIButton.isChecked():
            self.mapDisabled = True
        props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton,
                 self.excelPathLabel, self.browseExcelPushButton, self.excelPath,
                 self.saveFigLabel, self.yesSaveFigButton, self.noSaveFigButton,
                 self.figPath, self.figPathLabel, self.browseFigPushButton,
                 self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton,
                 self.mapExportLabel, self.mapInfoPath, self.browseMapPushButton,
                 self.backPushButton, self.saveExcelPushButton, self.saveFigPushButton,
                 self.settingsPushButton, self.exportPushButton,self.radioButtonJPG,
                 self.radioButtonPng, self.figExtensionLabel]
        for prop in props:
            prop.setDisabled(True)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(self.figureSaved)

    def figureSaved(self):
        if self.excelDisabled is True:
            props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton,
                     self.excelPath, self.excelPathLabel, self.browseExcelPushButton,
                     self.saveExcelPushButton]
            for prop in props:
                prop.setEnabled(True)
        else:
            props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton]
            for prop in props:
                prop.setEnabled(True)

        if self.mapDisabled is True:
            props = [self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton,
                     self.mapExportLabel, self.mapInfoPath, self.browseMapPushButton,
                     self.exportPushButton]
            for prop in props:
                prop.setEnabled(True)
        else:
            props = [self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton]
            for prop in props:
                prop.setEnabled(True)

        props = [self.saveFigLabel, self.yesSaveFigButton, self.noSaveFigButton,
                 self.figPath, self.figPathLabel, self.browseFigPushButton,
                 self.backPushButton, self.figExtensionLabel, self.radioButtonJPG, self.radioButtonPng]
        for prop in props:
            prop.setEnabled(True)
        if self.radioButtonPng.isChecked() or self.radioButtonJPG.isChecked():
            self.saveFigPushButton.setEnabled(True)
            self.settingsPushButton.setEnabled(True)

        if self.figSavedTimes == 1:
            self.savingLabel.setText(f"Figure file saved {self.figSavedTimes} time!")
            self.figSavedTimes = self.figSavedTimes + 1
        else:
            self.savingLabel.setText(f"Figure file saved {self.figSavedTimes} times!")
            self.figSavedTimes = self.figSavedTimes + 1

    def mapInfoSaved(self):
        if self.excelDisabled is True:
            props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton,
                     self.excelPath, self.excelPathLabel, self.browseExcelPushButton,
                     self.saveExcelPushButton]
            for prop in props:
                prop.setEnabled(True)
        else:
            props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton]
            for prop in props:
                prop.setEnabled(True)

        if self.figureDisabled is True:
            props = [self.figPathLabel, self.figPath, self.yesSaveFigButton,
                     self.noSaveFigButton, self.saveFigLabel, self.browseFigPushButton,
                     self.figExtensionLabel, self.radioButtonJPG, self.radioButtonPng,
                     self.settingsPushButton]
            for prop in props:
                prop.setEnabled(True)
            if self.radioFlag is True:
                self.saveFigPushButton.setEnabled(True)
        else:
            props = [self.yesSaveFigButton,self.noSaveFigButton, self.saveFigLabel]
            for prop in props:
                prop.setEnabled(True)

        props = [self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton,
                 self.mapInfoPath, self.mapExportLabel, self.browseMapPushButton,
                 self.backPushButton, self.exportPushButton]
        for prop in props:
            prop.setEnabled(True)
        if self.mapInfoSavedTimes == 1:
            self.savingLabel.setText(f"MapInfo files saved {self.mapInfoSavedTimes} time!")
            self.mapInfoSavedTimes = self.mapInfoSavedTimes + 1
        else:
            self.savingLabel.setText(f"MapInfo files saved {self.mapInfoSavedTimes} times!")
            self.mapInfoSavedTimes = self.mapInfoSavedTimes + 1

    def saveMapInfo(self):
        self.savingLabel.setText("Saving MapInfo files...")
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.mapInfoSave, self.gdfForExport, self.mapInfoPath.text(), self.propForExport))
        self.radioFlag = False
        self.figureDisabled = False
        self.excelDisabled = False
        if self.saveFigLabel.isEnabled() and self.yesSaveFigButton.isChecked():
            if self.radioButtonPng.isChecked() or self.radioButtonJPG.isChecked():
                self.radioFlag = True
            self.figureDisabled = True
        if self.saveXlsLabel.isEnabled() and self.yesSaveXlsxButton.isChecked():
            self.excelDisabled = True
        props = [self.saveXlsLabel, self.yesSaveXlsxButton, self.noSaveXlsxButton,
                 self.excelPathLabel, self.browseExcelPushButton, self.excelPath,
                 self.saveFigLabel, self.yesSaveFigButton, self.noSaveFigButton,
                 self.figPath, self.figPathLabel, self.browseFigPushButton,
                 self.saveMILabel, self.yesSaveMIButton, self.noSaveMIButton,
                 self.mapExportLabel, self.mapInfoPath, self.browseMapPushButton,
                 self.backPushButton, self.saveExcelPushButton, self.saveFigPushButton,
                 self.settingsPushButton, self.exportPushButton,self.radioButtonJPG,
                 self.radioButtonPng, self.figExtensionLabel]
        for prop in props:
            prop.setDisabled(True)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(self.mapInfoSaved)

    def enableSaveFigure(self):
        self.saveFigPushButton.setEnabled(True)

    def excelFileBrowser(self):
        saveLocation = QFileDialog.getExistingDirectory(None, "Select Location",
                                                        self.desktop)
        self.excelSaveLocation = saveLocation
        self.excelPath.setText(self.excelSaveLocation)

    def figFileBrowser(self):
        saveLocation = QFileDialog.getExistingDirectory(None, "Select Location",
                                                        self.desktop)
        self.figSaveLocation = saveLocation
        self.figPath.setText(self.figSaveLocation)

    def mapInfoFileBrowser(self):
        saveLocation = QFileDialog.getExistingDirectory(None, "Select Location",
                                                        self.desktop)
        self.mapInfoSaveLocation = saveLocation
        self.mapInfoPath.setText(self.mapInfoSaveLocation)

    def enableExcel(self):
        props = [self.excelPath, self.browseExcelPushButton, self.excelPathLabel,
                 self.saveExcelPushButton]
        for prop in props:
            prop.setEnabled(True)
        self.excelPath.setText(self.desktop)

    def enableFigure(self):
        props = [self.figPath, self.browseFigPushButton, self.figPathLabel,
                 self.figExtensionLabel, self.radioButtonJPG, self.radioButtonPng, self.settingsPushButton]
        for prop in props:
            prop.setEnabled(True)
        self.figPath.setText(self.desktop)

    def enableMapInfo(self):
        props = [self.mapExportLabel, self.browseMapPushButton, self.mapInfoPath,
                 self.exportPushButton]
        for prop in props:
            prop.setEnabled(True)
        self.mapInfoPath.setText(self.desktop)

    def disableExcel(self):
        self.excelPath.clear()
        self.excelPath.setEnabled(False)
        self.browseExcelPushButton.setEnabled(False)
        self.excelPathLabel.setEnabled(False)
        self.saveExcelPushButton.setEnabled(False)

    def disableFigure(self):
        self.figPath.clear()
        self.figPath.setEnabled(False)
        self.browseFigPushButton.setEnabled(False)
        self.figPathLabel.setEnabled(False)
        self.figExtensionLabel.setEnabled(False)
        self.radioButtonJPG.setEnabled(False)
        self.radioButtonPng.setEnabled(False)
        self.figExtButtonGroup.setExclusive(False)
        if self.radioButtonPng.isChecked():
            self.radioButtonPng.setChecked(False)
        if self.radioButtonJPG.isChecked():
            self.radioButtonJPG.setChecked(False)
        self.figExtButtonGroup.setExclusive(True)
        self.saveFigPushButton.setEnabled(False)
        self.settingsPushButton.setDisabled(True)

    def disableMapInfo(self):
        self.mapInfoPath.clear()
        self.mapExportLabel.setEnabled(False)
        self.browseMapPushButton.setEnabled(False)
        self.mapInfoPath.setEnabled(False)
        self.exportPushButton.setEnabled(False)

    def setupUi(self, voronoiPlotterWindow, voronoiCreatorGUI):
        # ==================WINDOW, LAYOUT AND TITLE==================
        # WINDOW
        voronoiPlotterWindow.setObjectName("voronoiPlotterWindow")
        voronoiPlotterWindow.resize(585, 441)
        voronoiPlotterWindow.setMinimumSize(QtCore.QSize(0, 0))
        voronoiPlotterWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.voronoiPlotter = QtWidgets.QWidget(voronoiPlotterWindow)
        self.voronoiPlotter.setObjectName("voronoiPlotter")
        self.gridLayout = QtWidgets.QGridLayout(self.voronoiPlotter)
        self.gridLayout.setObjectName("gridLayout")
        self.plotGridLayout = QtWidgets.QGridLayout()
        self.plotGridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.plotGridLayout.setContentsMargins(5, 5, 5, 5)
        self.plotGridLayout.setSpacing(10)
        self.plotGridLayout.setObjectName("plotGridLayout")
        self.voronoiPlotLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.voronoiPlotLabel.setFont(font)
        self.voronoiPlotLabel.setObjectName("voronoiPlotLabel")
        self.plotGridLayout.addWidget(self.voronoiPlotLabel, 1, 1, 1, 2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        # ==================EXCEL CHOICE LABEL,CHOICE BUTTONS, PATH LABEL, OPENER, PATH LINE EDIT==================
        # EXCEL CHOICE LABEL
        self.saveXlsLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.saveXlsLabel.setFont(font)
        self.saveXlsLabel.setObjectName("saveXlsLabel")
        self.plotGridLayout.addWidget(self.saveXlsLabel, 2, 1, 1, 1)

        # EXCEL CHOICE BUTTONS
        self.yes_no_saveXlsx_HLayout = QtWidgets.QHBoxLayout()
        self.yes_no_saveXlsx_HLayout.setObjectName("yes_no_saveXlsx_HLayout")
        self.yesSaveXlsxButton = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.yesSaveXlsxButton.setFont(font)
        self.yesSaveXlsxButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.yesSaveXlsxButton.setObjectName("yesSaveXlsxButton")
        self.saveXlsxbuttonGroup = QtWidgets.QButtonGroup(voronoiPlotterWindow)
        self.saveXlsxbuttonGroup.setObjectName("saveXlsxbuttonGroup")
        self.saveXlsxbuttonGroup.addButton(self.yesSaveXlsxButton)
        self.yes_no_saveXlsx_HLayout.addWidget(self.yesSaveXlsxButton)
        self.noSaveXlsxButton = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.noSaveXlsxButton.setFont(font)
        self.noSaveXlsxButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.noSaveXlsxButton.setObjectName("noSaveXlsxButton")
        self.saveXlsxbuttonGroup.addButton(self.noSaveXlsxButton)
        self.yes_no_saveXlsx_HLayout.addWidget(self.noSaveXlsxButton)
        self.plotGridLayout.addLayout(self.yes_no_saveXlsx_HLayout, 2, 2, 1, 1)
        self.yesSaveXlsxButton.toggled.connect(self.enableExcel)
        self.noSaveXlsxButton.toggled.connect(self.disableExcel)

        # EXCEL PATH LABEL
        self.excelPathLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.excelPathLabel.setFont(font)
        self.excelPathLabel.setObjectName("excelPathLabel")
        self.plotGridLayout.addWidget(self.excelPathLabel, 3, 1, 1, 1)
        self.excelPathLabel.setDisabled(True)

        # EXCEL OPENER
        self.browseExcelPushButton = QtWidgets.QPushButton(self.voronoiPlotter)
        self.browseExcelPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browseExcelPushButton.setFont(font)
        self.browseExcelPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browseExcelPushButton.setObjectName("browseExcelPushButton")
        self.plotGridLayout.addWidget(self.browseExcelPushButton, 3, 2, 1, 1,
                                      QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.browseExcelPushButton.setDisabled(True)
        self.browseExcelPushButton.clicked.connect(self.excelFileBrowser)

        # EXCEL PATH LINE EDIT
        self.excelPath = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.excelPath.setFont(font)
        self.excelPath.setObjectName("excelPath")
        self.plotGridLayout.addWidget(self.excelPath, 4, 1, 1, 2)
        self.excelPath.setDisabled(True)

        # ==================FIGURE CHOICE LABEL,CHOICE BUTTONS, PATH LABEL, OPENER==================
        # ==================FIGURE PATH LINE EDIT, EXTENSION LABEL, EXTENSION BUTTONS==================
        # FIGURE CHOICE LABEL
        self.saveFigLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.saveFigLabel.setFont(font)
        self.saveFigLabel.setObjectName("saveFigLabel")
        self.plotGridLayout.addWidget(self.saveFigLabel, 5, 1, 1, 1)

        # FIGURE CHOICE BUTTONS
        self.yes_no_saveFig_HLayout = QtWidgets.QHBoxLayout()
        self.yes_no_saveFig_HLayout.setObjectName("yes_no_saveFig_HLayout")
        self.yesSaveFigButton = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.yesSaveFigButton.setFont(font)
        self.yesSaveFigButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.yesSaveFigButton.setObjectName("yesSaveFigButton")
        self.saveFigbuttonGroup = QtWidgets.QButtonGroup(voronoiPlotterWindow)
        self.saveFigbuttonGroup.setObjectName("saveFigbuttonGroup")
        self.saveFigbuttonGroup.addButton(self.yesSaveFigButton)
        self.yes_no_saveFig_HLayout.addWidget(self.yesSaveFigButton)
        self.noSaveFigButton = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.noSaveFigButton.setFont(font)
        self.noSaveFigButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.noSaveFigButton.setObjectName("noSaveFigButton")
        self.saveFigbuttonGroup.addButton(self.noSaveFigButton)
        self.yes_no_saveFig_HLayout.addWidget(self.noSaveFigButton)
        self.plotGridLayout.addLayout(self.yes_no_saveFig_HLayout, 5, 2, 1, 1)
        self.yesSaveFigButton.toggled.connect(self.enableFigure)
        self.noSaveFigButton.toggled.connect(self.disableFigure)

        #FIGURE PATH LABEL
        self.figPathLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.figPathLabel.setFont(font)
        self.figPathLabel.setObjectName("figPathLabel")
        self.plotGridLayout.addWidget(self.figPathLabel, 6, 1, 1, 1)
        self.figPathLabel.setDisabled(True)

        # FIGURE OPENER
        self.browseFigPushButton = QtWidgets.QPushButton(self.voronoiPlotter)
        self.browseFigPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browseFigPushButton.setFont(font)
        self.browseFigPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browseFigPushButton.setObjectName("browseFigPushButton")
        self.plotGridLayout.addWidget(self.browseFigPushButton, 6, 2, 1, 1,
                                      QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.browseFigPushButton.setDisabled(True)
        self.browseFigPushButton.clicked.connect(self.figFileBrowser)

        #FIGURE PATH LINE EDIT
        self.figPath = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.figPath.setFont(font)
        self.figPath.setObjectName("figPath")
        self.plotGridLayout.addWidget(self.figPath, 7, 1, 1, 2)
        self.figPath.setDisabled(True)

        #FIGURE EXTENSION LABEL
        self.figExtensionLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.figExtensionLabel.setFont(font)
        self.figExtensionLabel.setObjectName("figExtensionLabel")
        self.plotGridLayout.addWidget(self.figExtensionLabel, 11, 1, 1, 2,
                                      QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.figExtensionLabel.setDisabled(True)

        #PNG AND JPG BUTTONS
        self.png_jpg_HLayout = QtWidgets.QHBoxLayout()
        self.png_jpg_HLayout.setObjectName("png_jpg_HLayout")
        self.radioButtonPng = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.radioButtonPng.setFont(font)
        self.radioButtonPng.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButtonPng.setObjectName("radioButtonPng")
        self.radioButtonPng.setDisabled(True)
        self.figExtButtonGroup = QtWidgets.QButtonGroup(voronoiPlotterWindow)
        self.figExtButtonGroup.setObjectName("figExtButtonGroup")
        self.figExtButtonGroup.addButton(self.radioButtonPng)
        self.png_jpg_HLayout.addWidget(self.radioButtonPng, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.radioButtonJPG = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.radioButtonJPG.setFont(font)
        self.radioButtonJPG.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButtonJPG.setObjectName("radioButtonJPG")
        self.figExtButtonGroup.addButton(self.radioButtonJPG)
        self.png_jpg_HLayout.addWidget(self.radioButtonJPG, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.radioButtonJPG.setDisabled(True)
        self.plotGridLayout.addLayout(self.png_jpg_HLayout, 12, 1, 1, 2)
        self.radioButtonJPG.toggled.connect(self.enableSaveFigure)
        self.radioButtonPng.toggled.connect(self.enableSaveFigure)

        # ==================MapInfo CHOICE LABEL,CHOICE BUTTONS, PATH LABEL, OPENER, PATH LINE EDIT==================
        # MapInfo CHOICE LABEL
        self.saveMILabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.saveMILabel.setFont(font)
        self.saveMILabel.setObjectName("saveMILabel")
        self.plotGridLayout.addWidget(self.saveMILabel, 8, 1, 1, 1)

        # MapInfo CHOICE BUTTONS
        self.yes_no_saveMI_HLayout = QtWidgets.QHBoxLayout()
        self.yes_no_saveMI_HLayout.setObjectName("yes_no_saveMI_HLayout")
        self.yesSaveMIButton = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.yesSaveMIButton.setFont(font)
        self.yesSaveMIButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.yesSaveMIButton.setObjectName("yesSaveMIButton")
        self.saveMIbuttonGroup = QtWidgets.QButtonGroup(voronoiPlotterWindow)
        self.saveMIbuttonGroup.setObjectName("saveMIbuttonGroup")
        self.saveMIbuttonGroup.addButton(self.yesSaveMIButton)
        self.yes_no_saveMI_HLayout.addWidget(self.yesSaveMIButton)
        self.noSaveMIButton = QtWidgets.QRadioButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.noSaveMIButton.setFont(font)
        self.noSaveMIButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.noSaveMIButton.setObjectName("noSaveMIButton")
        self.saveMIbuttonGroup.addButton(self.noSaveMIButton)
        self.yes_no_saveMI_HLayout.addWidget(self.noSaveMIButton)
        self.plotGridLayout.addLayout(self.yes_no_saveMI_HLayout, 8, 2, 1, 1)
        self.yesSaveMIButton.toggled.connect(self.enableMapInfo)
        self.noSaveMIButton.toggled.connect(self.disableMapInfo)

        # MapInfo PATH LABEL
        self.mapExportLabel = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.mapExportLabel.setFont(font)
        self.mapExportLabel.setObjectName("mapExportLabel")
        self.plotGridLayout.addWidget(self.mapExportLabel, 9, 1, 1, 1)
        self.mapExportLabel.setDisabled(True)

        # MapInfo OPENER
        self.browseMapPushButton = QtWidgets.QPushButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browseMapPushButton.setFont(font)
        self.browseMapPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browseMapPushButton.setObjectName("browseMapPushButton")
        self.plotGridLayout.addWidget(self.browseMapPushButton, 9, 2, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.browseMapPushButton.setDisabled(True)
        self.browseMapPushButton.clicked.connect(self.mapInfoFileBrowser)

        # MapInfo LINE EDIT
        self.mapInfoPath = QtWidgets.QLabel(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.mapInfoPath.setFont(font)
        self.mapInfoPath.setObjectName("mapInfoPath")
        self.plotGridLayout.addWidget(self.mapInfoPath, 10, 1, 1, 2)
        self.mapInfoPath.setDisabled(True)

        # ==================ACTION BUTTONS==================
        self.boxes_HLayout = QtWidgets.QHBoxLayout()
        self.boxes_HLayout.setObjectName("boxes_HLayout")

        # BACK BUTTON
        self.backPushButton = QtWidgets.QPushButton(self.voronoiPlotter, clicked = lambda: self.backButtonOperation(voronoiGui=voronoiCreatorGUI, plotterW=voronoiPlotterWindow))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.backPushButton.setFont(font)
        self.backPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backPushButton.setObjectName("backPushButton")
        self.boxes_HLayout.addWidget(self.backPushButton)
        # SAVE EXCEL BUTTON
        self.saveExcelPushButton = QtWidgets.QPushButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.saveExcelPushButton.setFont(font)
        self.saveExcelPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveExcelPushButton.setObjectName("saveExcelPushButton")
        self.boxes_HLayout.addWidget(self.saveExcelPushButton)
        self.saveExcelPushButton.setDisabled(True)
        self.saveExcelPushButton.clicked.connect(self.saveExcelFile)

        # SAVE FIGURE BUTTON
        self.saveFigPushButton = QtWidgets.QPushButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.saveFigPushButton.setFont(font)
        self.saveFigPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveFigPushButton.setObjectName("saveFigPushButton")
        self.boxes_HLayout.addWidget(self.saveFigPushButton)
        self.saveFigPushButton.setDisabled(True)
        self.saveFigPushButton.clicked.connect(self.saveFig)
        # FIGURE OPTIONS BUTTON
        self.settingsPushButton = QtWidgets.QPushButton(self.voronoiPlotter, clicked = lambda: self.open_settings())
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.settingsPushButton.setFont(font)
        self.settingsPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.settingsPushButton.setObjectName("settingsPushButton")
        self.boxes_HLayout.addWidget(self.settingsPushButton)

        # MapInfo EXPORT BUTTON
        self.exportPushButton = QtWidgets.QPushButton(self.voronoiPlotter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.exportPushButton.setFont(font)
        self.exportPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exportPushButton.setObjectName("exportPushButton")
        self.boxes_HLayout.addWidget(self.exportPushButton)
        self.plotGridLayout.addLayout(self.boxes_HLayout, 13, 1, 1, 2)
        self.exportPushButton.setDisabled(True)
        self.exportPushButton.clicked.connect(self.saveMapInfo)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.savingLabel = QtWidgets.QLabel(self.voronoiPlotter)
        self.savingLabel.setObjectName(u"savingLabel")
        self.savingLabel.setFont(font)
        #self.gridLayout.addWidget(self.savingLabel, 1, 0, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.plotGridLayout.addWidget(self.savingLabel, 14, 1, 1, 2)



        self.gridLayout.addLayout(self.plotGridLayout, 0, 0, 1, 1)
        voronoiPlotterWindow.setCentralWidget(self.voronoiPlotter)

        self.retranslateUi(voronoiPlotterWindow)
        QtCore.QMetaObject.connectSlotsByName(voronoiPlotterWindow)

    def retranslateUi(self, voronoiPlotterWindow):
        _translate = QtCore.QCoreApplication.translate
        voronoiPlotterWindow.setWindowTitle(_translate("voronoiPlotterWindow", "Voronoi Plot"))
        self.figPathLabel.setText(_translate("voronoiPlotterWindow", "Select path for saving the figure:"))
        self.mapExportLabel.setText(_translate("voronoiPlotterWindow", "Select path for saving the  MapInfo export:"))
        self.browseFigPushButton.setText(_translate("voronoiPlotterWindow", "Browse"))
        self.saveXlsLabel.setText(_translate("voronoiPlotterWindow", "Do you want to save the output excel file?"))
        self.browseMapPushButton.setText(_translate("voronoiPlotterWindow", "Browse"))
        self.backPushButton.setText(_translate("voronoiPlotterWindow", "Back"))
        self.saveExcelPushButton.setText(_translate("voronoiPlotterWindow", "Save excel file"))
        self.saveFigPushButton.setText(_translate("voronoiPlotterWindow", "Save figure"))
        self.settingsPushButton.setText(_translate("voronoiPlotterWindow", "Settings"))
        self.exportPushButton.setText(_translate("voronoiPlotterWindow", "Export to MapInfo"))
        self.browseExcelPushButton.setText(_translate("voronoiPlotterWindow", "Browse"))
        self.excelPathLabel.setText(_translate("voronoiPlotterWindow", "Select path for saving the excel file:"))
        self.voronoiPlotLabel.setText(_translate("voronoiPlotterWindow", "Voronoi Plot"))
        self.figExtensionLabel.setText(_translate("voronoiPlotterWindow", "Select extension of the figure"))
        self.saveFigLabel.setText(_translate("voronoiPlotterWindow", "Do you want to save the output figure?"))
        self.radioButtonPng.setText(_translate("voronoiPlotterWindow", ".png"))
        self.radioButtonJPG.setText(_translate("voronoiPlotterWindow", ".jpg"))
        self.saveMILabel.setText(_translate("voronoiPlotterWindow", "Do you want to save the MapInfo Tab file?"))
        self.yesSaveXlsxButton.setText(_translate("voronoiPlotterWindow", "Yes"))
        self.noSaveXlsxButton.setText(_translate("voronoiPlotterWindow", "No"))
        self.yesSaveFigButton.setText(_translate("voronoiPlotterWindow", "Yes"))
        self.noSaveFigButton.setText(_translate("voronoiPlotterWindow", "No"))
        self.yesSaveMIButton.setText(_translate("voronoiPlotterWindow", "Yes"))
        self.noSaveMIButton.setText(_translate("voronoiPlotterWindow", "No"))
        self.savingLabel.setText(_translate("voronoiPlotterWindow", ""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    voronoiPlotterWindow = QtWidgets.QMainWindow()
    ui = Ui_plotter()
    ui.setupUi(voronoiPlotterWindow)
    voronoiPlotterWindow.show()
    sys.exit(app.exec_())
