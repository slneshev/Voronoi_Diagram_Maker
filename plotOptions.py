from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_plotOptions(object):

    def __init__(self):
        self.separators = [".#", "(#)", "_#", "[#]", "{#}", "\\#", "|#", "/#", "-#", "*#"]
        # тук може да се добавят или премахват разделителите
        self.saveFlag = True
        self.legendNumCol_Settings = 1
        self.legendLoc_Settings = 'Best'
        self.legendLocIndex_Settings = 0
        self.legendMarkerSize_Settings = 1
        self.legendFontSize_Settings = 2
        self.legendTitle_Settings = ''
        self.legendTitleFontSize_Settings = 3
        self.legendBackgroundColor_Settings = 'inherit'
        self.legendTextColor_Settings = 'black'
        self.polyCmapB10_Settings = 'tab10'
        self.polyCmapB20_Settings = 'tab20'
        self.polyCmapA20_Settings = 'hsv'
        self.polyBorderColor_Settings = 'black'
        self.polyBorderLineW_Settings = 0.2
        self.polyTextStyle_Settings = 'Normal'
        self.polyTextStyleIndex_Settings = 0
        self.polyTextColor_Settings = 'black'
        self.polyHaloLineW_Settings = 0.4
        self.polyHaloColor_Settings = 'white'
        self.figAxis_Settings = True
        self.separatorIndex = 0
        self.stateLegend = True
        self.stateMarker = True
        self.stateLegendFrame = True
        self.stateAxis = True
        self.stateLegendFancy = True

        
    def okButtonFunc(self, settingsWindow):
        self.legendOptions_Settings = self.legendTrue.isChecked()
        self.stateLegend = self.checkRadioState(self.legendOptions_Settings)
        self.legendNumCol_Settings = self.ncolLineEdit.text()
        self.legendLoc_Settings = self.locComboBox.currentText()
        self.legendLocIndex_Settings = self.locComboBox.currentIndex()
        self.legendMarkerSize_Settings = self.markerScaleLineEdit.text()
        self.legendFontSize_Settings = self.title_fontsizeLineEdit.text()
        self.legendTitle_Settings = self.titleLineEdit.text()
        self.legendTitleFontSize_Settings = self.titleFontSizeLineEdit.text()
        self.legendBackgroundColor_Settings = self.facecolorLineEdit.text()
        self.legendTextColor_Settings = self.labelcolorLineEdit.text()
        self.legendMarkerFirst_Settings = self.markerfirstTrue.isChecked()
        self.stateMarker = self.checkRadioState(self.legendMarkerFirst_Settings)
        self.legendFrame_Settings = self.frameOnTrue.isChecked()
        self.stateLegendFrame = self.checkRadioState(self.legendFrame_Settings)
        self.legendFancyBox_Settings = self.fancyboxTrue.isChecked()
        self.stateLegendFancy = self.checkRadioState(self.legendFancyBox_Settings)
        self.polyCmapB10_Settings = self.cmap10LineEdit.text()
        self.polyCmapB20_Settings = self.cmap10_20LineEdit.text()
        self.polyCmapA20_Settings = self.cmap20LineEdit.text()
        self.polyBorderColor_Settings = self.edgeColourLineEdit.text()
        self.polyBorderLineW_Settings = self.lineWdthLineEdit.text()
        self.polyTextStyle_Settings = self.fontWeightComboBox.currentText()
        self.polyTextStyleIndex_Settings = self.fontWeightComboBox.currentIndex()
        self.polyTextColor_Settings = self.textColorLineEdit.text()
        self.polyHaloLineW_Settings = self.haloLineWidthLineEdit.text()
        self.polyHaloColor_Settings = self.haloColorLineEdit.text()
        self.figAxis_Settings = self.yesAxisRadioButton.isChecked()
        self.stateAxis = self.checkRadioState(self.figAxis_Settings)
        self.separatorIndex = self.separatorComboBox.currentIndex()
        self.saveFlag = True
        settingsWindow.hide()
    
    def checkRadioState(self, radioTrue):
        if radioTrue:
            state = True
        else: state = False
        return state
    
    def cancelButtonFunc(self, settingsWindow):
        if self.stateLegend == True:
            self.legendTrue.setChecked(True)
        else: self.legendFalse.setChecked(True)
        self.ncolLineEdit.setText(str(self.legendNumCol_Settings))
        self.locComboBox.setCurrentIndex(self.legendLocIndex_Settings)
        self.markerScaleLineEdit.setText(str(self.legendMarkerSize_Settings))
        self.title_fontsizeLineEdit.setText(str(self.legendTitleFontSize_Settings))
        self.titleLineEdit.setText(str(self.legendTitle_Settings))
        self.titleFontSizeLineEdit.setText(str(self.legendTitleFontSize_Settings))
        self.facecolorLineEdit.setText(str(self.legendBackgroundColor_Settings))
        self.labelcolorLineEdit.setText(str(self.legendTextColor_Settings))

        if self.stateMarker == True:
            self.markerfirstTrue.setChecked(True)
        else: self.markerfirstFalse.setChecked(True)

        if self.stateLegendFrame == True:
            self.frameOnTrue.setChecked(True)
        else: self.frameOnFalse.setChecked(True)

        if self.stateLegendFancy == True:
            self.fancyboxTrue.setChecked(True)
        else: self.fancyboxFalse.setChecked(True)

        self.cmap10LineEdit.setText(str(self.polyCmapB10_Settings))
        self.cmap10_20LineEdit.setText(str(self.polyCmapB20_Settings))
        self.cmap20LineEdit.setText(str(self.polyCmapA20_Settings))
        self.edgeColourLineEdit.setText(str(self.polyBorderColor_Settings))
        self.lineWdthLineEdit.setText(str(self.polyBorderLineW_Settings))
        self.fontWeightComboBox.setCurrentIndex(self.polyTextStyleIndex_Settings)
        self.textColorLineEdit.setText(str(self.polyTextColor_Settings))
        self.haloLineWidthLineEdit.setText(str(self.polyHaloLineW_Settings))
        self.haloColorLineEdit.setText(str(self.polyHaloColor_Settings))
        if self.stateAxis == True:
            self.yesAxisRadioButton.setChecked(True)
        else:
            self.noAxisRadioButton.setChecked(True)
        self.separatorComboBox.setCurrentIndex(self.separatorIndex)
        self.saveFlag = False
        settingsWindow.hide()

    def disableLegend(self):
        for option in self.legendOptions:
            option.setDisabled(True)

    def enableLegend(self):
        for option in self.legendOptions:
            option.setEnabled(True)

    def setupUi(self, SettingsWindow):
        lineFont = QtGui.QFont()
        lineFont.setFamily("Arial")
        lineFont.setPointSize(10)
        
        fontLabel = QtGui.QFont()
        fontLabel.setFamily("Arial")
        fontLabel.setPointSize(12)
        
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(1105, 569)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.legend_HLayout = QtWidgets.QHBoxLayout()
        self.legend_HLayout.setObjectName("legend_HLayout")

        # TITLE
        self.plotOptionsLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.plotOptionsLabel.setFont(font)
        self.plotOptionsLabel.setObjectName("plotOptionsLabel")
        self.gridLayout.addWidget(self.plotOptionsLabel, 0, 0, 1, 2, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # ==================LEGEND OPTIONS==================
        # LEGEND OPTIONS LABEL
        self.legendOptionsLabel = QtWidgets.QLabel(self.centralwidget)
        self.legendOptionsLabel.setFont(font)
        self.legendOptionsLabel.setObjectName("legendOptionsLabel")
        self.gridLayout.addWidget(self.legendOptionsLabel, 2, 0, 1, 1)

        # LEGEND LABEL AND YES/NO BUTTONS
        self.legendLabel = QtWidgets.QLabel(self.centralwidget)
        self.legendLabel.setFont(fontLabel)
        self.legendLabel.setObjectName("legendLabel")
        self.legend_HLayout.addWidget(self.legendLabel)
        self.legendYesNo_HLayout = QtWidgets.QHBoxLayout()
        self.legendYesNo_HLayout.setObjectName("legendYesNo_HLayout")
        self.legendTrue = QtWidgets.QRadioButton(self.centralwidget)
        self.legendTrue.setFont(lineFont)
        self.legendTrue.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.legendTrue.setChecked(True)
        self.legendTrue.setObjectName("legendTrue")
        self.legendButtonGroup = QtWidgets.QButtonGroup(SettingsWindow)
        self.legendButtonGroup.setObjectName("legendButtonGroup")
        self.legendButtonGroup.addButton(self.legendTrue)
        self.legendYesNo_HLayout.addWidget(self.legendTrue)
        self.legendFalse = QtWidgets.QRadioButton(self.centralwidget)
        self.legendFalse.setFont(lineFont)
        self.legendFalse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.legendFalse.setObjectName("legendFalse")
        self.legendButtonGroup.addButton(self.legendFalse)
        self.legendYesNo_HLayout.addWidget(self.legendFalse)
        self.legend_HLayout.addLayout(self.legendYesNo_HLayout)
        self.gridLayout.addLayout(self.legend_HLayout, 3, 0, 1, 1)
        self.legendFalse.toggled.connect(self.disableLegend)
        self.legendTrue.toggled.connect(self.enableLegend)

        # LEGEND NUMBER OF COLUMNS LABEL AND LINE EDIT
        self.legendNumCol_HLayout = QtWidgets.QHBoxLayout()
        self.legendNumCol_HLayout.setObjectName("legendNumCol_HLayout")
        self.ncolLabel = QtWidgets.QLabel(self.centralwidget)
        self.ncolLabel.setFont(fontLabel)
        self.ncolLabel.setObjectName("ncolLabel")
        self.legendNumCol_HLayout.addWidget(self.ncolLabel)
        self.ncolLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ncolLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.ncolLineEdit.setObjectName("ncolLineEdit")
        self.ncolLineEdit.setText('1')
        self.ncolLineEdit.setFont(lineFont)
        self.legendNumCol_HLayout.addWidget(self.ncolLineEdit)
        self.gridLayout.addLayout(self.legendNumCol_HLayout, 4, 0, 1, 1)

        # LEGEND LOCATION LABEL AND LINE EDIT
        self.legendLoc_HLayout = QtWidgets.QHBoxLayout()
        self.legendLoc_HLayout.setObjectName("legendLoc_HLayout")
        self.locLabel = QtWidgets.QLabel(self.centralwidget)

        self.locLabel.setFont(fontLabel)
        self.locLabel.setObjectName("locLabel")
        self.legendLoc_HLayout.addWidget(self.locLabel)
        self.locComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.locComboBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.locComboBox.setObjectName("locComboBox")
        self.locComboBox.addItems([ 'Best', 'Upper left', 'Upper right', 'Lower left', 'Lower right',
                                    'Upper center', 'Lower center', 'Center left', 'Center right', 'Center'])
        self.locComboBox.setFont(lineFont)
        self.legendLoc_HLayout.addWidget(self.locComboBox)
        self.gridLayout.addLayout(self.legendLoc_HLayout, 5, 0, 1, 1)

        # LEGEND MARKER SIZE LABEL AND LINE EDIT
        self.legendMarkerSize_HLayout = QtWidgets.QHBoxLayout()
        self.legendMarkerSize_HLayout.setObjectName("legendMarkerSize_HLayout")
        self.markerScaleLabel = QtWidgets.QLabel(self.centralwidget)
        self.markerScaleLabel.setFont(fontLabel)
        self.markerScaleLabel.setObjectName("markerScaleLabel")
        self.legendMarkerSize_HLayout.addWidget(self.markerScaleLabel)
        self.markerScaleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.markerScaleLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.markerScaleLineEdit.setObjectName("markerScaleLineEdit")
        self.markerScaleLineEdit.setText('0.2')
        self.markerScaleLineEdit.setFont(lineFont)

        self.legendMarkerSize_HLayout.addWidget(self.markerScaleLineEdit)
        self.gridLayout.addLayout(self.legendMarkerSize_HLayout, 6, 0, 1, 1)

        # LEGEND FONT SIZE LABEL AND LINE EDIT
        self.legendFontSize_HLayout = QtWidgets.QHBoxLayout()
        self.legendFontSize_HLayout.setObjectName("legendFontSize_HLayout")
        self.title_fontsizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.title_fontsizeLabel.setFont(fontLabel)
        self.title_fontsizeLabel.setObjectName("title_fontsizeLabel")
        self.legendFontSize_HLayout.addWidget(self.title_fontsizeLabel)
        self.title_fontsizeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.title_fontsizeLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.title_fontsizeLineEdit.setObjectName("title_fontsizeLineEdit")
        self.title_fontsizeLineEdit.setText('2')
        self.title_fontsizeLineEdit.setFont(lineFont)
        self.legendFontSize_HLayout.addWidget(self.title_fontsizeLineEdit)
        self.gridLayout.addLayout(self.legendFontSize_HLayout, 7, 0, 1, 1)

        # LEGEND TITLE LABEL AND LINE EDIT
        self.legendTitle_HLayout = QtWidgets.QHBoxLayout()
        self.legendTitle_HLayout.setObjectName("legendTitle_HLayout")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setFont(fontLabel)
        self.titleLabel.setObjectName("titleLabel")
        self.legendTitle_HLayout.addWidget(self.titleLabel)
        self.titleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.titleLineEdit.setObjectName("titleLineEdit")
        self.titleLineEdit.setFont(lineFont)

        self.legendTitle_HLayout.addWidget(self.titleLineEdit)
        self.gridLayout.addLayout(self.legendTitle_HLayout, 8, 0, 1, 1)

        # LEGEND TITLE FONT SIZE LABEL AND LINE EDIT
        self.legendTitleFontSize_HLayout = QtWidgets.QHBoxLayout()
        self.legendTitleFontSize_HLayout.setObjectName("legendTitleFontSize_HLayout")
        self.titleFontSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleFontSizeLabel.setFont(fontLabel)
        self.titleFontSizeLabel.setObjectName("titleFontSizeLabel")
        self.legendTitleFontSize_HLayout.addWidget(self.titleFontSizeLabel)
        self.titleFontSizeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleFontSizeLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.titleFontSizeLineEdit.setObjectName("titleFontSizeLineEdit")
        self.titleFontSizeLineEdit.setText('3')
        self.titleFontSizeLineEdit.setFont(lineFont)

        self.legendTitleFontSize_HLayout.addWidget(self.titleFontSizeLineEdit)
        self.gridLayout.addLayout(self.legendTitleFontSize_HLayout, 9, 0, 1, 1)

        # LEGEND BACKGROUND COLOR LABEL AND LINE EDIT
        self.legendBackgroundColor_HLayout = QtWidgets.QHBoxLayout()
        self.legendBackgroundColor_HLayout.setObjectName("legendBackgroundColor_HLayout")
        self.facecolorLabel = QtWidgets.QLabel(self.centralwidget)
        self.facecolorLabel.setFont(fontLabel)
        self.facecolorLabel.setObjectName("facecolorLabel")
        self.legendBackgroundColor_HLayout.addWidget(self.facecolorLabel)
        self.facecolorLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.facecolorLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.facecolorLineEdit.setObjectName("facecolorLineEdit")
        self.facecolorLineEdit.setText('inherit')
        self.facecolorLineEdit.setFont(lineFont)

        self.legendBackgroundColor_HLayout.addWidget(self.facecolorLineEdit)
        self.gridLayout.addLayout(self.legendBackgroundColor_HLayout, 10, 0, 1, 1)

        # LEGEND TEXT COLOR LABEL AND LINE EDIT
        self.legendColorText_HLayout = QtWidgets.QHBoxLayout()
        self.legendColorText_HLayout.setObjectName("legendColorText_HLayout")
        self.labelcolorLabel = QtWidgets.QLabel(self.centralwidget)
        self.labelcolorLabel.setFont(fontLabel)
        self.labelcolorLabel.setObjectName("labelcolorLabel")
        self.legendColorText_HLayout.addWidget(self.labelcolorLabel)
        self.labelcolorLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.labelcolorLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.labelcolorLineEdit.setObjectName("labelcolorLineEdit")
        self.labelcolorLineEdit.setText('black')
        self.labelcolorLineEdit.setFont(lineFont)

        self.legendColorText_HLayout.addWidget(self.labelcolorLineEdit)
        self.gridLayout.addLayout(self.legendColorText_HLayout, 11, 0, 1, 1)

        # LEGEND MARKER FIRST LABEL, YES/NO BUTTONS
        self.legendMarkerFirst_HLayout = QtWidgets.QHBoxLayout()
        self.legendMarkerFirst_HLayout.setObjectName("legendMarkerFirst_HLayout")
        self.markerfirstLabel = QtWidgets.QLabel(self.centralwidget)
        self.markerfirstLabel.setFont(fontLabel)
        self.markerfirstLabel.setObjectName("markerfirstLabel")
        self.legendMarkerFirst_HLayout.addWidget(self.markerfirstLabel)
        self.legendMarkerFirstYesNo_HLayout = QtWidgets.QHBoxLayout()
        self.legendMarkerFirstYesNo_HLayout.setObjectName("legendMarkerFirstYesNo_HLayout")
        self.markerfirstTrue = QtWidgets.QRadioButton(self.centralwidget)
        self.markerfirstTrue.setFont(lineFont)
        self.markerfirstTrue.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.markerfirstTrue.setChecked(True)
        self.markerfirstTrue.setObjectName("markerfirstTrue")
        self.markerFirstButtonGroup = QtWidgets.QButtonGroup(SettingsWindow)
        self.markerFirstButtonGroup.setObjectName("markerFirstButtonGroup")
        self.markerFirstButtonGroup.addButton(self.markerfirstTrue)
        self.legendMarkerFirstYesNo_HLayout.addWidget(self.markerfirstTrue)
        self.markerfirstFalse = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.markerfirstFalse.setFont(lineFont)
        self.markerfirstFalse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.markerfirstFalse.setObjectName("markerfirstFalse")
        self.markerFirstButtonGroup.addButton(self.markerfirstFalse)
        self.legendMarkerFirstYesNo_HLayout.addWidget(self.markerfirstFalse)
        self.legendMarkerFirst_HLayout.addLayout(self.legendMarkerFirstYesNo_HLayout)
        self.gridLayout.addLayout(self.legendMarkerFirst_HLayout, 12, 0, 1, 1)

        # LEGEND FRAME LABEL AND YES/NO
        self.legendFrame_HLayout = QtWidgets.QHBoxLayout()
        self.legendFrame_HLayout.setObjectName("legendFrame_HLayout")
        self.frameOnLabel = QtWidgets.QLabel(self.centralwidget)
        self.frameOnLabel.setFont(fontLabel)
        self.frameOnLabel.setObjectName("frameOnLabel")
        self.legendFrame_HLayout.addWidget(self.frameOnLabel)
        self.legendFrameYesNo_HLayout = QtWidgets.QHBoxLayout()
        self.legendFrameYesNo_HLayout.setObjectName("legendFrameYesNo_HLayout")
        self.frameOnTrue = QtWidgets.QRadioButton(self.centralwidget)
        self.frameOnTrue.setFont(lineFont)
        self.frameOnTrue.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frameOnTrue.setChecked(True)
        self.frameOnTrue.setObjectName("frameOnTrue")
        self.frameButtonGroup = QtWidgets.QButtonGroup(SettingsWindow)
        self.frameButtonGroup.setObjectName("frameButtonGroup")
        self.frameButtonGroup.addButton(self.frameOnTrue)
        self.legendFrameYesNo_HLayout.addWidget(self.frameOnTrue)
        self.frameOnFalse = QtWidgets.QRadioButton(self.centralwidget)
        self.frameOnFalse.setFont(lineFont)
        self.frameOnFalse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frameOnFalse.setObjectName("frameOnFalse")
        self.frameButtonGroup.addButton(self.frameOnFalse)
        self.legendFrameYesNo_HLayout.addWidget(self.frameOnFalse)
        self.legendFrame_HLayout.addLayout(self.legendFrameYesNo_HLayout)
        self.gridLayout.addLayout(self.legendFrame_HLayout, 13, 0, 1, 1)

        # LEGEND FANCY BOX LABEL AND YES/NO
        self.legendFancyBox_HLayout = QtWidgets.QHBoxLayout()
        self.legendFancyBox_HLayout.setObjectName("legendFancyBox_HLayout")
        self.fancyboxLabel = QtWidgets.QLabel(self.centralwidget)
        self.fancyboxLabel.setFont(fontLabel)
        self.fancyboxLabel.setObjectName("fancyboxLabel")
        self.legendFancyBox_HLayout.addWidget(self.fancyboxLabel)
        self.legendFancyBoxYesNo_HLayout = QtWidgets.QHBoxLayout()
        self.legendFancyBoxYesNo_HLayout.setObjectName("legendFancyBoxYesNo_HLayout")
        self.fancyboxTrue = QtWidgets.QRadioButton(self.centralwidget)
        self.fancyboxTrue.setFont(lineFont)
        self.fancyboxTrue.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fancyboxTrue.setChecked(True)
        self.fancyboxTrue.setObjectName("fancyboxTrue")
        self.fancyBoxButtonGroup = QtWidgets.QButtonGroup(SettingsWindow)
        self.fancyBoxButtonGroup.setObjectName("fancyBoxButtonGroup")
        self.fancyBoxButtonGroup.addButton(self.fancyboxTrue)
        self.legendFancyBoxYesNo_HLayout.addWidget(self.fancyboxTrue)
        self.fancyboxFalse = QtWidgets.QRadioButton(self.centralwidget)
        self.fancyboxFalse.setFont(lineFont)
        self.fancyboxFalse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fancyboxFalse.setObjectName("fancyboxFalse")
        self.fancyBoxButtonGroup.addButton(self.fancyboxFalse)
        self.legendFancyBoxYesNo_HLayout.addWidget(self.fancyboxFalse)
        self.legendFancyBox_HLayout.addLayout(self.legendFancyBoxYesNo_HLayout)
        self.gridLayout.addLayout(self.legendFancyBox_HLayout, 14, 0, 1, 1)

        #DPI
        self.dpi_HLayout = QtWidgets.QHBoxLayout()
        self.dpi_HLayout.setObjectName(u"dpi_HLayout")
        self.dpiLabel = QtWidgets.QLabel(self.centralwidget)
        self.dpiLabel.setObjectName(u"dpiLabel")
        self.dpiLabel.setFont(fontLabel)
        self.dpi_HLayout.addWidget(self.dpiLabel)
        self.dpiLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.dpiLineEdit.setObjectName(u"dpiLineEdit")
        self.dpiLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.dpiLineEdit.setText('1200')
        self.dpiLineEdit.setFont(lineFont)
        self.dpi_HLayout.addWidget(self.dpiLineEdit)

        self.gridLayout.addLayout(self.dpi_HLayout, 15, 1, 1, 1)

        # LEGEND MORE OPTIONS LINK LABEL
        self.legendOptionsLinkLabel = QtWidgets.QLabel(self.centralwidget)
        self.legendOptionsLinkLabel.setFont(fontLabel)
        self.legendOptionsLinkLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.legendOptionsLinkLabel.setObjectName("legendOptionsLinkLabel")
        self.gridLayout.addWidget(self.legendOptionsLinkLabel, 18, 0, 1, 2)

        self.legendOptions = [self.title_fontsizeLabel, self.ncolLabel, self.ncolLineEdit,
                              self.locLabel, self.locComboBox, self.markerScaleLabel, self.markerScaleLineEdit,
                              self.titleFontSizeLabel, self.titleFontSizeLineEdit, self.title_fontsizeLineEdit,
                              self.title_fontsizeLineEdit, self.titleLabel, self.titleLineEdit, self.facecolorLineEdit,
                              self.facecolorLabel, self.labelcolorLabel, self.labelcolorLineEdit, self.markerfirstLabel,
                              self.markerfirstTrue, self.markerfirstFalse, self.frameOnLabel, self.frameOnTrue,
                              self.frameOnFalse,
                              self.fancyboxFalse, self.fancyboxTrue, self.fancyboxLabel]

        # ==================POLYGON OPTIONS==================
        # POLYGON OPTIONS LABEL
        self.polygonOptionslabel = QtWidgets.QLabel(self.centralwidget)
        self.polygonOptionslabel.setFont(fontLabel)
        self.polygonOptionslabel.setObjectName("polygonOptionslabel")
        self.gridLayout.addWidget(self.polygonOptionslabel, 2, 1, 1, 1)

        # POLYGON COLOR MAPS BELOW 10 LABEL AND LINE EDIT
        self.polyCmapBelow10_HLayout = QtWidgets.QHBoxLayout()
        self.polyCmapBelow10_HLayout.setObjectName("polyCmapBelow10_HLayout")
        self.cmap10Label = QtWidgets.QLabel(self.centralwidget)
        self.cmap10Label.setFont(fontLabel)
        self.cmap10Label.setObjectName("cmap10Label")
        self.polyCmapBelow10_HLayout.addWidget(self.cmap10Label)
        self.cmap10LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.cmap10LineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.cmap10LineEdit.setObjectName("cmap10LineEdit")
        self.cmap10LineEdit.setText('tab10')
        self.cmap10LineEdit.setFont(lineFont)

        self.polyCmapBelow10_HLayout.addWidget(self.cmap10LineEdit)
        self.gridLayout.addLayout(self.polyCmapBelow10_HLayout, 3, 1, 1, 1)

        # POLYGON COLOR MAP BELOW 20 LABEL AND LINE EDIT
        self.polyCmapBelow20_HLayout = QtWidgets.QHBoxLayout()
        self.polyCmapBelow20_HLayout.setObjectName("polyCmapBelow20_HLayout")
        self.cmap10_20 = QtWidgets.QLabel(self.centralwidget)
        self.cmap10_20.setFont(fontLabel)
        self.cmap10_20.setObjectName("cmap10_20")
        self.polyCmapBelow20_HLayout.addWidget(self.cmap10_20)
        self.cmap10_20LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.cmap10_20LineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.cmap10_20LineEdit.setObjectName("cmap10_20LineEdit")
        self.cmap10_20LineEdit.setText('tab20')
        self.cmap10_20LineEdit.setFont(lineFont)

        self.polyCmapBelow20_HLayout.addWidget(self.cmap10_20LineEdit)
        self.gridLayout.addLayout(self.polyCmapBelow20_HLayout, 4, 1, 1, 1)

        # POLYGON COLOR MAP ABOVE 20 LABEL AND LINE EDIT
        self.polyCmapAbove20_HLayout = QtWidgets.QHBoxLayout()
        self.polyCmapAbove20_HLayout.setObjectName("polyCmapAbove20_HLayout")
        self.cmap20 = QtWidgets.QLabel(self.centralwidget)

        self.cmap20.setFont(fontLabel)
        self.cmap20.setObjectName("cmap20")
        self.polyCmapAbove20_HLayout.addWidget(self.cmap20)
        self.cmap20LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.cmap20LineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.cmap20LineEdit.setObjectName("cmap20LineEdit")
        self.cmap20LineEdit.setText('hsv')
        self.cmap20LineEdit.setFont(lineFont)
        self.polyCmapAbove20_HLayout.addWidget(self.cmap20LineEdit)
        self.gridLayout.addLayout(self.polyCmapAbove20_HLayout, 5, 1, 1, 1)

        # POLYGON BORDER COLOR LABEL AND LINE EDIT
        self.polyBorderColor_HLayout = QtWidgets.QHBoxLayout()
        self.polyBorderColor_HLayout.setObjectName("polyBorderColor_HLayout")
        self.edgeColourLabel = QtWidgets.QLabel(self.centralwidget)
        self.edgeColourLabel.setFont(fontLabel)
        self.edgeColourLabel.setObjectName("edgeColourLabel")
        self.polyBorderColor_HLayout.addWidget(self.edgeColourLabel)
        self.edgeColourLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.edgeColourLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.edgeColourLineEdit.setObjectName("edgeColourLineEdit")
        self.polyBorderColor_HLayout.addWidget(self.edgeColourLineEdit)
        self.edgeColourLineEdit.setText('black')
        self.edgeColourLineEdit.setFont(lineFont)

        self.gridLayout.addLayout(self.polyBorderColor_HLayout, 6, 1, 1, 1)

        # POLYGON BORDER LINE WIDTH LABEL AND LINE EDIT
        self.polyBorderLineWidth_HLayout = QtWidgets.QHBoxLayout()
        self.polyBorderLineWidth_HLayout.setObjectName("polyBorderLineWidth_HLayout")
        self.lineWdthLabel = QtWidgets.QLabel(self.centralwidget)
        self.lineWdthLabel.setFont(fontLabel)
        self.lineWdthLabel.setObjectName("lineWdthLabel")
        self.polyBorderLineWidth_HLayout.addWidget(self.lineWdthLabel)
        self.lineWdthLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineWdthLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineWdthLineEdit.setObjectName("lineWdthLineEdit")
        self.lineWdthLineEdit.setText('0.2')
        self.lineWdthLineEdit.setFont(lineFont)

        self.polyBorderLineWidth_HLayout.addWidget(self.lineWdthLineEdit)
        self.gridLayout.addLayout(self.polyBorderLineWidth_HLayout, 7, 1, 1, 1)

        # POLYGON FONT STYLE LABEL AND DROP MENU
        self.polyTextStyle_HLayout = QtWidgets.QHBoxLayout()
        self.polyTextStyle_HLayout.setObjectName("polyTextStyle_HLayout")
        self.fontWeightLabel = QtWidgets.QLabel(self.centralwidget)
        self.fontWeightLabel.setFont(fontLabel)
        self.fontWeightLabel.setObjectName("fontWeightLabel")
        self.polyTextStyle_HLayout.addWidget(self.fontWeightLabel)
        self.fontWeightComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.fontWeightComboBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.fontWeightComboBox.setObjectName("fontWeightComboBox")
        self.fontWeightComboBox.addItems(['Normal', 'Bold', 'Heavy', 'Light', 'Ultrabold', 'Ultralight'])
        self.polyTextStyle_HLayout.addWidget(self.fontWeightComboBox)
        self.fontWeightComboBox.setFont(lineFont)
        self.gridLayout.addLayout(self.polyTextStyle_HLayout, 8, 1, 1, 1)

        # POLYGON TEXT COLOR LABEL AND LINE EDIT
        self.polyTextColor_HLayout = QtWidgets.QHBoxLayout()
        self.polyTextColor_HLayout.setObjectName("polyTextColor_HLayout")
        self.textColorLabel = QtWidgets.QLabel(self.centralwidget)
        self.textColorLabel.setFont(fontLabel)
        self.textColorLabel.setObjectName("textColorLabel")
        self.polyTextColor_HLayout.addWidget(self.textColorLabel)
        self.textColorLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.textColorLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.textColorLineEdit.setObjectName("textColorLineEdit")
        self.textColorLineEdit.setText('black')
        self.textColorLineEdit.setFont(lineFont)

        self.polyTextColor_HLayout.addWidget(self.textColorLineEdit)
        self.gridLayout.addLayout(self.polyTextColor_HLayout, 9, 1, 1, 1)

        self.polyLabelFont_HLayout = QtWidgets.QHBoxLayout()
        self.polyLabelFont_HLayout.setObjectName(u"polyLabelFont_HLayout")
        self.polyLabelFont = QtWidgets.QLabel(self.centralwidget)
        self.polyLabelFont.setObjectName(u"polyLabelFont")
        self.polyLabelFont.setFont(fontLabel)

        self.polyLabelFont_HLayout.addWidget(self.polyLabelFont)

        self.polyLabelFontLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.polyLabelFontLineEdit.setObjectName(u"polyLabelFontLineEdit")
        self.polyLabelFontLineEdit.setFont(lineFont)
        self.polyLabelFontLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.polyLabelFontLineEdit.setText('4')
        self.polyLabelFont_HLayout.addWidget(self.polyLabelFontLineEdit)
        self.gridLayout.addLayout(self.polyLabelFont_HLayout, 10, 1, 1, 1)

        # POLYGON HALO EFFECT LINE WIDTH LABEL AND LINE EDIT
        self.polyHaloLineWidth_HLayout = QtWidgets.QHBoxLayout()
        self.polyHaloLineWidth_HLayout.setObjectName("polyHaloLineWidth_HLayout")
        self.haloLineWidthLabel = QtWidgets.QLabel(self.centralwidget)
        self.haloLineWidthLabel.setFont(fontLabel)
        self.haloLineWidthLabel.setObjectName("haloLineWidthLabel")
        self.polyHaloLineWidth_HLayout.addWidget(self.haloLineWidthLabel)
        self.haloLineWidthLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.haloLineWidthLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.haloLineWidthLineEdit.setObjectName("haloLineWidthLineEdit")
        self.haloLineWidthLineEdit.setText('0.4')
        self.haloLineWidthLineEdit.setFont(lineFont)
        self.polyHaloLineWidth_HLayout.addWidget(self.haloLineWidthLineEdit)
        self.gridLayout.addLayout(self.polyHaloLineWidth_HLayout, 11, 1, 1, 1)

        # POLYGON HALO EFFECT COLOR LABEL AND LINE EDIT
        self.polyHaloColor_HLayout = QtWidgets.QHBoxLayout()
        self.polyHaloColor_HLayout.setObjectName("polyHaloColor_HLayout")
        self.haloColorLabel = QtWidgets.QLabel(self.centralwidget)
        self.haloColorLabel.setFont(fontLabel)
        self.haloColorLabel.setObjectName("haloColorLabel")
        self.polyHaloColor_HLayout.addWidget(self.haloColorLabel)
        self.haloColorLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.haloColorLineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.haloColorLineEdit.setObjectName("haloColorLineEdit")
        self.haloColorLineEdit.setText('white')
        self.polyHaloColor_HLayout.addWidget(self.haloColorLineEdit)
        self.haloColorLineEdit.setFont(lineFont)

        self.gridLayout.addLayout(self.polyHaloColor_HLayout, 12, 1, 1, 1)

        # POLYGON COLOR MAPS LINK LABEL
        self.colorMapLinklabel = QtWidgets.QLabel(self.centralwidget)
        self.colorMapLinklabel.setFont(fontLabel)
        self.colorMapLinklabel.setMouseTracking(False)
        self.colorMapLinklabel.setOpenExternalLinks(True)
        self.colorMapLinklabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.colorMapLinklabel.setObjectName("colorMapLinklabel")
        self.gridLayout.addWidget(self.colorMapLinklabel, 16, 0, 1, 2)

        # COLOR LINK LABEL
        self.colorLinkLabel = QtWidgets.QLabel(self.centralwidget)
        self.colorLinkLabel.setFont(fontLabel)
        self.colorLinkLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.colorLinkLabel.setObjectName("colorLinkLabel")
        self.gridLayout.addWidget(self.colorLinkLabel, 17, 0, 1, 2)

        # CANCEL/OK BUTTONS
        self.save_cancel_HLayout = QtWidgets.QHBoxLayout()
        self.save_cancel_HLayout.setObjectName("save_cancel_HLayout")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.cancelButtonFunc(SettingsWindow))

        self.cancelButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cancelButton.setFont(lineFont)
        self.cancelButton.setObjectName("cancelButton")
        self.save_cancel_HLayout.addWidget(self.cancelButton)
        self.okButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.okButtonFunc(SettingsWindow))
        self.okButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.okButton.setFont(lineFont)
        self.okButton.setObjectName("okButton")
        self.save_cancel_HLayout.addWidget(self.okButton)
        self.gridLayout.addLayout(self.save_cancel_HLayout, 19, 0, 1, 2)

        self.axis_HLayout = QtWidgets.QHBoxLayout()
        self.axis_HLayout.setObjectName(u"axis_HLayout")
        self.axisLabel = QtWidgets.QLabel(self.centralwidget)
        self.axisLabel.setObjectName(u"axisLabel")
        self.axisLabel.setFont(fontLabel)

        self.axis_HLayout.addWidget(self.axisLabel)

        self.yes_no_HLayout = QtWidgets.QHBoxLayout()
        self.yes_no_HLayout.setObjectName(u"yes_no_HLayout")
        self.yesAxisRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.axisButtonGroup = QtWidgets.QButtonGroup(SettingsWindow)
        self.axisButtonGroup.setObjectName(u"axisButtonGroup")
        self.axisButtonGroup.addButton(self.yesAxisRadioButton)
        self.yesAxisRadioButton.setObjectName(u"yesAxisRadioButton")
        self.yesAxisRadioButton.setFont(lineFont)

        self.yes_no_HLayout.addWidget(self.yesAxisRadioButton)

        self.noAxisRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.axisButtonGroup.addButton(self.noAxisRadioButton)
        self.noAxisRadioButton.setObjectName(u"noAxisRadioButton")
        self.noAxisRadioButton.setFont(lineFont)
        self.noAxisRadioButton.setChecked(True)
        self.yes_no_HLayout.addWidget(self.noAxisRadioButton)

        self.axis_HLayout.addLayout(self.yes_no_HLayout)

        self.gridLayout.addLayout(self.axis_HLayout, 13, 1, 1, 1)

        self.separator_HLayout = QtWidgets.QHBoxLayout()
        self.separator_HLayout.setObjectName(u"separator_HLayout")
        self.separatorLabel = QtWidgets.QLabel(self.centralwidget)
        self.separatorLabel.setObjectName(u"separatorLabel")
        self.separatorLabel.setFont(fontLabel)
        self.separator_HLayout.addWidget(self.separatorLabel)

        self.separatorComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.separatorComboBox.setObjectName(u"separatorComboBox")

        self.separatorComboBox.setFont(lineFont)
        self.separator_HLayout.addWidget(self.separatorComboBox, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.separatorComboBox.addItems(self.separators)
        self.gridLayout.addLayout(self.separator_HLayout, 14, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Plot Options"))
        self.legendLabel.setText(_translate("SettingsWindow", "Legend (default: yes)"))
        self.legendTrue.setText(_translate("SettingsWindow", "Yes"))
        self.legendFalse.setText(_translate("SettingsWindow", "No"))
        self.titleLabel.setText(_translate("SettingsWindow", "Title (default: str; property name)"))
        self.titleFontSizeLabel.setText(_translate("SettingsWindow", "Title font size (default: float; 3)"))
        self.ncolLabel.setText(_translate("SettingsWindow", "Number of columns (default: int; 1)"))
        self.markerfirstLabel.setText(_translate("SettingsWindow", "Marker first"))
        self.markerfirstTrue.setText(_translate("SettingsWindow", "Yes"))
        self.markerfirstFalse.setText(_translate("SettingsWindow", "No"))
        self.title_fontsizeLabel.setText(_translate("SettingsWindow", "Font size (default: float; 2)"))
        self.haloLineWidthLabel.setText(_translate("SettingsWindow", "Halo effect line width (default: float; 0.4)"))
        self.labelcolorLabel.setText(_translate("SettingsWindow", "Color of the text (default: str; black)"))
        self.legendOptionsLabel.setText(_translate("SettingsWindow", "Legend options"))
        self.cmap10_20.setText(_translate("SettingsWindow", "Color Map if the elements>10;=<20 (default: str; tab20)"))
        self.legendOptionsLinkLabel.setText(_translate("SettingsWindow", "All legend options can be found here: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html"))
        self.fontWeightLabel.setText(_translate("SettingsWindow", "Text style (default: normal)"))
        self.haloColorLabel.setText(_translate("SettingsWindow", "Halo effect color (default: str; white)"))
        self.frameOnLabel.setText(_translate("SettingsWindow", "Frame"))
        self.frameOnTrue.setText(_translate("SettingsWindow", "Yes"))
        self.frameOnFalse.setText(_translate("SettingsWindow", "No"))
        self.colorMapLinklabel.setText(_translate("SettingsWindow", "All color maps can be found here: https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html"))
        self.cmap20.setText(_translate("SettingsWindow", "Color Map if the elements>20 (default: str; hsv)"))
        self.edgeColourLabel.setText(_translate("SettingsWindow", "Border color (default: str; black)"))
        self.locLabel.setText(_translate("SettingsWindow", "Location (default: str; best)"))
        self.fancyboxLabel.setText(_translate("SettingsWindow", "Fancy box"))
        self.fancyboxTrue.setText(_translate("SettingsWindow", "Yes"))
        self.fancyboxFalse.setText(_translate("SettingsWindow", "No"))
        self.polygonOptionslabel.setText(_translate("SettingsWindow", "Polygon Options"))
        self.lineWdthLabel.setText(_translate("SettingsWindow", "Border line width (default: float; 0.2)"))
        self.markerScaleLabel.setText(_translate("SettingsWindow", "Marker size (default: float; 0.2)"))
        self.colorLinkLabel.setText(_translate("SettingsWindow", "All colors can be found here: https://matplotlib.org/stable/gallery/color/named_colors.html"))
        self.facecolorLabel.setText(_translate("SettingsWindow", "Background color (default: str; inherit/white)"))
        self.textColorLabel.setText(_translate("SettingsWindow", "Text color (default: str; black)"))
        self.cancelButton.setText(_translate("SettingsWindow", "Cancel"))
        self.okButton.setText(_translate("SettingsWindow", "OK"))
        self.plotOptionsLabel.setText(_translate("SettingsWindow", "Plot Options"))
        self.cmap10Label.setText(_translate("SettingsWindow", "Color Map if the elements=<10 (default: str; tab10)"))
        self.axisLabel.setText(_translate("SettingsWindow", 'Axis'))
        self.separatorLabel.setText(_translate("SettingsWindow", 'Separator in case of saving multiple files.'))
        self.yesAxisRadioButton.setText(_translate("SettingsWindow", "Yes"))
        self.noAxisRadioButton.setText(_translate("SettingsWindow", "No"))
        self.polyLabelFont.setText(_translate("SettingsWindow", "Text font (default: float; 4)"))
        self.dpiLabel.setText(_translate("SettingsWindow", "Figure DPI (default: int; 1200)"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QMainWindow()
    ui = Ui_plotOptions()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())
