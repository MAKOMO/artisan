#!/usr/bin/env python3

# ABOUT
# Artisan Colors dialog

# LICENSE
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later versison. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# AUTHOR
# Marko Luther, 2020

import platform

from artisanlib.util import deltaLabelUTF8
from artisanlib.dialogs import ArtisanDialog

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
    QSizePolicy, QHBoxLayout, QVBoxLayout, QDialogButtonBox, QGridLayout, QGroupBox,
    QLayout, QSpinBox, QTabWidget, QMessageBox)

class graphColorDlg(ArtisanDialog):
    def __init__(self, parent = None, aw = None, activeTab = 0):
        super(graphColorDlg,self).__init__(parent, aw)
        self.setAttribute(Qt.WA_DeleteOnClose, False) # overwrite the ArtisanDialog class default here!!
        self.setModal(True)
        self.setWindowTitle(QApplication.translate("Form Caption","Colors", None))
        titlefont = QFont()
        titlefont.setBold(True)
        titlefont.setWeight(75)
        self.commonstyle = "border-style: solid; border-width: 1px; border-radius: 4px; border-color: black; padding: 4px;"
        
        #TAB0
        profilecolorlabel = QLabel(QApplication.translate("Label","Profile Colors",None))
        profilecolorlabel.setFont(titlefont)
        bgcolorlabel = QLabel(QApplication.translate("Label","Background Profile Colors",None))
        bgcolorlabel.setFont(titlefont)
        profilecolorlabel.setMaximumSize(180,20)
        bgcolorlabel.setMaximumSize(180,20)
        profilecolorlabel.setMinimumSize(150,20)
        bgcolorlabel.setMinimumSize(150,20)
        
        self.metLabel = QLabel(QApplication.translate("Button","ET", None))
        self.metLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.metButton = QPushButton()
        self.metButton.setFocusPolicy(Qt.NoFocus)
        self.metButton.clicked.connect(self.setColorSlot)
        self.btLabel = QLabel(QApplication.translate("Button","BT", None))
        self.btLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.btButton = QPushButton()
        self.btButton.setFocusPolicy(Qt.NoFocus)
        self.btButton.clicked.connect(self.setColorSlot)
        self.deltametLabel = QLabel(deltaLabelUTF8 + QApplication.translate("Button","ET", None))
        self.deltametLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.deltametButton = QPushButton()
        self.deltametButton.setFocusPolicy(Qt.NoFocus)
        self.deltametButton.clicked.connect(self.setColorSlot)
        self.deltabtLabel = QLabel(deltaLabelUTF8 + QApplication.translate("Button","BT", None))
        self.deltabtLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.deltabtButton = QPushButton()
        self.deltabtButton.setFocusPolicy(Qt.NoFocus)
        self.deltabtButton.clicked.connect(self.setColorSlot)

        self.bgmetLabel = QLabel(QApplication.translate("Button","ET", None))
        self.bgmetLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgmetButton = QPushButton()
        self.bgmetButton.setFocusPolicy(Qt.NoFocus)
        self.bgmetButton.clicked.connect(self.setbgColorSlot)
        self.bgbtLabel = QLabel(QApplication.translate("Button","BT", None))
        self.bgbtLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgbtButton = QPushButton()
        self.bgbtButton.setFocusPolicy(Qt.NoFocus)
        self.bgbtButton.clicked.connect(self.setbgColorSlot)
        self.bgdeltametLabel = QLabel(deltaLabelUTF8 + QApplication.translate("Button","ET", None))
        self.bgdeltametLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgdeltametButton = QPushButton()
        self.bgdeltametButton.setFocusPolicy(Qt.NoFocus)
        self.bgdeltametButton.clicked.connect(self.setbgColorSlot)
        self.bgdeltabtLabel = QLabel(deltaLabelUTF8 + QApplication.translate("Button","BT", None))
        self.bgdeltabtLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgdeltabtButton = QPushButton()
        self.bgdeltabtButton.setFocusPolicy(Qt.NoFocus)
        self.bgdeltabtButton.clicked.connect(self.setbgColorSlot)

        self.bgextraLabel = QLabel(QApplication.translate("Button","Extra 1", None))
        self.bgextraLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgextra2Label = QLabel(QApplication.translate("Button","Extra 2", None))
        self.bgextra2Label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgextraButton = QPushButton()
        self.bgextraButton.setFocusPolicy(Qt.NoFocus)
        self.bgextraButton.clicked.connect(self.setbgColorSlot)
        self.bgextra2Button = QPushButton()
        self.bgextra2Button.setFocusPolicy(Qt.NoFocus)
        self.bgextra2Button.clicked.connect(self.setbgColorSlot)
            
        opaqbgLabel = QLabel(QApplication.translate("Label", "Opaqueness",None))
        opaqbgLabel.setAlignment(Qt.AlignRight)
        self.opaqbgSpinBox = QSpinBox()
        self.opaqbgSpinBox.setAlignment(Qt.AlignRight)
        self.opaqbgSpinBox.setRange(1,10)
        self.opaqbgSpinBox.setSingleStep(1)
        self.opaqbgSpinBox.setValue(self.aw.qmc.backgroundalpha * 10)
        self.opaqbgSpinBox.valueChanged.connect(self.adjustintensity)
        self.opaqbgSpinBox.setFocusPolicy(Qt.NoFocus)
        self.opaqbgLayout = QHBoxLayout()
        self.opaqbgLayout.addWidget(opaqbgLabel)
        self.opaqbgLayout.addWidget(self.opaqbgSpinBox)
            
        #TAB1
        self.backgroundLabel = QLabel(QApplication.translate("Button","Background", None))
        self.backgroundLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.backgroundButton = QPushButton()
        self.backgroundButton = self.colorButton(self.aw.qmc.palette["background"])
        self.backgroundButton.setFocusPolicy(Qt.NoFocus)
        self.backgroundButton.clicked.connect(self.setColorSlot)
        self.gridLabel = QLabel(QApplication.translate("Button","Grid", None))
        self.gridLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.gridButton = QPushButton()
        self.gridButton = self.colorButton(self.aw.qmc.palette["grid"])
        self.gridButton.setFocusPolicy(Qt.NoFocus)
        self.gridButton.clicked.connect(self.setColorSlot)
        self.titleLabel = QLabel(QApplication.translate("Button","Title", None))
        self.titleLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.titleButton = QPushButton()
        self.titleButton = self.colorButton(self.aw.qmc.palette["title"])
        self.titleButton.setFocusPolicy(Qt.NoFocus)
        self.titleButton.clicked.connect(self.setColorSlot)
        self.yLabel = QLabel(QApplication.translate("Button","Y Label", None))
        self.yLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.yButton = QPushButton()
        self.yButton = self.colorButton(self.aw.qmc.palette["ylabel"])
        self.yButton.setFocusPolicy(Qt.NoFocus)
        self.yButton.clicked.connect(self.setColorSlot)
        self.xLabel = QLabel(QApplication.translate("Button","X Label", None))
        self.xLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.xButton = self.colorButton(self.aw.qmc.palette["xlabel"])
        self.xButton.setFocusPolicy(Qt.NoFocus)
        self.xButton.clicked.connect(self.setColorSlot)
        self.rect1Label = QLabel(QApplication.translate("Button","Drying Phase", None))
        self.rect1Label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.rect1Button = QPushButton()
        self.rect1Button = self.colorButton(self.aw.qmc.palette["rect1"])
        self.rect1Button.setFocusPolicy(Qt.NoFocus)
        self.rect1Button.clicked.connect(self.setColorSlot)
        self.rect2Label = QLabel(QApplication.translate("Button","Maillard Phase", None))
        self.rect2Label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.rect2Button = QPushButton()
        self.rect2Button = self.colorButton(self.aw.qmc.palette["rect2"])
        self.rect2Button.setFocusPolicy(Qt.NoFocus)
        self.rect2Button.clicked.connect(self.setColorSlot)
        self.rect3Label = QLabel(QApplication.translate("Button","Finishing Phase", None))
        self.rect3Label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.rect3Button = QPushButton()
        self.rect3Button = self.colorButton(self.aw.qmc.palette["rect3"])
        self.rect3Button.setFocusPolicy(Qt.NoFocus)
        self.rect3Button.clicked.connect(self.setColorSlot)
        self.rect4Label = QLabel(QApplication.translate("Button","Cooling Phase", None))
        self.rect4Label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.rect4Button = QPushButton()
        self.rect4Button = self.colorButton(self.aw.qmc.palette["rect4"])
        self.rect4Button.setFocusPolicy(Qt.NoFocus)
        self.rect4Button.clicked.connect(self.setColorSlot)
        self.rect5Label = QLabel(QApplication.translate("Button","Bars Bkgnd", None))
        self.rect5Label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.rect5Button = QPushButton()
        self.rect5Button = self.colorButton(self.aw.qmc.palette["rect5"])
        self.rect5Button.setFocusPolicy(Qt.NoFocus)
        self.rect5Button.clicked.connect(self.setColorSlot)
        self.markersLabel = QLabel(QApplication.translate("Button","Markers", None))
        self.markersLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.markersButton = QPushButton()
        self.markersButton = self.colorButton(self.aw.qmc.palette["markers"])
        self.markersButton.setFocusPolicy(Qt.NoFocus)
        self.markersButton.clicked.connect(self.setColorSlot)
        self.textLabel = QLabel(QApplication.translate("Button","Text", None))
        self.textLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.textButton = QPushButton()
        self.textButton = self.colorButton(self.aw.qmc.palette["text"])
        self.textButton.setFocusPolicy(Qt.NoFocus)
        self.textButton.clicked.connect(self.setColorSlot)
        self.watermarksLabel = QLabel(QApplication.translate("Button","Watermarks", None))
        self.watermarksLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.watermarksButton = QPushButton()
        self.watermarksButton = self.colorButton(self.aw.qmc.palette["watermarks"])
        self.watermarksButton.setFocusPolicy(Qt.NoFocus)
        self.watermarksButton.clicked.connect(self.setColorSlot)
        self.timeguideLabel = QLabel(QApplication.translate("Button","Time Guide", None))
        self.timeguideLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.timeguideButton = QPushButton()
        self.timeguideButton = self.colorButton(self.aw.qmc.palette["timeguide"])
        self.timeguideButton.setFocusPolicy(Qt.NoFocus)
        self.timeguideButton.clicked.connect(self.setColorSlot)
        self.aucguideLabel = QLabel(QApplication.translate("Button","AUC Guide", None))
        self.aucguideLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.aucguideButton = QPushButton()
        self.aucguideButton = self.colorButton(self.aw.qmc.palette["aucguide"])
        self.aucguideButton.setFocusPolicy(Qt.NoFocus)
        self.aucguideButton.clicked.connect(self.setColorSlot)
        self.aucareaLabel = QLabel(QApplication.translate("Button","AUC Area", None))
        self.aucareaLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.aucareaButton = QPushButton()
        self.aucareaButton = self.colorButton(self.aw.qmc.palette["aucarea"])
        self.aucareaButton.setFocusPolicy(Qt.NoFocus)
        self.aucareaButton.clicked.connect(self.setColorSlot)
        self.legendbgLabel = QLabel(QApplication.translate("Button","Legend bkgnd", None))
        self.legendbgLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.legendbgButton = QPushButton()
        self.legendbgButton = self.colorButton(self.aw.qmc.palette["legendbg"])
        self.legendbgButton.setFocusPolicy(Qt.NoFocus)
        self.legendbgButton.clicked.connect(self.setColorSlot)
        self.legendbgSpinBox = QSpinBox()
        self.legendbgSpinBox.setAlignment(Qt.AlignRight)
        self.legendbgSpinBox.setRange(1,10)
        self.legendbgSpinBox.setSingleStep(1)
        self.legendbgSpinBox.setValue(self.aw.qmc.alpha["legendbg"] * 10)
        self.legendbgSpinBox.valueChanged.connect(self.adjustOpaqenesssSlot)
        self.legendbgSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.legendbgButton.setSizePolicy(QSizePolicy.Expanding,self.legendbgButton.sizePolicy().verticalPolicy())
        self.legendbgLayout = QHBoxLayout()
        self.legendbgLayout.addWidget(self.legendbgButton)
        self.legendbgLayout.addWidget(self.legendbgSpinBox)
        self.legendborderLabel = QLabel(QApplication.translate("Button","Legend border", None))
        self.legendborderLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.legendborderButton = QPushButton()
        self.legendborderButton = self.colorButton(self.aw.qmc.palette["legendborder"])
        self.legendborderButton.setFocusPolicy(Qt.StrongFocus)
        self.legendborderButton.clicked.connect(self.setColorSlot)

        self.canvasLabel = QLabel(QApplication.translate("Button","Canvas", None))
        self.canvasLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.canvasButton = QPushButton()
        self.canvasButton = self.colorButton(self.aw.qmc.palette["canvas"])
        if str(self.aw.qmc.palette["canvas"]) == 'None':
            self.canvasButton.setPalette(QPalette(QColor("#f0f0f0")))
        else:
            self.canvasButton.setPalette(QPalette(QColor(self.aw.qmc.palette["canvas"])))
        self.canvasButton.setFocusPolicy(Qt.NoFocus)
        self.canvasButton.clicked.connect(self.setColorSlot)

        self.specialeventboxLabel = QLabel(QApplication.translate("Button","SpecialEvent Marker", None))
        self.specialeventboxLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.specialeventboxButton = QPushButton()
        self.specialeventboxButton = self.colorButton(self.aw.qmc.palette["specialeventbox"])
        self.specialeventboxButton.setFocusPolicy(Qt.NoFocus)
        self.specialeventboxButton.clicked.connect(self.setColorSlot)
        self.specialeventtextLabel = QLabel(QApplication.translate("Button","SpecialEvent Text", None))
        self.specialeventtextLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.specialeventtextButton = QPushButton()
        self.specialeventtextButton = self.colorButton(self.aw.qmc.palette["specialeventtext"])
        self.specialeventtextButton.setFocusPolicy(Qt.NoFocus)
        self.specialeventtextButton.clicked.connect(self.setColorSlot)
        self.bgeventmarkerLabel = QLabel(QApplication.translate("Button","Bkgd Event Marker", None))
        self.bgeventmarkerLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgeventmarkerButton = QPushButton()
        self.bgeventmarkerButton = self.colorButton(self.aw.qmc.palette["bgeventmarker"])
        self.bgeventmarkerButton.setFocusPolicy(Qt.NoFocus)
        self.bgeventmarkerButton.clicked.connect(self.setColorSlot)
        self.bgeventtextLabel = QLabel(QApplication.translate("Button","Bkgd Event Text", None))
        self.bgeventtextLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bgeventtextButton = QPushButton()
        self.bgeventtextButton = self.colorButton(self.aw.qmc.palette["bgeventtext"])
        self.bgeventtextButton.setFocusPolicy(Qt.NoFocus)
        self.bgeventtextButton.clicked.connect(self.setColorSlot)
        self.mettextLabel = QLabel(QApplication.translate("Button","MET Text", None))
        self.mettextLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.mettextButton = QPushButton()
        self.mettextButton = self.colorButton(self.aw.qmc.palette["mettext"])
        self.mettextButton.setFocusPolicy(Qt.NoFocus)
        self.mettextButton.clicked.connect(self.setColorSlot)
        self.metboxLabel = QLabel(QApplication.translate("Button","MET Box", None))
        self.metboxLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.metboxButton = QPushButton()
        self.metboxButton = self.colorButton(self.aw.qmc.palette["metbox"])
        self.metboxButton.setFocusPolicy(Qt.NoFocus)
        self.metboxButton.clicked.connect(self.setColorSlot)
        self.analysismaskLabel = QLabel(QApplication.translate("Button","Analysis Mask", None))
        self.analysismaskLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.analysismaskButton = QPushButton()
        self.analysismaskButton = self.colorButton(self.aw.qmc.palette["analysismask"])
        self.analysismaskButton.setFocusPolicy(Qt.StrongFocus)
        self.analysismaskButton.clicked.connect(self.setColorSlot)
        self.analysismaskSpinBox = QSpinBox()
        self.analysismaskSpinBox.setAlignment(Qt.AlignRight)
        self.analysismaskSpinBox.setRange(1,10)
        self.analysismaskSpinBox.setSingleStep(1)
        self.analysismaskSpinBox.setValue(self.aw.qmc.alpha["analysismask"] * 10)
        self.analysismaskSpinBox.valueChanged.connect(self.adjustOpaqenesssSlot)
        self.analysismaskLayout = QHBoxLayout()
        self.analysismaskButton.setSizePolicy(QSizePolicy.Expanding,self.analysismaskButton.sizePolicy().verticalPolicy())
        self.analysismaskLayout.addWidget(self.analysismaskButton)
        self.analysismaskLayout.addWidget(self.analysismaskSpinBox)
        self.statsanalysisbkgndLabel = QLabel(QApplication.translate("Button","Stats&Analysis Bkgnd", None))
        self.statsanalysisbkgndLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.statsanalysisbkgndButton = QPushButton()
        self.statsanalysisbkgndButton = self.colorButton(self.aw.qmc.palette["statsanalysisbkgnd"])
        self.statsanalysisbkgndButton.setFocusPolicy(Qt.StrongFocus)
        self.statsanalysisbkgndButton.clicked.connect(self.setColorSlot)
        self.statsanalysisbkgndSpinBox = QSpinBox()
        self.statsanalysisbkgndSpinBox.setAlignment(Qt.AlignRight)
        self.statsanalysisbkgndSpinBox.setRange(1,10)
        self.statsanalysisbkgndSpinBox.setSingleStep(1)
        self.statsanalysisbkgndSpinBox.setValue(self.aw.qmc.alpha["statsanalysisbkgnd"] * 10)
        self.statsanalysisbkgndSpinBox.valueChanged.connect(self.adjustOpaqenesssSlot)
        self.statsanalysisbkgndSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.statsanalysisbkgndLayout = QHBoxLayout()
        self.statsanalysisbkgndButton.setSizePolicy(QSizePolicy.Expanding,self.statsanalysisbkgndButton.sizePolicy().verticalPolicy())
        self.statsanalysisbkgndLayout.addWidget(self.statsanalysisbkgndButton)
        self.statsanalysisbkgndLayout.addWidget(self.statsanalysisbkgndSpinBox)

        #TAB2
        self.lcd1LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd1LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd2LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd2LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd3LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd3LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd4LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd4LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd5LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd5LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd6LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd6LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd7LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd7LEDButton.clicked.connect(self.paintlcdsSlot)
        self.lcd8LEDButton = QPushButton(QApplication.translate("Button","Digits",None))
        self.lcd8LEDButton.clicked.connect(self.paintlcdsSlot)
        
        self.lcd1backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd1backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd2backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd2backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd3backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd3backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd4backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd4backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd5backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd5backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd6backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd6backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd7backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd7backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd8backButton = QPushButton(QApplication.translate("Button","Background",None))
        self.lcd8backButton.clicked.connect(self.paintlcdsSlot)
        self.lcd1LEDButton.setMinimumWidth(80)
        self.lcd2LEDButton.setMinimumWidth(80)
        self.lcd3LEDButton.setMinimumWidth(80)
        self.lcd4LEDButton.setMinimumWidth(80)
        self.lcd5LEDButton.setMinimumWidth(80)
        self.lcd6LEDButton.setMinimumWidth(80)
        self.lcd7LEDButton.setMinimumWidth(80)
        self.lcd8LEDButton.setMinimumWidth(80)

        LCDdefaultButton = QPushButton(QApplication.translate("Button","B/W",None))
        LCDdefaultButton.clicked.connect(self.setLCD_bw)
            
        #LAYOUTS
        #tab0 layout
        lines = QGridLayout()
        lines.setAlignment(Qt.AlignCenter)
        lines.setVerticalSpacing(1)
        lines.setColumnMinimumWidth(0,0)   #0,80
