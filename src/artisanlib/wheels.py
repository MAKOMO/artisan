#!/usr/bin/env python3

# ABOUT
# Artisan Wheels Dialog

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

from artisanlib.dialogs import ArtisanDialog

from matplotlib import rcParams

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QLabel, QTableWidget, QPushButton, 
    QComboBox, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QDialogButtonBox,
    QDoubleSpinBox, QGroupBox, QLineEdit, QSpinBox)


class WheelDlg(ArtisanDialog):
    def __init__(self, parent = None, aw = None):
        super(WheelDlg,self).__init__(parent, aw)
        self.setAttribute(Qt.WA_DeleteOnClose, False) # overwrite the ArtisanDialog class default here!!
        
        rcParams['path.effects'] = []
            
        self.setModal(True)
        self.setWindowTitle(QApplication.translate("Form Caption","Wheel Graph Editor",None))
        #table
        self.datatable = QTableWidget()
        self.createdatatable()
        #table for labels
        self.labeltable = QTableWidget()

        self.subdialogbuttons = QDialogButtonBox(QDialogButtonBox.Close | QDialogButtonBox.RestoreDefaults, Qt.Horizontal)
        self.setButtonTranslations(self.subdialogbuttons.button(QDialogButtonBox.RestoreDefaults),"Restore Defaults",QApplication.translate("Button","Restore Defaults", None))
        self.setButtonTranslations(self.subdialogbuttons.button(QDialogButtonBox.Close),"Close",QApplication.translate("Button","Close", None))
        
        self.subdialogbuttons.rejected.connect(self.closelabels)
        self.subdialogbuttons.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.resetlabelparents)
        
        self.labelwheelx = 0   #index of wheel being edited on labeltable
