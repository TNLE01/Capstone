"""
Garden Helper
Capstone Project
Author:
    Truong Le

This is the main file for the Garden Helper app. It is a GUI application that allows users to track their plants,
"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGridLayout, QWidget, 
                            QPushButton, QStackedWidget, QLabel, QListWidget, 
                            QListWidgetItem, QScrollBar, QVBoxLayout, QScrollArea, 
                            QFrame, QLineEdit, QFileDialog, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt
import plantSearchAPI as PS
import plantLookUpAPI as PLU
import AIAssistant as AIA
import projectDatabase as PD
import random


class MainWindow(QMainWindow):
    """
    This is the main class for the MainWindow and GUI.
    """

    def __init__(self):
        """
        This function initializes the main window.
        """
        
        super().__init__()
        self.setWindowTitle("Garden Helper")
        self.setGeometry(700, 300, 1200, 800)
        #self.setFixedSize(1200, 800)
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("Plant Icon-01.png"))
        self.initUI()

    def initUI(self):
        """
        This function initializes all the GUI widgets.
        """

        # Icons
        self.plantIconBW = QPixmap('Plant Icon BW.png')
        self.boxIcon = QPixmap('Background Square.png')
        
        # Center Widget
        centerWidget = QWidget()
        centerWidget.setStyleSheet("background-color: #999999;") ##99FF99
        self.setCentralWidget(centerWidget)

        # User Interactable Frame

        self.userWidget = QWidget()
        self.userWidget.setStyleSheet("background-color: #666666;")
        self.layoutUser = QVBoxLayout()
        self.userWidget.setLayout(self.layoutUser)

        # Title Frame

        self.titleWidget = QStackedWidget()
        self.titleWidget.setStyleSheet("background-color: white;")
        self.layoutUser.addWidget(self.titleWidget, 1)

        self.titleTab = QWidget()
        self.titleTab.setStyleSheet("background-color: white;")
        self.titleWidget.addWidget(self.titleTab)
        self.layoutTitleTab = QGridLayout()
        self.titleTab.setLayout(self.layoutTitleTab)
        
        self.addingTab = QWidget()
        self.addingTab.setStyleSheet("background-color: white;")
        self.titleWidget.addWidget(self.addingTab)
        self.layoutaddingTab = QGridLayout()
        self.addingTab.setLayout(self.layoutaddingTab)

        self.titleLabel = QLabel('Plant Tracker', self.titleTab)
        self.titleLabel.setFont(QFont('Roboto', 20))
        self.titleLabel.setStyleSheet("color: #333333;")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.adjustSize()

        self.addButton = QPushButton('Add', self.titleTab)
        self.addButton.clicked.connect(lambda: self.titleWidget.setCurrentIndex(1))

        self.deleteButton = QPushButton('Delete', self.titleTab)
        self.deleteButton.clicked.connect(self.clickedDeleteButton)

        self.layoutTitleTab.addWidget(self.titleLabel, 0, 0)
        self.layoutTitleTab.addWidget(self.addButton, 1, 0)
        self.layoutTitleTab.addWidget(self.deleteButton, 1, 0)
        self.addButton.raise_()

        self.userInputName = QLineEdit()
        self.userInputName.setPlaceholderText('Save Name')
        self.userInputName.setMaxLength(50)
        self.layoutaddingTab.addWidget(self.userInputName, 0, 0, 1, 2)

        self.comfirmButton = QPushButton('Confirm', self.addingTab)
        self.comfirmButton.clicked.connect(self.clickedComfirmButton)
        self.layoutaddingTab.addWidget(self.comfirmButton, 1, 1,)
        
        self.cancelButton = QPushButton('Cancel', self.addingTab)
        self.cancelButton.clicked.connect(self.clickedCancelButton)
        self.layoutaddingTab.addWidget(self.cancelButton, 1, 0)

        # List Frame

        self.listWidget = QStackedWidget()
        self.listWidget.setStyleSheet("background-color: white;")
        self.layoutUser.addWidget(self.listWidget, 3)

        self.emptyListTab = QWidget()
        self.emptyListTab.setStyleSheet("background-color: white;")
        self.listWidget.addWidget(self.emptyListTab)
        self.layoutEmptyList = QGridLayout()
        self.emptyListTab.setLayout(self.layoutEmptyList)

        self.grayPL = QLabel(self.emptyListTab)
        self.grayPL.setPixmap(self.plantIconBW)
        self.grayPL.adjustSize()

        emptyText = QLabel('  There are no plants  ', self.emptyListTab)
        emptyText.setFont(QFont('Roboto'))
        emptyText.setStyleSheet("color: #333333; border: 1px solid black;")
        emptyText.setAlignment(QtCore.Qt.AlignCenter)
        emptyText.adjustSize()

        self.layoutEmptyList.addWidget(self.grayPL, 0, 0, alignment = Qt.AlignCenter)
        self.layoutEmptyList.addWidget(emptyText, 0, 0, alignment = Qt.AlignCenter)

        self.plantListTab = QListWidget(self)
        self.plantListTab.setStyleSheet("background-color: white;")
        self.listWidget.addWidget(self.plantListTab)
        self.layoutPlantList = QGridLayout()
        self.plantListTab.setLayout(self.layoutPlantList)
        self.current = -1

        self.plantListTab.itemClicked.connect(self.clickeditem)

        # Information Frame

        self.infoWidget = QWidget()
        self.infoWidget.setStyleSheet("background-color: #666666;")
        self.infoTabs = QStackedWidget(self.infoWidget)

        self.noSelectionTab = QWidget()
        self.noSelectionTab.setStyleSheet("background-color: white;")
        self.infoTabs.addWidget(self.noSelectionTab)
        self.layoutNoSelectionTab = QGridLayout()
        self.noSelectionTab.setLayout(self.layoutNoSelectionTab)

        self.grayPI = QLabel(self.noSelectionTab)
        self.grayPI.setPixmap(self.plantIconBW)
        self.grayPI.adjustSize()

        emptyText = QLabel('  No plants selected  ', self.noSelectionTab)
        emptyText.setFont(QFont('Roboto'))
        emptyText.setStyleSheet("color: #333333; border: 1px solid black;")
        emptyText.setAlignment(QtCore.Qt.AlignCenter)
        emptyText.adjustSize()

        self.layoutNoSelectionTab.addWidget(self.grayPI, 0, 0, alignment = Qt.AlignCenter)
        self.layoutNoSelectionTab.addWidget(emptyText, 0, 0, alignment = Qt.AlignCenter)

        self.layoutInfoWidget = QGridLayout()
        self.layoutInfoWidget.addWidget(self.infoTabs)
        self.infoWidget.setLayout(self.layoutInfoWidget)

        # Layout Grid

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.userWidget, 0, 0, 4, 2)
        mainLayout.addWidget(self.infoWidget, 0, 3, 4, 4)
        centerWidget.setLayout(mainLayout) 
    
    def clickedComfirmButton(self):
        """
        This function is for the confirm button to make a new list item.
        """

        # List item name
        itemName = ''
        if self.userInputName.text() == '':
            itemName = self.userInputName.placeholderText()
        else:
            itemName =  self.userInputName.text()

        # Makes a custom list item
        item = customListItem()
        item.setName(itemName)
        item.setPlant('Unknown')
        tag = QListWidgetItem(self.plantListTab)
        tag.setSizeHint(item.sizeHint())
        
        # Add the item to the list widget
        self.plantListTab.addItem(tag)
        self.plantListTab.setItemWidget(tag, item)

        # Clears the user name input
        self.userInputName.clear()
        self.titleWidget.setCurrentIndex(0)

        self.newPlantTab(itemName, tag)

    def makeBoxes(self, layout, value):
        """
        This function set image boxes so that the labels can be align correctly.
    
        Parameters:
        layout (widget): The image file.
        value (int): The spacing for the boxes.
        """

        boxes1 = QLabel()
        boxes1.setScaledContents(True)
        boxes1.setPixmap(self.boxIcon)
        layout.addWidget(boxes1, 0, 0, value, value)

        boxes2 = QLabel()
        boxes2.setScaledContents(True)
        boxes2.setPixmap(self.boxIcon)
        layout.addWidget(boxes2, 0, value, value, value)

        boxes3 = QLabel()
        boxes3.setScaledContents(True)
        boxes3.setPixmap(self.boxIcon)
        layout.addWidget(boxes3, value, 0, value, value)

        boxes4 = QLabel()
        boxes4.setScaledContents(True)
        boxes4.setPixmap(self.boxIcon)
        layout.addWidget(boxes4, value , value, value, value)

    def newPlantTab(self, itemName, tag):
        """
        This function adds a tab to displace the plant data.

        Parameters:
        itemName (int): The saved tab name.
        tag (widget): The tag of the list item corresponding to the current tab.
        """

        # Makes a new tab for the plant data
        newPlant = QWidget()
        newPlant.setStyleSheet("background-color: white;")
        self.infoTabs.addWidget(newPlant)
        layoutNewPlant = QGridLayout()
        newPlant.setLayout(layoutNewPlant)

        # Add the image boxes to measure and align the widgets
        self.makeBoxes(layoutNewPlant, 10)
    
        # Add to the database
        currentItem = self.plantListTab.itemWidget(tag)
        if PD.connected == True:
            PD.addToTable(currentItem.getTag(), itemName)

        # Add the label widgets
        newPlantLabel = QLabel(itemName, newPlant)
        newPlantLabel.setFont(QFont('Roboto', 20))
        newPlantLabel.setStyleSheet("color: #333333;")
        newPlantLabel.setAlignment(QtCore.Qt.AlignCenter)
        newPlantLabel.adjustSize()
        layoutNewPlant.addWidget(newPlantLabel, 1, 11, 2, 8)

        plantNameLabel = QLabel('Unknown', newPlant)
        plantNameLabel.setFont(QFont('Roboto', 20))
        plantNameLabel.setStyleSheet("color: #333333;")
        plantNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        plantNameLabel.adjustSize()
        layoutNewPlant.addWidget(plantNameLabel, 3, 11, 1, 8)
        
        plantImage = QLabel(self)
        plantImage.setScaledContents(True)
        plantImage.setPixmap(self.plantIconBW)
        plantImage.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Ignored )
        layoutNewPlant.addWidget(plantImage, 0, 0, 10, 10)

        # Add the button to upload a image
        uploadImageButton = QPushButton('Upload Image', newPlant)
        uploadImageButton.clicked.connect(lambda: self.UploadingImage(plantImage, plantNameLabel, layoutNewPlant, tag))
        layoutNewPlant.addWidget(uploadImageButton, 4, 11, 1, 8)

        # Move the add button to the top so other items can be added
        if (self.plantListTab.count() == 1):
            self.addButton.raise_()
            self.listWidget.setCurrentIndex(1)
        
    def clickedCancelButton(self):
        """
        This function is for the clear button to cancel the current add.
        """

        self.userInputName.clear()
        self.titleWidget.setCurrentIndex(0)

    def clickeditem(self):
        """
        This function is for the button on the list, it selects or deselects the current item.
        """

        if (self.plantListTab.currentRow() == self.current) or (self.current == -2):
            self.plantListTab.clearSelection()
            self.current = -1
            self.infoTabs.setCurrentIndex(0)
            self.addButton.raise_()

        else:
            self.current = self.plantListTab.currentRow()
            #print(self.plantListTab.currentItem().text())
            self.infoTabs.setCurrentIndex(self.current + 1)
            self.deleteButton.raise_()

    def clickedDeleteButton(self):
        """
        This function is for the delete button, it will delete the tab and the list item.
        """
        
        currentIndex = self.plantListTab.currentRow()
        
        currentItem = self.plantListTab.item(currentIndex)
        currentItemTag = self.plantListTab.itemWidget(currentItem).getTag()
        if PD.connected == True:
            PD.removeFromTable(currentItemTag)

        self.plantListTab.takeItem(currentIndex)
        self.current = -2
        self.clickeditem()
        self.infoTabs.removeWidget(self.infoTabs.widget(currentIndex + 1))
        if (self.plantListTab.count() == 0):
            self.listWidget.setCurrentIndex(0)

    def UploadingImage(self, imgLabel, nameLabel, layout, tag):
        """
        This function takes a image file and find the plant species using that file.

        Parameters:
        imgLabel (widget): The label to display the image on.
        nameLabel (widget): The label to display the name on.
        layout (widget): The layout used to add information to.
        tag (widget): The current selected list item corresponding to the tab.
        """

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", 
                                                    "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if fileName:
            pixmap = QPixmap(fileName)
            imgLabel.setPixmap(pixmap)
            #print(PS.plantSearch(fileName))
            plantName = PS.plantSearch(fileName)
            nameLabel.setText(plantName)
            dataDict = PLU.plantLookUp(plantName)
            currentItem = self.plantListTab.itemWidget(tag)
            currentItem.setPlant(plantName)
            if PD.connected == True:
                PD.addImageData(currentItem.getTag(), fileName)

            if dataDict == 0:
                self.nothingFound(layout)
            else:
                self.addingPlantData(dataDict, layout)
    
    def load_image(self, file_path, Qlabel):
        """
        This function takes a image file and find the plant species using that file.
    
        Parameters:
        file_path (str): The image file.
        Qlabel (widget): The label to add the image too.
        """

        pixmap = QPixmap(file_path)
        Qlabel.setPixmap(pixmap)

    def nothingFound(self, layout):
        """
        This function puts a change find label for plants it cant find.
    
        Parameters:
        layout (widget): The layout to use for displaying the cant find message.
        """
        
        plantDescription = QLabel('No plants found')
        plantDescription.setFont(QFont('Roboto', 20))
        plantDescription.setStyleSheet("color: #333333;")
        plantDescription.setAlignment(QtCore.Qt.AlignCenter)
        plantDescription.adjustSize()
        layout.addWidget(plantDescription, 14, 1, 2, 8)

    def addingPlantData(self, dict, layout):
        """
        This function displays the information provided by the API.
    
        Parameters:
        dict (dict): The dictionary to use to get the information.
        layout (widget): The layout to use for displaying the information found.
        """

        plantDescription = QLabel(dict['description'])
        plantDescription.setFont(QFont('Roboto', 8))
        plantDescription.setStyleSheet("color: #333333;")
        plantDescription.setAlignment(QtCore.Qt.AlignCenter)
        plantDescription.adjustSize()
        plantDescription.setWordWrap(True)
        layout.addWidget(plantDescription, 10, 0, 10, 10)

        plantType = QLabel("Type: " + dict['type'])
        plantType.setFont(QFont('Roboto', 8))
        plantType.setStyleSheet("color: #333333;")
        plantType.setAlignment(QtCore.Qt.AlignCenter)
        plantType.adjustSize()
        plantType.setWordWrap(True)
        layout.addWidget(plantType, 5, 11, 1, 4)

        plantCycle = QLabel("Cycle: " + dict['cycle'])
        plantCycle.setFont(QFont('Roboto', 8))
        plantCycle.setStyleSheet("color: #333333;")
        plantCycle.setAlignment(QtCore.Qt.AlignCenter)
        plantCycle.adjustSize()
        plantCycle.setWordWrap(True)
        layout.addWidget(plantCycle, 5, 15, 1, 4)

        plantWatering = QLabel("Watering: " + dict['watering'])
        plantWatering.setFont(QFont('Roboto', 8))
        plantWatering.setStyleSheet("color: #333333;")
        plantWatering.setAlignment(QtCore.Qt.AlignCenter)
        plantWatering.adjustSize()
        plantWatering.setWordWrap(True)
        layout.addWidget(plantWatering, 6, 11, 1, 4)

        plantSunlight = QLabel("Sunlight: " + dict['sunlight'][0])
        plantSunlight.setFont(QFont('Roboto', 8))
        plantSunlight.setStyleSheet("color: #333333;")
        plantSunlight.setAlignment(QtCore.Qt.AlignCenter)
        plantSunlight.adjustSize()
        plantSunlight.setWordWrap(True)
        layout.addWidget(plantSunlight, 6, 15, 1, 4)

        plantGrowthRate = QLabel("Growth Rate: " + dict['growth_rate'])
        plantGrowthRate.setFont(QFont('Roboto', 8))
        plantGrowthRate.setStyleSheet("color: #333333;")
        plantGrowthRate.setAlignment(QtCore.Qt.AlignCenter)
        plantGrowthRate.adjustSize()
        plantGrowthRate.setWordWrap(True)
        layout.addWidget(plantGrowthRate, 7, 11, 1, 4)

        plantSoil = QLabel("Soil: " + dict['soil'][0])
        plantSoil.setFont(QFont('Roboto', 8))
        plantSoil.setStyleSheet("color: #333333;")
        plantSoil.setAlignment(QtCore.Qt.AlignCenter)
        plantSoil.adjustSize()
        plantSoil.setWordWrap(True)
        layout.addWidget(plantSoil, 7, 15, 1, 4)

        plantIndoors = QLabel("Indoors: {}".format(dict['indoor']))
        plantIndoors.setFont(QFont('Roboto', 8))
        plantIndoors.setStyleSheet("color: #333333;")
        plantIndoors.setAlignment(QtCore.Qt.AlignCenter)
        plantIndoors.adjustSize()
        plantIndoors.setWordWrap(True)
        layout.addWidget(plantIndoors, 8, 11, 1, 4)

        plantMaintenance = QLabel("Maintenance: " + dict['maintenance'])
        plantMaintenance.setFont(QFont('Roboto', 8))
        plantMaintenance.setStyleSheet("color: #333333;")
        plantMaintenance.setAlignment(QtCore.Qt.AlignCenter)
        plantMaintenance.adjustSize()
        plantMaintenance.setWordWrap(True)
        layout.addWidget(plantMaintenance, 8, 15, 1, 4)

        AIInput = QLineEdit()
        AIInput.setFont(QFont('Roboto', 8))
        AIInput.setStyleSheet("color: #333333;")
        AIInput.setAlignment(QtCore.Qt.AlignCenter)
        AIInput.adjustSize()
        layout.addWidget(AIInput, 11, 11, 1, 8)
        
        askAssistant = QPushButton('Ask Assistant')
        askAssistant.clicked.connect(lambda: self.askAIAssistant(dict["common_name"] + ". Only answer questions this plant. " + AIInput.text(), outputLabel))
        layout.addWidget(askAssistant, 12, 11, 1, 8)

        outputLabel = QLabel('Nothing')
        outputLabel.setFont(QFont('Roboto', 6))
        outputLabel.setStyleSheet("color: #333333;")
        outputLabel.setAlignment(QtCore.Qt.AlignCenter)
        outputLabel.adjustSize()
        outputLabel.setWordWrap(True)
        outputLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layout.addWidget(outputLabel, 13, 11, 6, 8)

    def askAIAssistant(self, qestion, outputLabel):
        """
        This function askes the ChatGPT API a question and displays the outputed message on a label.
    
        Parameters:
        question (str): The question that is being asked.
        outputLabel (widget): The label used to display the response.
        """

        answer = AIA.AIHelp(qestion)
        outputLabel.setText(answer)    

class customListItem(QWidget):
    """
    This class is for the custom list item in the QListWidget.
    Source: https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
    Purpose: To create a custom list item.
    Adaptation: Unique ID was added, image was remove because of scaling issues.
    """

    def __init__(self, parent = None):
        """
        This function initializes the main window.
        """

        super(customListItem, self).__init__(parent)
        self.gridLayoutList = QGridLayout()
        self.nameLabel = QLabel()
        self.plantLabel = QLabel()
        self.gridLayoutList.addWidget(self.nameLabel, 0, 0)
        self.gridLayoutList.addWidget(self.plantLabel, 1, 0)
        self.setLayout(self.gridLayoutList)
        self.uniTag = random.getrandbits(128)
        self.nameLabel.setStyleSheet('color: #333333;')
        self.plantLabel.setStyleSheet('color: #333333;')
        
    def setName(self, text):
        """
        This function sets the name for the custom item.
    
        Parameters:
        text (str): The name to set.
        """

        self.nameLabel.setText(text)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)

    def setPlant(self, text):
        """
        This function sets the plant name for the custom item.
    
        Parameters:
        text (str): The plant name to set.
        """

        self.plantLabel.setText(text)
        self.plantLabel.setAlignment(QtCore.Qt.AlignCenter)

    def getTag(self):
        """
        This function gets the unique ID for the custom item.

        Returns:
        int: The Unique ID for the custom item.
        """

        return self.uniTag

def main():
    """
    This function starts up the main window.
    
    Parameters:
    None.

    Returns:
    None.
    """

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()