#        lines.setColumnMaximumWidth(0,30)
        lines.setColumnMinimumWidth(1,150)   #1,180
        lines.setColumnMinimumWidth(2,50)   #2,80
        lines.setColumnMinimumWidth(3,150)   #3,180

        lines.addWidget(profilecolorlabel,0,1)
        lines.addWidget(self.metButton,1,1)
        lines.addWidget(self.metLabel,1,0)
        lines.addWidget(self.btButton,2,1)
        lines.addWidget(self.btLabel,2,0)
        lines.addWidget(self.deltametButton,3,1)
        lines.addWidget(self.deltametLabel,3,0)
        lines.addWidget(self.deltabtButton,4,1)
        lines.addWidget(self.deltabtLabel,4,0)

        lines.addWidget(bgcolorlabel,0,3)
        lines.addWidget(self.bgmetButton,1,3)
        lines.addWidget(self.bgmetLabel,1,2)
        lines.addWidget(self.bgbtButton,2,3)
        lines.addWidget(self.bgbtLabel,2,2)
        lines.addWidget(self.bgdeltametButton,3,3)
        lines.addWidget(self.bgdeltametLabel,3,2)
        lines.addWidget(self.bgdeltabtButton,4,3)
        lines.addWidget(self.bgdeltabtLabel,4,2)
        lines.addWidget(self.bgextraButton,5,3)
        lines.addWidget(self.bgextraLabel,5,2)
        lines.addWidget(self.bgextra2Button,6,3)
        lines.addWidget(self.bgextra2Label,6,2)
        lines.addLayout(self.opaqbgLayout,7,3)

        graphlinesLayout = QVBoxLayout()
        graphlinesLayout.addLayout(lines)
        
        #tab1 layout
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignCenter)
#        grid.setColumnStretch(1,12)
#        grid.setColumnStretch(3,12)
        grid.setVerticalSpacing(1)
        grid.setColumnMinimumWidth(0,80)
        grid.setColumnMinimumWidth(2,80)
        grid.setColumnMinimumWidth(1,110)  #1,80
        grid.setColumnMinimumWidth(3,110)  #3,80
        grid.addWidget(self.canvasButton,0,1)
        grid.addWidget(self.canvasLabel,0,0)
        grid.addWidget(self.backgroundButton,1,1)
        grid.addWidget(self.backgroundLabel,1,0)
        grid.addWidget(self.titleButton,2,1)
        grid.addWidget(self.titleLabel,2,0)
        grid.addWidget(self.gridButton,3,1)
        grid.addWidget(self.gridLabel,3,0)
        grid.addWidget(self.yButton,4,1)
        grid.addWidget(self.yLabel,4,0)
        grid.addWidget(self.xButton,5,1)
        grid.addWidget(self.xLabel,5,0)
        grid.addWidget(self.markersButton,6,1)
        grid.addWidget(self.markersLabel,6,0)
        grid.addWidget(self.textButton,7,1)
        grid.addWidget(self.textLabel,7,0)
        grid.addLayout(self.legendbgLayout,8,1) 
        grid.addWidget(self.legendbgLabel,8,0) 
        grid.addWidget(self.legendborderButton,9,1)
        grid.addWidget(self.legendborderLabel,9,0) 
        grid.addWidget(self.watermarksButton,10,1)
        grid.addWidget(self.watermarksLabel,10,0)
        grid.addWidget(self.aucguideButton,11,1)
        grid.addWidget(self.aucguideLabel,11,0)
        grid.addWidget(self.aucareaButton,12,1)
        grid.addWidget(self.aucareaLabel,12,0)
        grid.addWidget(self.rect1Button,0,3)
        grid.addWidget(self.rect1Label,0,2)
        grid.addWidget(self.rect2Button,1,3)
        grid.addWidget(self.rect2Label,1,2)
        grid.addWidget(self.rect3Button,2,3)
        grid.addWidget(self.rect3Label,2,2)
        grid.addWidget(self.rect4Button,3,3)
        grid.addWidget(self.rect4Label,3,2)
        grid.addWidget(self.rect5Button,4,3)
        grid.addWidget(self.rect5Label,4,2)
        grid.addWidget(self.specialeventboxButton,5,3) 
        grid.addWidget(self.specialeventboxLabel,5,2) 
        grid.addWidget(self.specialeventtextButton,6,3) 
        grid.addWidget(self.specialeventtextLabel,6,2) 
        grid.addWidget(self.bgeventmarkerButton,7,3) 
        grid.addWidget(self.bgeventmarkerLabel,7,2) 
        grid.addWidget(self.bgeventtextButton,8,3) 
        grid.addWidget(self.bgeventtextLabel,8,2) 
        grid.addWidget(self.metboxButton,9,3) 
        grid.addWidget(self.metboxLabel,9,2) 
        grid.addWidget(self.mettextButton,10,3) 
        grid.addWidget(self.mettextLabel,10,2) 
        grid.addWidget(self.timeguideButton,11,3)
        grid.addWidget(self.timeguideLabel,11,2)
        grid.addLayout(self.analysismaskLayout,12,3)
        grid.addWidget(self.analysismaskLabel,12,2)
        grid.addLayout(self.statsanalysisbkgndLayout,13,3)
        grid.addWidget(self.statsanalysisbkgndLabel,13,2)
        graphLayout = QVBoxLayout()
        graphLayout.addLayout(grid)

        #tab 2 layout
        lcd1layout = QHBoxLayout()
        lcd1layout.addWidget(self.lcd1LEDButton,0)
        lcd1layout.addWidget(self.lcd1backButton,1)
        lcd2layout = QHBoxLayout()
        lcd2layout.addWidget(self.lcd2LEDButton,0)
        lcd2layout.addWidget(self.lcd2backButton,1)
        lcd3layout = QHBoxLayout()
        lcd3layout.addWidget(self.lcd3LEDButton,0)
        lcd3layout.addWidget(self.lcd3backButton,1)
        lcd4layout = QHBoxLayout()
        lcd4layout.addWidget(self.lcd4LEDButton,0)
        lcd4layout.addWidget(self.lcd4backButton,1)
        lcd5layout = QHBoxLayout()
        lcd5layout.addWidget(self.lcd5LEDButton,0)
        lcd5layout.addWidget(self.lcd5backButton,1)
        lcd6layout = QHBoxLayout()
        lcd6layout.addWidget(self.lcd6LEDButton,0)
        lcd6layout.addWidget(self.lcd6backButton,1)
        lcd7layout = QHBoxLayout()
        lcd7layout.addWidget(self.lcd7LEDButton,0)
        lcd7layout.addWidget(self.lcd7backButton,1)
        lcd8layout = QHBoxLayout()
        lcd8layout.addWidget(self.lcd8LEDButton,0)
        lcd8layout.addWidget(self.lcd8backButton,1)
        LCD1GroupLayout = QGroupBox(QApplication.translate("GroupBox","Timer LCD",None))
        LCD1GroupLayout.setLayout(lcd1layout)
        lcd1layout.setContentsMargins(0,0,0,0)
        LCD2GroupLayout = QGroupBox(QApplication.translate("GroupBox","ET LCD",None))
        LCD2GroupLayout.setLayout(lcd2layout)
        lcd2layout.setContentsMargins(0,0,0,0)
        LCD3GroupLayout = QGroupBox(QApplication.translate("GroupBox","BT LCD",None))
        LCD3GroupLayout.setLayout(lcd3layout)
        lcd3layout.setContentsMargins(0,0,0,0)
        LCD4GroupLayout = QGroupBox(deltaLabelUTF8 + QApplication.translate("GroupBox","ET LCD",None))
        LCD4GroupLayout.setLayout(lcd4layout)
        lcd4layout.setContentsMargins(0,0,0,0)
        LCD5GroupLayout = QGroupBox(deltaLabelUTF8 + QApplication.translate("GroupBox","BT LCD",None))
        LCD5GroupLayout.setLayout(lcd5layout)
        lcd5layout.setContentsMargins(0,0,0,0)
        LCD6GroupLayout = QGroupBox(QApplication.translate("GroupBox","Extra Devices / PID SV LCD",None))
        LCD6GroupLayout.setLayout(lcd6layout)
        lcd6layout.setContentsMargins(0,0,0,0)
        LCD7GroupLayout = QGroupBox(QApplication.translate("GroupBox","Ramp/Soak Timer LCD",None))
        LCD7GroupLayout.setLayout(lcd7layout)
        lcd7layout.setContentsMargins(0,0,0,0)
        LCD8GroupLayout = QGroupBox(QApplication.translate("GroupBox","Slow Cooling Timer LCD",None))
        LCD8GroupLayout.setLayout(lcd8layout)
        lcd8layout.setContentsMargins(0,0,0,0)

        buttonlayout = QHBoxLayout()
        buttonlayout.addStretch()
        buttonlayout.addWidget(LCDdefaultButton)
        buttonlayout.setContentsMargins(0,0,0,0)
        buttonlayout.setSpacing(0)
        
        lcdlayout1 = QVBoxLayout()
        lcdlayout1.addWidget(LCD2GroupLayout)
        lcdlayout1.addWidget(LCD3GroupLayout)
        lcdlayout1.addWidget(LCD1GroupLayout)
        lcdlayout1.addWidget(LCD6GroupLayout)
        lcdlayout2 = QVBoxLayout()
        lcdlayout2.addWidget(LCD4GroupLayout)
        lcdlayout2.addWidget(LCD5GroupLayout)
        lcdlayout2.addWidget(LCD7GroupLayout)
        lcdlayout2.addWidget(LCD8GroupLayout)
        lcdlayout = QHBoxLayout()
        lcdlayout.addLayout(lcdlayout1)
        lcdlayout.addLayout(lcdlayout2)
        lllayout = QVBoxLayout()
        lllayout.addLayout(lcdlayout)
        lllayout.addLayout(buttonlayout)
        lllayout.setContentsMargins(0,0,0,0)
        lllayout.setSpacing(5)

        ###################################
        self.TabWidget = QTabWidget()
        C0Widget = QWidget()
        C0Widget.setLayout(graphlinesLayout)
        self.TabWidget.addTab(C0Widget,QApplication.translate("Tab","Curves",None))
        C1Widget = QWidget()
        C1Widget.setLayout(graphLayout)
        self.TabWidget.addTab(C1Widget,QApplication.translate("Tab","Graph",None))
        C2Widget = QWidget()
        C2Widget.setLayout(lllayout)
        self.TabWidget.addTab(C2Widget,QApplication.translate("Tab","LCDs",None))

        # connect the ArtisanDialog standard OK/Cancel buttons
        self.dialogbuttons.accepted.connect(self.accept)
        self.dialogbuttons.removeButton(self.dialogbuttons.button(QDialogButtonBox.Cancel))
        self.dialogbuttons.addButton(QDialogButtonBox.RestoreDefaults)
        self.dialogbuttons.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.recolor1)
        self.setButtonTranslations(self.dialogbuttons.button(QDialogButtonBox.RestoreDefaults),"Restore Defaults",QApplication.translate("Button","Restore Defaults", None))
        
        greyButton = QPushButton(QApplication.translate("Button","Grey", None))
        greyButton.setFocusPolicy(Qt.NoFocus)
        greyButton.clicked.connect(self.recolor2)
        
        self.dialogbuttons.addButton(greyButton, QDialogButtonBox.ActionRole)

        okLayout = QHBoxLayout()
        okLayout.addStretch()
        okLayout.addWidget(self.dialogbuttons)
        okLayout.setContentsMargins(10, 10, 10, 10)
        self.TabWidget.setContentsMargins(0, 0, 0, 0)
        C0Widget.setContentsMargins(5, 10, 5, 10)
        C1Widget.setContentsMargins(5, 10, 5, 10)
        C2Widget.setContentsMargins(5, 10, 5, 10)
        graphLayout.setContentsMargins(5,0,5,0)
        #incorporate layouts
        Mlayout = QVBoxLayout()
        Mlayout.addWidget(self.TabWidget)
        Mlayout.addLayout(okLayout)
        Mlayout.setContentsMargins(5,10,5,0)
        Mlayout.setSpacing(0)
        self.setLayout(Mlayout)
        self.setColorButtons()
        if platform.system() == 'Windows':
            self.dialogbuttons.button(QDialogButtonBox.Ok)
        else:
            self.dialogbuttons.button(QDialogButtonBox.Ok).setFocus()
        self.layout().setSizeConstraint(QLayout.SetFixedSize) # don't allow resizing
        self.TabWidget.setCurrentIndex(activeTab)

    @pyqtSlot(bool)
    def setLCD_bw(self,_):
        self.aw.setLCDsBW()
        self.setColorButtons()
        
    def setLED(self,hue,lcd):
        if lcd == 1:
            color = QColor(self.aw.lcdpaletteF["timer"])
            color.setHsv(hue,255,255,255)
            self.aw.lcdpaletteF["timer"] = str(color.name())
            self.aw.lcd1.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["timer"],self.aw.lcdpaletteB["timer"]))
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        elif lcd == 2:
            color = QColor(self.aw.lcdpaletteF["et"])
            color.setHsv(hue,255,255,255)
            self.aw.lcdpaletteF["et"] = str(color.name())
            self.aw.lcd2.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["et"],self.aw.lcdpaletteB["et"]))
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        elif lcd == 3:
            color = QColor(self.aw.lcdpaletteF["bt"])
            color.setHsv(hue,255,255,255)
            self.aw.lcdpaletteF["bt"] = str(color.name())
            self.aw.lcd3.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["bt"],self.aw.lcdpaletteB["bt"]))
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        elif lcd == 4:
            color = QColor(self.aw.lcdpaletteF["deltaet"])
            color.setHsv(hue,255,255,255)
            self.aw.lcdpaletteF["deltaet"] = str(color.name())
            self.aw.lcd4.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["deltaet"],self.aw.lcdpaletteB["deltaet"]))
            if self.aw.largeDeltaLCDs_dialog:
                self.aw.largeDeltaLCDs_dialog.updateStyles()
        elif lcd == 5:
            color = QColor(self.aw.lcdpaletteF["deltabt"])
            color.setHsv(hue,255,255,255)
            self.aw.lcdpaletteF["deltabt"] = str(color.name())
            self.aw.lcd5.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["deltabt"],self.aw.lcdpaletteB["deltabt"]))
            if self.aw.largeDeltaLCDs_dialog:
                self.aw.largeDeltaLCDs_dialog.updateStyles()
        elif lcd == 6:
            color = QColor(self.aw.lcdpaletteF["sv"])
            color.setHsv(hue,255,255,255)
            self.aw.lcdpaletteF["sv"] = str(color.name())
            self.aw.lcd6.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
            self.aw.lcd7.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
            for i in range(len(self.aw.qmc.extradevices)):
                self.aw.extraLCD1[i].setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
                self.aw.extraLCD2[i].setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
            if self.aw.largePIDLCDs_dialog:
                self.aw.largePIDLCDs_dialog.updateStyles()
            if self.aw.largeExtraLCDs_dialog:
                self.aw.largeExtraLCDs_dialog.updateStyles()
            if self.aw.largePhasesLCDs_dialog:
                self.aw.largePhasesLCDs_dialog.updateStyles()

    @pyqtSlot(bool)
    def paintlcdsSlot(self,_):
        lcdButton = self.sender()
        if lcdButton in [self.lcd1LEDButton,self.lcd1backButton]:
            if lcdButton == self.lcd1backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"timer")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"timer")
            self.aw.lcd1.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["timer"],self.aw.lcdpaletteB["timer"]))
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd2LEDButton,self.lcd2backButton]:
            if lcdButton == self.lcd2backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"et")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"et")
            self.aw.lcd2.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["et"],self.aw.lcdpaletteB["et"]))
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd3LEDButton,self.lcd3backButton]:
            if lcdButton == self.lcd3backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"bt")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"bt")
            self.aw.lcd3.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["bt"],self.aw.lcdpaletteB["bt"]))
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd4LEDButton,self.lcd4backButton]:
            if lcdButton == self.lcd4backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"deltaet")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"deltaet")
            self.aw.lcd4.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["deltaet"],self.aw.lcdpaletteB["deltaet"]))
            if self.aw.largeDeltaLCDs_dialog:
                self.aw.largeDeltaLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd5LEDButton,self.lcd5backButton]:
            if lcdButton == self.lcd5backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"deltabt")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"deltabt")
            self.aw.lcd5.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["deltabt"],self.aw.lcdpaletteB["deltabt"]))
            if self.aw.largeDeltaLCDs_dialog:
                self.aw.largeDeltaLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd6LEDButton,self.lcd6backButton]:
            if lcdButton == self.lcd6backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"sv")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"sv")
            self.aw.lcd6.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
            self.aw.lcd7.setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
            for i in range(len(self.aw.qmc.extradevices)):
                self.aw.extraLCD1[i].setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
                self.aw.extraLCD2[i].setStyleSheet("QLCDNumber { border-radius: 4; color: %s; background-color: %s;}"%(self.aw.lcdpaletteF["sv"],self.aw.lcdpaletteB["sv"]))
            if self.aw.largePIDLCDs_dialog:
                self.aw.largePIDLCDs_dialog.updateStyles()
            if self.aw.largeExtraLCDs_dialog:
                self.aw.largeExtraLCDs_dialog.updateStyles()
            if self.aw.largePhasesLCDs_dialog:
                self.aw.largePhasesLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd7LEDButton,self.lcd7backButton]:
            if lcdButton == self.lcd7backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"rstimer")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"rstimer")
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        if lcdButton in [self.lcd8LEDButton,self.lcd8backButton]:
            if lcdButton == self.lcd8backButton:
                self.setlcdColor(self.aw.lcdpaletteB,self.aw.lcdpaletteF,"slowcoolingtimer")
            else:
                self.setlcdColor(self.aw.lcdpaletteF,self.aw.lcdpaletteB,"slowcoolingtimer")
            if self.aw.largeLCDs_dialog:
                self.aw.largeLCDs_dialog.updateStyles()
        self.setColorButtons()

    def setColorButtons(self):
        for l,t in [
                # Curves (background curves handled separately)
                (self.metButton,"et"),
                (self.btButton,"bt"),
                (self.deltametButton,"deltaet"),
                (self.deltabtButton,"deltabt"),
                # Graph
                (self.canvasButton,"canvas"),
                (self.backgroundButton,"background"),
                (self.titleButton,"title"),
                (self.gridButton,"grid"),
                (self.yButton,"ylabel"),
                (self.xButton,"xlabel"),
                (self.timeguideButton,"timeguide"),
                (self.aucguideButton,"aucguide"),
                (self.aucareaButton,"aucarea"),
                (self.watermarksButton,"watermarks"),
                (self.rect1Button,"rect1"),
                (self.rect2Button,"rect2"),
                (self.rect3Button,"rect3"),
                (self.rect4Button,"rect4"),
                (self.rect5Button,"rect5"),
                (self.markersButton,"markers"),
                (self.textButton,"text"),
                (self.legendbgButton,"legendbg"),
                (self.legendborderButton,"legendborder"),
                (self.specialeventboxButton,"specialeventbox"),
                (self.specialeventtextButton,"specialeventtext"),
                (self.bgeventmarkerButton,"bgeventmarker"),
                (self.bgeventtextButton,"bgeventtext"),
                (self.mettextButton,"mettext"),
                (self.metboxButton,"metbox"),
                (self.analysismaskButton,"analysismask"),
                (self.statsanalysisbkgndButton,"statsanalysisbkgnd"),
                ]:
            self.setColorButton(l,t)
            
        # Curves, set background colors and alpha
        self.bgmetButton.setText(self.aw.qmc.backgroundmetcolor)
        self.bgbtButton.setText(self.aw.qmc.backgroundbtcolor)
        self.bgdeltametButton.setText(self.aw.qmc.backgrounddeltaetcolor)
        self.bgdeltabtButton.setText(self.aw.qmc.backgrounddeltabtcolor)
        self.bgextraButton.setText(self.aw.qmc.backgroundxtcolor)
        self.bgextra2Button.setText(self.aw.qmc.backgroundytcolor)
        self.bgmetButton.setStyleSheet("QPushButton { background-color: " + self.aw.qmc.backgroundmetcolor + "; color: " + self.aw.labelBorW(self.aw.qmc.backgroundmetcolor) + ";" + self.commonstyle + "}")
        self.bgbtButton.setStyleSheet("QPushButton { background-color: " + self.aw.qmc.backgroundbtcolor + "; color: " + self.aw.labelBorW(self.aw.qmc.backgroundbtcolor) + ";" + self.commonstyle + "}")
        self.bgdeltametButton.setStyleSheet("QPushButton { background-color: " + self.aw.qmc.backgrounddeltaetcolor + "; color: " + self.aw.labelBorW(self.aw.qmc.backgrounddeltaetcolor) + ";" + self.commonstyle + "}")
        self.bgdeltabtButton.setStyleSheet("QPushButton { background-color: " + self.aw.qmc.backgrounddeltabtcolor + "; color: " + self.aw.labelBorW(self.aw.qmc.backgrounddeltabtcolor) + ";" + self.commonstyle + "}")
        self.bgextraButton.setStyleSheet("QPushButton { background-color: " + self.aw.qmc.backgroundxtcolor + "; color: " + self.aw.labelBorW(self.aw.qmc.backgroundxtcolor) + ";" + self.commonstyle + "}")
        self.bgextra2Button.setStyleSheet("QPushButton { background-color: " + self.aw.qmc.backgroundytcolor + "; color: " + self.aw.labelBorW(self.aw.qmc.backgroundytcolor) + ";" + self.commonstyle + "}")
        self.opaqbgSpinBox.setValue(self.aw.qmc.backgroundalpha * 10)

        # LEDs
        self.lcd1backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['timer'] + "; color: " + self.aw.lcdpaletteF['timer'] + ";" + self.commonstyle)
        self.lcd1LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['timer'] + "; color: " + self.aw.lcdpaletteF['timer'] + ";" + self.commonstyle)
        self.lcd2backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['et'] + "; color: " + self.aw.lcdpaletteF['et'] + ";" + self.commonstyle)
        self.lcd2LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['et'] + "; color: " + self.aw.lcdpaletteF['et'] + ";" + self.commonstyle)
        self.lcd3backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['bt'] + "; color: " + self.aw.lcdpaletteF['bt'] + ";" + self.commonstyle)
        self.lcd3LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['bt'] + "; color: " + self.aw.lcdpaletteF['bt'] + ";" + self.commonstyle)
        self.lcd4backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['deltaet'] + "; color: " + self.aw.lcdpaletteF['deltaet'] + ";" + self.commonstyle)
        self.lcd4LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['deltaet'] + "; color: " + self.aw.lcdpaletteF['deltaet'] + ";" + self.commonstyle)
        self.lcd5backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['deltabt'] + "; color: " + self.aw.lcdpaletteF['deltabt'] + ";" + self.commonstyle)
        self.lcd5LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['deltabt'] + "; color: " + self.aw.lcdpaletteF['deltabt'] + ";" + self.commonstyle)
        self.lcd6backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['sv'] + "; color: " + self.aw.lcdpaletteF['sv'] + ";" + self.commonstyle)
        self.lcd6LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['sv'] + "; color: " + self.aw.lcdpaletteF['sv'] + ";" + self.commonstyle)
        self.lcd7backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['rstimer'] + "; color: " + self.aw.lcdpaletteF['rstimer'] + ";" + self.commonstyle)
        self.lcd7LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['rstimer'] + "; color: " + self.aw.lcdpaletteF['rstimer'] + ";" + self.commonstyle)
        self.lcd8backButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['slowcoolingtimer'] + "; color: " + self.aw.lcdpaletteF['slowcoolingtimer'] + ";" + self.commonstyle)
        self.lcd8LEDButton.setStyleSheet("background-color: " + self.aw.lcdpaletteB['slowcoolingtimer'] + "; color: " + self.aw.lcdpaletteF['slowcoolingtimer'] + ";" + self.commonstyle)
            
        if str(self.aw.qmc.palette["canvas"]) == 'None':