#        self.hierarchyButton = QPushButton(QApplication.translate("Button","Reverse Hierarchy",None))
#        self.hierarchyButton.setToolTip(QApplication.translate("Tooltip","Sets graph hierarchy child->parent instead of parent->child",None))
#        self.hierarchyButton.clicked.connect(self.aw.qmc.setWheelHierarchy)
        self.labeltable.setVisible(False)
        self.subdialogbuttons.setVisible(False)
        aspectlabel = QLabel(QApplication.translate("Label","Ratio",None))
        self.aspectSpinBox = QDoubleSpinBox()
        self.aspectSpinBox.setToolTip(QApplication.translate("Tooltip","Aspect Ratio",None))
        self.aspectSpinBox.setRange(0.,2.)
        self.aspectSpinBox.setSingleStep(.1)
        self.aspectSpinBox.setValue(self.aw.qmc.wheelaspect)
        self.aspectSpinBox.valueChanged.connect(self.setaspect)
        txtlabel = QLabel(QApplication.translate("Label","Text",None))
        txtButtonplus = QPushButton(QApplication.translate("Button","+",None))
        txtButtonplus.setToolTip(QApplication.translate("Tooltip","Increase size of text in all the graph",None))
        txtButtonplus.clicked.connect(self.changetext1)
        txtButtonminus = QPushButton(QApplication.translate("Button","-",None))
        txtButtonminus.setToolTip(QApplication.translate("Tooltip","Decrease size of text in all the graph",None))
        txtButtonminus.clicked.connect(self.changetext0)
        edgelabel = QLabel(QApplication.translate("Label","Edge",None))
        self.edgeSpinBox = QSpinBox()
        self.edgeSpinBox.setToolTip(QApplication.translate("Tooltip","Decorative edge beween wheels",None))
        self.edgeSpinBox.setRange(0,5)
        self.edgeSpinBox.setValue(int(self.aw.qmc.wheeledge*100))
        self.edgeSpinBox.valueChanged.connect(self.setedge)
        linewidthlabel = QLabel(QApplication.translate("Label","Line",None))
        self.linewidthSpinBox = QSpinBox()
        self.linewidthSpinBox.setToolTip(QApplication.translate("Tooltip","Line thickness",None))
        self.linewidthSpinBox.setRange(0,20)
        self.linewidthSpinBox.setValue(self.aw.qmc.wheellinewidth)
        self.linewidthSpinBox.valueChanged.connect(self.setlinewidth)
        linecolor = QPushButton(QApplication.translate("Button","Line Color",None))
        linecolor.setToolTip(QApplication.translate("Tooltip","Line color",None))
        linecolor.clicked.connect(self.setlinecolor)        
        textcolor = QPushButton(QApplication.translate("Button","Text Color",None))
        textcolor.setToolTip(QApplication.translate("Tooltip","Text color",None))
        textcolor.clicked.connect(self.settextcolor)        
        colorlabel = QLabel(QApplication.translate("Label","Color pattern",None))
        self.colorSpinBox = QSpinBox()
        self.colorSpinBox.setToolTip(QApplication.translate("Tooltip","Apply color pattern to whole graph",None))
        self.colorSpinBox.setRange(0,255)
        self.colorSpinBox.setValue(self.aw.qmc.wheelcolorpattern)
        self.colorSpinBox.setWrapping(True)
        self.colorSpinBox.valueChanged.connect(self.setcolorpattern)
        addButton = QPushButton(QApplication.translate("Button","Add",None))
        addButton.setToolTip(QApplication.translate("Tooltip","Add new wheel",None))
        addButton.clicked.connect(self.insertwheel)
        rotateLeftButton = QPushButton(QApplication.translate("Button","<",None))
        rotateLeftButton.setToolTip(QApplication.translate("Tooltip","Rotate graph 1 degree counter clockwise",None))
        rotateLeftButton.clicked.connect(self.rotatewheels1)
        rotateRightButton = QPushButton(QApplication.translate("Button",">",None))
        rotateRightButton.setToolTip(QApplication.translate("Tooltip","Rotate graph 1 degree clockwise",None))
        rotateRightButton.clicked.connect(self.rotatewheels0)
        
        self.main_buttons = QDialogButtonBox()
        
        saveButton = QPushButton(QApplication.translate("Button","Save File",None))
        saveButton.clicked.connect(self.fileSave)
        saveButton.setToolTip(QApplication.translate("Tooltip","Save graph to a text file.wg",None))
        self.main_buttons.addButton(saveButton,QDialogButtonBox.ActionRole)
        
        saveImgButton = QPushButton(QApplication.translate("Button","Save Img",None))
        saveImgButton.setToolTip(QApplication.translate("Tooltip","Save image using current graph size to a png format",None))
        #saveImgButton.clicked.connect(self.aw.resizeImg_0_1) # save as PNG (raster)
        saveImgButton.clicked.connect(self.aw.saveVectorGraph_PDF) # save as PDF (vector)
        self.main_buttons.addButton(saveImgButton,QDialogButtonBox.ActionRole)
        
        openButton = self.main_buttons.addButton(QDialogButtonBox.Open)
        openButton.setToolTip(QApplication.translate("Tooltip","open wheel graph file",None))
        openButton.clicked.connect(self.loadWheel)
        
        viewModeButton = self.main_buttons.addButton(QDialogButtonBox.Close)
        viewModeButton.setToolTip(QApplication.translate("Tooltip","Sets Wheel graph to view mode",None))
        viewModeButton.clicked.connect(self.viewmode)
        
        if self.aw.locale not in self.aw.qtbase_locales:
            self.main_buttons.button(QDialogButtonBox.Close).setText(QApplication.translate("Button","Close", None))
            self.main_buttons.button(QDialogButtonBox.Open).setText(QApplication.translate("Button","Open",None))
        
        self.aw.qmc.drawWheel()
        label1layout = QVBoxLayout()
        label2layout = QHBoxLayout()
        label1layout.addWidget(self.labeltable)
        label2layout.addWidget(self.subdialogbuttons)
        label1layout.addLayout(label2layout)
        self.labelGroupLayout = QGroupBox(QApplication.translate("GroupBox","Label Properties",None))
        self.labelGroupLayout.setLayout(label1layout)
        self.labelGroupLayout.setVisible(False)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.main_buttons)
        configlayout =  QHBoxLayout()
        configlayout.addWidget(colorlabel)
        configlayout.addWidget(self.colorSpinBox)
        configlayout.addWidget(aspectlabel)
        configlayout.addWidget(self.aspectSpinBox)
        configlayout.addWidget(edgelabel)
        configlayout.addWidget(self.edgeSpinBox)
        configlayout.addWidget(linewidthlabel)
        configlayout.addWidget(self.linewidthSpinBox)
        configlayout.addWidget(linecolor)
        configlayout.addWidget(textcolor)
        configlayout.addWidget(txtlabel)
        configlayout.addWidget(txtButtonplus)
        configlayout.addWidget(txtButtonminus)
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(addButton)
        controlLayout.addWidget(rotateLeftButton)
        controlLayout.addWidget(rotateRightButton)
