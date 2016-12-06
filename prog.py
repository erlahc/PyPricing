import sys
from dataanalysis import *
import numpy as np
import matplotlib.pyplot as plt
from classmappingv2 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from gui2 import Ui_MainWindow
 
class MyFirstGuiProgram(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.refresh_display()

        self.slideScope.sliderReleased.connect(self.scope_changed)
        self.listScope.itemClicked.connect(self.scope_activated)
        self.buttonScope.clicked.connect(self.scope_raz)

        self.slideCsp.sliderReleased.connect(self.csp_changed)
        self.listCsp.itemClicked.connect(self.csp_activated)
        self.buttonCsp.clicked.connect(self.csp_raz)

        self.slideCountry.sliderReleased.connect(self.country_changed)
        self.listCountry.itemClicked.connect(self.country_activated)
        self.buttonCountry.clicked.connect(self.country_raz)

        self.goButton.clicked.connect(self.build_time_waterfall)
        self.countryButton.clicked.connect(self.build_country_modified)

    def build_country_modified(self):
        plt.rcdefaults()
        country_modified=get_country_modified()
        x=1
        for i in country_modified:
            plt.bar(x,i[1])
        plt.show()

    def build_time_waterfall(self):
        plt.rcdefaults()
        fig, ax = plt.subplots()
        b=waterfallgraph((get_volumebase(),get_scope_impact(),get_csp_impact(),get_country_impact(),get_volumedriven()))
        for i in range(len(b)):
            if b[i][1]>=0:
                ax.broken_barh([b[i]],(i*10+10,9),facecolors='green')
            else:
                ax.broken_barh([b[i]],(i*10+10,9),facecolors='red')
        plt.show()

    def refresh_display(self):
        self.display_scope_list()
        self.display_csp_list()
        self.display_country_list()
        self.display_company_list()
        self.textVolume.setText(str(get_volumedriven())) 

    def scope_changed(self):
        try:
            i = self.listScope.selectedItems()
            j=self.slideScope.value()
            update_scope(i[0].text(),j)
            self.refresh_display()
        except IndexError:
            print('Pas de selection')

    def scope_activated(self):
        i = self.listScope.selectedItems()
        i=float(i[1].text())
        self.slideScope.setValue(i)

    def scope_raz(self):
        try:
            i = self.listScope.selectedItems()
            update_scope(i[0].text(),0)
            self.refresh_display()
            self.scope_activated()
        except IndexError:
            print('Pas de selection')

    def display_scope_list(self):
        base=get_scope_list()
        x=len(base)
        y=len(base[0])
        self.listScope.setRowCount(x)
        self.listScope.setColumnCount(y)
        self.listScope.setColumnWidth(0,80)
        self.listScope.setColumnWidth(1,39)
        for i in range(x):
            for j in range(y): 
                a=base[i][j]
                self.listScope.setItem(i,j,QtWidgets.QTableWidgetItem(str(a)))

    def csp_changed(self):
        try:
            i = self.listCsp.selectedItems()
            j=self.slideCsp.value()
            update_csp(i[0].text(),j)
            self.refresh_display()
        except IndexError:
            print('Pas de selection')

    def csp_activated(self):
        i = self.listCsp.selectedItems()
        i=float(i[1].text())
        self.slideCsp.setValue(i)

    def csp_raz(self):
        try:
            i = self.listCsp.selectedItems()
            update_csp(i[0].text(),0)
            self.refresh_display()
            self.csp_activated()
        except IndexError:
            print('Pas de selection')

    def display_csp_list(self):
        base =get_csp_list() 
        x=len(base)
        y=len(base[0])
        self.listCsp.setRowCount(x)
        self.listCsp.setColumnCount(y)
        self.listCsp.setColumnWidth(0,80)
        self.listCsp.setColumnWidth(1,39)
        for i in range(x):
            for j in range(y): 
                a=base[i][j]
                self.listCsp.setItem(i,j,QtWidgets.QTableWidgetItem(str(a)))

    def country_changed(self):
        try:
            i = self.listCountry.selectedItems()
            j=self.slideCountry.value()
            update_country(i[0].text(),round(j/100,1))
            self.refresh_display()
        except IndexError:
            print('Pas de selection')

    def country_activated(self):
        i = self.listCountry.selectedItems()
        i=float(i[1].text())
        self.slideCountry.setValue(i*100)

    def country_raz(self):
        try:
            i = self.listCountry.selectedItems()
            update_country(i[0].text(),get_country_default(i[0].text()))
            self.refresh_display()
            self.country_activated()
        except IndexError:
            print('Pas de selection')

    def display_country_list(self):
        base = get_country_list() 
        x=len(base)
        y=len(base[0])
        self.listCountry.setRowCount(x)
        self.listCountry.setColumnCount(y)
        self.listCountry.setColumnWidth(0,80)
        self.listCountry.setColumnWidth(1,39)
        for i in range(x):
            for j in range(y): 
                a=base[i][j]
                self.listCountry.setItem(i,j,QtWidgets.QTableWidgetItem(str(a)))

    def display_company_list(self):
        base = get_company_list()
        x=len(base)
        y=len(base[0])
        self.listCompany.setRowCount(x)
        self.listCompany.setColumnCount(y)
        for i in range(y):
            if i==0 or i ==1:
                self.listCompany.setColumnWidth(i,100)
            else:  
                self.listCompany.setColumnWidth(i,80)
        for i in range(x):
            for j in range(y): 
                a=base[i][j]
                self.listCompany.setItem(i,j,QtWidgets.QTableWidgetItem(str(a)))

 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = MyFirstGuiProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())