#            self.canvasLabel.setStyleSheet("QLabel { background-color: #f0f0f0 }")
            self.canvasLabel.setStyleSheet("QPushButton {background-color: #f0f0f0 ;" + self.commonstyle + "}")
            
    def setColorButton(self,button,tag):
        c = self.aw.qmc.palette[tag]
        button.setText(c)
        tc = self.aw.labelBorW(c)
        button.setStyleSheet("QPushButton {background: " + c + "; color: " + tc + ";" + self.commonstyle + "}")

    # adds a new event to the Dlg
    @pyqtSlot(bool)
    def recolor1(self,_):
        self.aw.qmc.changeGColor(1)
        self.setColorButtons()
    
    @pyqtSlot(bool)
    def recolor2(self,_):
        self.aw.qmc.changeGColor(2)
        self.setColorButtons()

    def adjustOpaqenesss(self,spinbox,coloralpha):
        #block button
        spinbox.setDisabled(True)
        self.aw.qmc.alpha[coloralpha] = spinbox.value()/10.
#        coloralpha = spinbox.value()/10.
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        #reactivate button
        spinbox.setDisabled(False)

    @pyqtSlot(int)
    def adjustOpaqenesssSlot(self,_):
        widget = self.sender()
#        if widget == self.opaqbgSpinBox:
#            self.adjustOpaqenesss(self.opaqbgSpinBox,self.aw.qmc.backgroundalpha)
        if widget == self.legendbgSpinBox:
            self.adjustOpaqenesss(self.legendbgSpinBox,"legendbg")
        if widget == self.analysismaskSpinBox:
            self.adjustOpaqenesss(self.analysismaskSpinBox,"analysismask")
        if widget == self.statsanalysisbkgndSpinBox:
            self.adjustOpaqenesss(self.statsanalysisbkgndSpinBox,"statsanalysisbkgnd")

    @pyqtSlot(bool)
    def setbgColorSlot(self,_):
        widget = self.sender()
        if widget == self.bgmetButton:
            self.setbgColor("ET",self.bgmetButton,self.aw.qmc.backgroundmetcolor)
        elif widget == self.bgbtButton:
            self.setbgColor("BT",self.bgbtButton,self.aw.qmc.backgroundbtcolor)
        elif widget == self.bgdeltametButton:
            self.setbgColor("DeltaET",self.bgdeltametButton,self.aw.qmc.backgrounddeltaetcolor)
        elif widget == self.bgdeltabtButton:
            self.setbgColor("DeltaBT",self.bgdeltabtButton,self.aw.qmc.backgrounddeltabtcolor)
        elif widget == self.bgextraButton:
            self.setbgColor("Extra1",self.bgextraButton,self.aw.qmc.backgroundxtcolor)
        elif widget == self.bgextra2Button:
            self.setbgColor("Extra2",self.bgextra2Button,self.aw.qmc.backgroundytcolor)

    def setbgColor(self,title,var,color):
        labelcolor = QColor(color)
        colorf = self.aw.colordialog(labelcolor)
        if colorf.isValid():
            color = str(colorf.name())
            self.aw.updateCanvasColors()
            tc = self.aw.labelBorW(color)
            var.setText(colorf.name())
            var.setStyleSheet("QPushButton { background-color: " + color + "; color: " + tc + ";" + self.commonstyle + "}");