#        controlLayout.addWidget(self.hierarchyButton)
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.datatable)
        mainlayout.addWidget(self.labelGroupLayout)
        mainlayout.addLayout(controlLayout)
        mainlayout.addLayout(configlayout)
        mainlayout.addLayout(buttonlayout)
        self.setLayout(mainlayout)
        
    def close(self):
        self.accept()

    #creates config table for wheel with index x
    @pyqtSlot(bool)
    def createlabeltable(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),3)
        if x is not None:
            self.createlabeltablex(x)

    def createlabeltablex(self,x):
        self.labelwheelx = x                    #wheel being edited
        self.labelGroupLayout.setVisible(True)
        self.labeltable.setVisible(True)
        self.subdialogbuttons.setVisible(True)
        
        nlabels = len(self.aw.qmc.wheelnames[x])
        # self.labeltable.clear() # this crashes Ubuntu 16.04
        self.labeltable.clearSelection() # this seems to work also for Ubuntu 16.04
        
        if nlabels:
            self.labeltable.setRowCount(nlabels)
            self.labeltable.setColumnCount(5)
            self.labeltable.setHorizontalHeaderLabels([QApplication.translate("Table","Label",None),
                                                       QApplication.translate("Table","Parent",None),
                                                       QApplication.translate("Table","Width",None),
                                                       QApplication.translate("Table","Color",None),
                                                       QApplication.translate("Table","Opaqueness",None)])
            self.labeltable.setAlternatingRowColors(True)
            self.labeltable.setEditTriggers(QTableWidget.NoEditTriggers)
            self.labeltable.setSelectionBehavior(QTableWidget.SelectRows)
            self.labeltable.setSelectionMode(QTableWidget.SingleSelection)
            self.labeltable.setShowGrid(True)
            self.labeltable.verticalHeader().setSectionResizeMode(2)
            #populate table
            for i in range(nlabels):
                label = QTableWidgetItem(self.aw.qmc.wheelnames[x][i])
                parentComboBox =  QComboBox()
                if x > 0:
                    items = self.aw.qmc.wheelnames[x-1][:]
                    items.insert(0,"")
                    parentComboBox.addItems(items)
                    if self.aw.qmc.wheellabelparent[x][i]:
                        parentComboBox.setCurrentIndex(self.aw.qmc.wheellabelparent[x][i])
                else:
                    parentComboBox.addItems([])
                parentComboBox.currentIndexChanged.connect(self.setwheelchild)
                labelwidthSpinBox = QDoubleSpinBox()
                labelwidthSpinBox.setRange(1.,100.)
                labelwidthSpinBox.setValue(self.aw.qmc.segmentlengths[x][i])
                labelwidthSpinBox.setSuffix("%")
                labelwidthSpinBox.valueChanged.connect(self.setlabelwidth)
                colorButton = QPushButton("Set Color")
                colorButton.clicked.connect(self.setsegmentcolor)
                alphaSpinBox = QSpinBox()
                alphaSpinBox.setRange(0,10)
                alphaSpinBox.setValue(int(self.aw.qmc.segmentsalpha[x][i]*10))
                alphaSpinBox.valueChanged.connect(self.setsegmentalpha)
                #add widgets to the table
                self.labeltable.setItem(i,0,label)
                self.labeltable.setCellWidget(i,1,parentComboBox)
                self.labeltable.setCellWidget(i,2,labelwidthSpinBox)
                self.labeltable.setCellWidget(i,3,colorButton)
                self.labeltable.setCellWidget(i,4,alphaSpinBox)

    @pyqtSlot(bool)
    def setsegmentcolor(self,_):
        i = self.aw.findWidgetsRow(self.labeltable,self.sender(),3)
        if i is not None:
            x = self.labelwheelx
            colorf = self.aw.colordialog(QColor(self.aw.qmc.wheelcolor[x][i]))
            if colorf.isValid():
                colorname = str(colorf.name())
                self.aw.qmc.wheelcolor[x][i] = colorname      #add new color to label
                self.createdatatable()                           #update main table with label names (label::color)
                self.aw.qmc.drawWheel()

    #sets a uniform color in wheel
    @pyqtSlot(bool)
    def setwheelcolor(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),8)
        if x is not None:
            colorf = self.aw.colordialog(QColor(self.aw.qmc.wheelcolor[x][0]))
            if colorf.isValid():
                colorname = str(colorf.name())
                for i in range(len(self.aw.qmc.wheelcolor[x])):
                    self.aw.qmc.wheelcolor[x][i] =  colorname
            self.createdatatable()
            self.aw.qmc.drawWheel()

    #sets color pattern (many colors) in wheel
    @pyqtSlot(int)
    def setwheelcolorpattern(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),9)
        if x is not None:
            wsb =  self.datatable.cellWidget(x,9)
            wpattern = wsb.value()
            wlen = len(self.aw.qmc.wheelcolor[x])
            for i in range(wlen):
                color = QColor()
                color.setHsv((360/wlen)*i*wpattern,255,255,255)
                self.aw.qmc.wheelcolor[x][i] = str(color.name())
            self.aw.qmc.drawWheel()

    #sets color pattern (many colors) for whole graph
    @pyqtSlot(int)
    def setcolorpattern(self,_):
        self.aw.qmc.wheelcolorpattern = self.colorSpinBox.value()
        if self.aw.qmc.wheelcolorpattern:
            for x in range(len(self.aw.qmc.wheelcolor)):
                wlen = len(self.aw.qmc.wheelcolor[x])
                for i in range(wlen):
                    color = QColor()
                    color.setHsv((360/wlen)*i*self.aw.qmc.wheelcolorpattern,255,255,255)
                    self.aw.qmc.wheelcolor[x][i] = str(color.name())
            self.aw.qmc.drawWheel()

    @pyqtSlot(int)
    def setsegmentalpha(self,z):
        u = self.aw.findWidgetsRow(self.labeltable,self.sender(),4)
        if u is not None:
            x = self.labelwheelx
            self.aw.qmc.segmentsalpha[x][u] = float(z/10.)
            self.aw.qmc.drawWheel()

    #rotate whole graph
    @pyqtSlot(bool)
    def rotatewheels1(self,_):
        for i in range(len(self.aw.qmc.startangle)):
            self.aw.qmc.startangle[i] += 1
        self.aw.qmc.drawWheel()
    
    @pyqtSlot(bool)
    def rotatewheels0(self,_):
        for i in range(len(self.aw.qmc.startangle)):
            self.aw.qmc.startangle[i] -= 1
        self.aw.qmc.drawWheel()

    #z= new width%, x= wheel number index, u = index of segment in the wheel
    @pyqtSlot(float)
    def setlabelwidth(self,z):
        u = self.aw.findWidgetsRow(self.labeltable,self.sender(),2)
        if u is not None:
            x = self.labelwheelx
            newwidth = z
            oldwidth = self.aw.qmc.segmentlengths[x][u]
            diff = newwidth - oldwidth
            l = len(self.aw.qmc.segmentlengths[x])
            for i in range(l):
                if i != u:
                    if diff > 0:
                        self.aw.qmc.segmentlengths[x][i] -= abs(float(diff))/(l-1)
                    else:
                        self.aw.qmc.segmentlengths[x][i] += abs(float(diff))/(l-1)
            self.aw.qmc.segmentlengths[x][u] = newwidth
            self.aw.qmc.drawWheel()

    #input: z = index of parent in previus wheel; x = wheel number; i = index of element in wheel
    @pyqtSlot(int)
    def setwheelchild(self,z):
        i = self.aw.findWidgetsRow(self.labeltable,self.sender(),1)
        if i is not None:
            self.aw.qmc.setwheelchild(z,self.labelwheelx,i)
            self.aw.qmc.drawWheel()
            self.createdatatable() #update data table

    #deletes parent-child relation in a wheel. It obtains the wheel index by self.labelwheelx
    @pyqtSlot(bool)
    def resetlabelparents(self,_):
        x = self.labelwheelx
        nsegments = len(self.aw.qmc.wheellabelparent[x])
        for i in range(nsegments):
            self.aw.qmc.wheellabelparent[x][i] = 0
            self.aw.qmc.segmentlengths[x][i] = 100./nsegments
        self.aw.qmc.drawWheel()
        self.createlabeltablex(x)

    @pyqtSlot(float)
    def setaspect(self,_):
        self.aw.qmc.wheelaspect = self.aspectSpinBox.value()
        self.aw.qmc.drawWheel()

    #adjust decorative edge between wheels
    @pyqtSlot(int)
    def setedge(self):
        self.aw.qmc.wheeledge = float(self.edgeSpinBox.value())/100.
        self.aw.qmc.drawWheel()

    #adjusts line thickness
    @pyqtSlot(int)
    def setlinewidth(self,_):
        self.aw.qmc.wheellinewidth = self.linewidthSpinBox.value()
        self.aw.qmc.drawWheel()

    #sets line color
    @pyqtSlot(bool)
    def setlinecolor(self,_):
        colorf = self.aw.colordialog(QColor(self.aw.qmc.wheellinecolor))
        if colorf.isValid():
            colorname = str(colorf.name())
            #self.aw.qmc.wheellinealpha = colorf.alphaF()
            self.aw.qmc.wheellinecolor = colorname      #add new color to label
            self.aw.qmc.drawWheel()
            
    #sets text color
    @pyqtSlot(bool)
    def settextcolor(self,_):
        colorf = self.aw.colordialog(QColor(self.aw.qmc.wheeltextcolor))
        if colorf.isValid():
            colorname = str(colorf.name())
            #self.aw.qmc.wheeltextalpha = colorf.alphaF()
            self.aw.qmc.wheeltextcolor = colorname      #add new color to label
            self.aw.qmc.drawWheel()

    #makes not visible the wheel config table
    @pyqtSlot()
    def closelabels(self):
        self.labelGroupLayout.setVisible(False)
        self.labeltable.setVisible(False)