#  is this needed?            var.setPalette(QPalette(colorf))
            self.aw.qmc.fig.canvas.redraw(recomputeAllDeltas=False)
            if title == "ET":
                self.aw.qmc.backgroundmetcolor = color
            elif title == "BT":
                self.aw.qmc.backgroundbtcolor = color
            elif title == "DeltaET":
                self.aw.qmc.backgrounddeltaetcolor = color
            elif title == "DeltaBT":
                self.aw.qmc.backgrounddeltabtcolor = color
            elif title == "Extra1":
                self.aw.qmc.backgroundxtcolor = color
            elif title == "Extra2":
                self.aw.qmc.backgroundytcolor = color
            self.aw.sendmessage(QApplication.translate("Message","Color of {0} set to {1}", None).format(title,str(color)))

    def setlcdColor(self,palette,disj_palette,select):
        res = self.aw.colordialog(QColor(palette[select]))
        if QColor.isValid(res):
            nc = str(res.name())
            if nc != disj_palette[select]:
                palette[select] = nc
            else:
                QMessageBox.question(self.aw,QApplication.translate("Message", "Config LCD colors",None),
                    "Digits color and Background color cannot be the same.", QMessageBox.Ok)
    
    @pyqtSlot(bool)
    def setColorSlot(self,_):
        widget = self.sender()
        if widget == self.metButton:
            self.setColor("ET",self.metButton,"et")
        elif widget == self.btButton:
            self.setColor("BT",self.btButton,"bt")
        elif widget == self.deltametButton:
            self.setColor("DeltaET",self.deltametButton,"deltaet")
        elif widget == self.deltabtButton:
            self.setColor("DeltaBT",self.deltabtButton,"deltabt")
        elif widget == self.backgroundButton:
            self.setColor("Background",self.backgroundButton,"background")
        elif widget == self.gridButton:
            self.setColor("Grid",self.gridButton,"grid")
        elif widget == self.titleButton:
            self.setColor("Title",self.titleButton,"title")
        elif widget ==self.yButton:
            self.setColor("Y Button",self.yButton,"ylabel")
        elif widget == self.xButton:
            self.setColor("X Button",self.xButton,"xlabel")
        elif widget == self.rect1Button:
            self.setColor("Drying Phase",self.rect1Button,"rect1")
        elif widget == self.rect2Button:
            self.setColor("Maillard Phase",self.rect2Button,"rect2")
        elif widget == self.rect3Button:
            self.setColor("Finishing Phase",self.rect3Button,"rect3")
        elif widget == self.rect4Button:
            self.setColor("Cooling Phase",self.rect4Button,"rect4")
        elif widget == self.rect5Button:
            self.setColor("Bars Bkgnd",self.rect5Button,"rect5")
        elif widget == self.markersButton:
            self.setColor("Markers",self.markersButton,"markers")
        elif widget == self.textButton:
            self.setColor("Text",self.textButton,"text")
        elif widget == self.watermarksButton:
            self.setColor("Watermarks",self.watermarksButton,"watermarks")
        elif widget == self.timeguideButton:
            self.setColor("Time Guide",self.timeguideButton,"timeguide")
        elif widget == self.aucguideButton:
            self.setColor("AUC Guide",self.aucguideButton,"aucguide")
        elif widget == self.aucareaButton:
            self.setColor("AUC Area",self.aucareaButton,"aucarea")
        elif widget == self.legendbgButton:
            self.setColor("legendbg",self.legendbgButton,"legendbg")
        elif widget == self.legendborderButton:
            self.setColor("legendborder",self.legendborderButton,"legendborder")
        elif widget == self.canvasButton:
            self.setColor("canvas",self.canvasButton,"canvas")
        elif widget == self.specialeventboxButton:
            self.setColor("specialeventbox",self.specialeventboxButton,"specialeventbox")
        elif widget == self.specialeventtextButton:
            self.setColor("specialeventtext",self.specialeventtextButton,"specialeventtext")
        elif widget == self.bgeventmarkerButton:
            self.setColor("bgeventmarker",self.bgeventmarkerButton,"bgeventmarker")
        elif widget == self.bgeventtextButton:
            self.setColor("bgeventtext",self.bgeventtextButton,"bgeventtext")
        elif widget == self.mettextButton:
            self.setColor("mettext",self.mettextButton,"mettext")
        elif widget == self.metboxButton:
            self.setColor("metbox",self.metboxButton,"metbox")
        elif widget == self.analysismaskButton:
            self.setColor("Analysis Mask",self.analysismaskButton,"analysismask")
        elif widget == self.statsanalysisbkgndButton:
            self.setColor("Analysis Result",self.statsanalysisbkgndButton,"statsanalysisbkgnd")
            
    def colorButton(self,s):
        button = QPushButton(s)
        button.setPalette(QPalette(QColor(s)))
        button.setStyleSheet("QPushButton {background-color:" + s + ";" + self.commonstyle + "}")
        return button

    def setColor(self,title,var,color):
        labelcolor = QColor(self.aw.qmc.palette[color])
        colorf = self.aw.colordialog(labelcolor)
        if colorf.isValid():
            self.aw.qmc.palette[color] = str(colorf.name())
            self.aw.updateCanvasColors()
            self.aw.applyStandardButtonVisibility()
            self.aw.update_extraeventbuttons_visibility()
            var.setText(colorf.name())
            tc = self.aw.labelBorW(self.aw.qmc.palette[color])
            var.setStyleSheet("QPushButton { background: " + self.aw.qmc.palette[color] + "; color: " + tc + ";" + self.commonstyle + "}")
#            var.setPalette(QPalette(colorf))
            self.aw.qmc.fig.canvas.redraw(recomputeAllDeltas=False)
            if title == "ET":
                self.aw.setLabelColor(self.aw.label2,QColor(self.aw.qmc.palette[color]))
            elif title == "BT":
                self.aw.setLabelColor(self.aw.label3,QColor(self.aw.qmc.palette[color]))
            elif title == "DeltaET":
                self.aw.setLabelColor(self.aw.label4,QColor(self.aw.qmc.palette[color]))
            elif title == "DeltaBT":
                self.aw.setLabelColor(self.aw.label5,QColor(self.aw.qmc.palette[color]))
            self.aw.sendmessage(QApplication.translate("Message","Color of {0} set to {1}", None).format(title,str(self.aw.qmc.palette[color])))

    @pyqtSlot(int)
    def adjustintensity(self,_):
        #block button
        self.opaqbgSpinBox.setDisabled(True)
        self.aw.qmc.backgroundalpha = self.opaqbgSpinBox.value()/10.
        self.aw.qmc.redraw(recomputeAllDeltas=False)
        #reactivate button
        self.opaqbgSpinBox.setDisabled(False)