#        self.labelCloseButton.setVisible(False)
#        self.labelResetButton.setVisible(False)
        self.subdialogbuttons.setVisible(False)

    #creates graph table
    def createdatatable(self):
        ndata = len(self.aw.qmc.wheelnames)
        
        # self.datatable.clear() # this crashes Ubuntu 16.04
#        if ndata != 0:
#            self.datatable.clearContents() # this crashes Ubuntu 16.04 if device table is empty and also sometimes else
        self.datatable.clearSelection() # this seems to work also for Ubuntu 16.04
        
        self.datatable.setRowCount(ndata)
        self.datatable.setColumnCount(10)
        self.datatable.setHorizontalHeaderLabels([QApplication.translate("Table","Delete Wheel",None),
                                                  QApplication.translate("Table","Edit Labels",None),
                                                  QApplication.translate("Table","Update Labels",None),
                                                  QApplication.translate("Table","Properties",None),
                                                  QApplication.translate("Table","Radius",None),
                                                  QApplication.translate("Table","Starting angle",None),
                                                  QApplication.translate("Table","Projection",None),
                                                  QApplication.translate("Table","Text Size",None),
                                                  QApplication.translate("Table","Color",None),
                                                  QApplication.translate("Table","Color Pattern",None)])
        self.datatable.setAlternatingRowColors(True)
        self.datatable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.datatable.setSelectionBehavior(QTableWidget.SelectRows)
        self.datatable.setSelectionMode(QTableWidget.SingleSelection)
        self.datatable.setShowGrid(True)
        self.datatable.verticalHeader().setSectionResizeMode(2)
        #populate table
        for i in range(ndata):
            delButton = QPushButton(QApplication.translate("Button","Delete",None))
            delButton.clicked.connect(self.popwheel)
            labelsedit = QLineEdit(str(",".join(self.aw.qmc.wheelnames[i])))
            updateButton = QPushButton(QApplication.translate("Button","Update",None))
            updateButton.clicked.connect(self.updatelabels)
            setButton = QPushButton(QApplication.translate("Button","Select",None))
            setButton.clicked.connect(self.createlabeltable)
            widthSpinBox = QDoubleSpinBox()
            widthSpinBox.setRange(1.,100.)
            widthSpinBox.setValue(self.aw.qmc.wradii[i])
            widthSpinBox.setSuffix("%")
            widthSpinBox.valueChanged.connect(self.setwidth)
            angleSpinBox = QSpinBox()
            angleSpinBox.setSuffix(QApplication.translate("Label"," dg",None))
            angleSpinBox.setRange(0,359)
            angleSpinBox.setWrapping(True)
            angleSpinBox.setValue(self.aw.qmc.startangle[i])
            angleSpinBox.valueChanged.connect(self.setangle)
            projectionComboBox =  QComboBox()
            projectionComboBox.addItems([QApplication.translate("ComboBox","Flat",None),
                                         QApplication.translate("ComboBox","Perpendicular",None),
                                         QApplication.translate("ComboBox","Radial",None)])
            projectionComboBox.setCurrentIndex(self.aw.qmc.projection[i])
            projectionComboBox.currentIndexChanged.connect(self.setprojection)
            txtSpinBox = QSpinBox()
            txtSpinBox.setRange(1,30)
            txtSpinBox.setValue(self.aw.qmc.wheeltextsize[i])
            txtSpinBox.valueChanged.connect(self.setTextsizeX)
            colorButton = QPushButton(QApplication.translate("Button","Set Color",None))
            colorButton.clicked.connect(self.setwheelcolor)
            colorSpinBox = QSpinBox()
            colorSpinBox.setRange(0,255)
            colorSpinBox.setWrapping(True)
            colorSpinBox.valueChanged.connect(self.setwheelcolorpattern)
            #add widgets to the table
            self.datatable.setCellWidget(i,0,delButton)
            self.datatable.setCellWidget(i,1,labelsedit)
            self.datatable.setCellWidget(i,2,updateButton)
            self.datatable.setCellWidget(i,3,setButton)
            self.datatable.setCellWidget(i,4,widthSpinBox)
            self.datatable.setCellWidget(i,5,angleSpinBox)
            self.datatable.setCellWidget(i,6,projectionComboBox)
            self.datatable.setCellWidget(i,7,txtSpinBox)
            self.datatable.setCellWidget(i,8,colorButton)
            self.datatable.setCellWidget(i,9,colorSpinBox)

    #reads label edit box for wheel with index x, and updates labels
    @pyqtSlot(bool)
    def updatelabels(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),2)
        if x is not None:
            labelsedit =  self.datatable.cellWidget(x,1)
            text  = str(labelsedit.text())
            if "\\n" in text:              #make multiple line text if "\n" found in label string
                parts = text.split("\\n")
                text = chr(10).join(parts)
            newwheellabels = text.strip().split(",")
            newnlabels = len(newwheellabels)
            oldnlabels = len(self.aw.qmc.wheelnames[x])
            #adjust segments len and alpha for each wheel if number of labels changed
            if oldnlabels != newnlabels:
                self.aw.qmc.segmentlengths[x] = [100./newnlabels]*newnlabels
                self.aw.qmc.segmentsalpha[x] = [.3]*newnlabels
                self.aw.qmc.wheellabelparent[x] = [0]*newnlabels
                self.aw.qmc.wheelcolor[x] = [self.aw.qmc.wheelcolor[x][0]]*newnlabels
            self.aw.qmc.wheelnames[x] = newwheellabels[:]
            self.aw.qmc.drawWheel()

    #sets radii for a wheel
    @pyqtSlot(float)
    def setwidth(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),4)
        if x is not None:
            widthSpinBox = self.datatable.cellWidget(x,4)
            newwidth = widthSpinBox.value()
            oldwidth = self.aw.qmc.wradii[x]
            diff = newwidth - oldwidth
            l = len(self.aw.qmc.wradii)
            for i in range(l):
                if i != x:
                    if diff > 0:
                        self.aw.qmc.wradii[i] -= abs(float(diff))/(l-1)
                    else:
                        self.aw.qmc.wradii[i] += abs(float(diff))/(l-1)
            self.aw.qmc.wradii[x] = newwidth
            #Need 100.0% coverage. Correct for numerical floating point rounding errors:
            count = 0.
            for i in range(len(self.aw.qmc.wradii)):
                count +=  self.aw.qmc.wradii[i]
            diff = 100. - count
            if diff  != 0.:
                if diff > 0.000:  #if count smaller
                    self.aw.qmc.wradii[x] += abs(diff)
                else:
                    self.aw.qmc.wradii[x] -= abs(diff)
            self.aw.qmc.drawWheel()

    #sets starting angle (rotation) for a wheel with index x
    @pyqtSlot(int)
    def setangle(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),5)
        if x is not None:
            angleSpinBox = self.datatable.cellWidget(x,5)
            self.aw.qmc.startangle[x] = angleSpinBox.value()
            self.aw.qmc.drawWheel()

    #sets text projection style for a wheel with index x
    @pyqtSlot(int)
    def setprojection(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),6)
        if x is not None:
            projectionComboBox = self.datatable.cellWidget(x,6)
            self.aw.qmc.projection[x] = projectionComboBox.currentIndex()
            self.aw.qmc.drawWheel()

    #chages text size in wheel with index x
    @pyqtSlot(int)
    def setTextsizeX(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),7)
        if x is not None:
            txtSpinBox = self.datatable.cellWidget(x,7)
            self.aw.qmc.wheeltextsize[x] = txtSpinBox.value()
            self.aw.qmc.drawWheel()

    #changes size of text in whole graph
    @pyqtSlot(bool)
    def changetext1(self,_):
        for i in range(len(self.aw.qmc.wheeltextsize)):
            self.aw.qmc.wheeltextsize[i] += 1
        self.aw.qmc.drawWheel()
    
    @pyqtSlot(bool)
    def changetext0(self,_):
        for i in range(len(self.aw.qmc.wheeltextsize)):
            self.aw.qmc.wheeltextsize[i] -= 1
        self.aw.qmc.drawWheel()

    #adds new top wheel
    @pyqtSlot(bool)
    def insertwheel(self,_):
        ndata = len(self.aw.qmc.wradii)
        if ndata:
            count = 0.
            for i in range(ndata):
                self.aw.qmc.wradii[i] = 100./(ndata+1)
                count += self.aw.qmc.wradii[i]
            self.aw.qmc.wradii.append(100.-count)
        else:
            self.aw.qmc.wradii.append(100.)
        #find number of labels of most outer wheel (last)
        if len(self.aw.qmc.wheelnames):
            nwheels = len(self.aw.qmc.wheelnames[-1])
        else:                                       #if no wheels
            nwheels = 3
        wn,sl,sa,wlp,co = [],[],[],[],[]
        for i in range(nwheels+1):
            wn.append("W%i %i"%(len(self.aw.qmc.wheelnames)+1,i+1))
            sl.append(100./(nwheels+1))
            sa.append(.3)
            wlp.append(0)
            color = QColor()
            color.setHsv((360/(nwheels+1))*i,255,255,255)
            co.append(str(color.name()))
        self.aw.qmc.wheelnames.append(wn)
        self.aw.qmc.segmentlengths.append(sl)
        self.aw.qmc.segmentsalpha.append(sa)
        self.aw.qmc.wheellabelparent.append(wlp)
        self.aw.qmc.startangle.append(0)
        self.aw.qmc.projection.append(2)
        self.aw.qmc.wheeltextsize.append(10)
        self.aw.qmc.wheelcolor.append(co)
        self.createdatatable()
        self.aw.qmc.drawWheel()

    #deletes wheel with index x
    @pyqtSlot(bool)
    def popwheel(self,_):
        x = self.aw.findWidgetsRow(self.datatable,self.sender(),0)
        if x is not None:
            #correct raius of other wheels (to use 100% coverage)
            width = self.aw.qmc.wradii[x]
            l = len(self.aw.qmc.wradii)
            for i in range(l):
                if i != x:
                    self.aw.qmc.wradii[i] += float(width)/(l-1)
            self.aw.qmc.wheelnames.pop(x)
            self.aw.qmc.wradii.pop(x)
            self.aw.qmc.startangle.pop(x)
            self.aw.qmc.projection.pop(x)
            self.aw.qmc.wheeltextsize.pop(x)
            self.aw.qmc.segmentlengths.pop(x)
            self.aw.qmc.segmentsalpha.pop(x)
            self.aw.qmc.wheellabelparent.pop(x)
            self.aw.qmc.wheelcolor.pop(x)
            self.createdatatable()
            self.aw.qmc.drawWheel()
    
    @pyqtSlot(bool)
    def fileSave(self,_):
        try:
            filename = self.aw.ArtisanSaveFileDialog(msg=QApplication.translate("Message","Save Wheel graph",None),ext="*.wg")
            if filename:
                #write
                self.aw.serialize(filename,self.aw.getWheelGraph())
                self.aw.sendmessage(QApplication.translate("Message","Wheel Graph saved",None))
        except IOError as e:
            self.aw.qmc.adderror((QApplication.translate("Error Message","IO Error:",None) + " Wheel graph filesave(): {0}").format(str(e)))
            return

    @pyqtSlot(bool)
    def loadWheel(self,_):
        filename = self.aw.ArtisanOpenFileDialog(msg=QApplication.translate("Message","Open Wheel Graph",None),path = self.aw.getDefaultPath(),ext="*.wg")
        if filename:
            self.aw.loadWheel(filename)
            self.aw.wheelpath = filename
            self.createdatatable()
            self.aw.qmc.drawWheel()

    def closeEvent(self, _):
        self.viewmode(False)

    @pyqtSlot(bool)
    def viewmode(self,_):
        self.close()
        self.aw.qmc.connectWheel()
        self.aw.qmc.drawWheel()