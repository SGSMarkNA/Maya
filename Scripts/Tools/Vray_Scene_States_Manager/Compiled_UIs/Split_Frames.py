# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\isln-smb\aw_config\Git_Live_Code\Software\Maya\Scripts\Tools\Vray_Scene_States_Manager\Split_Frames.ui'
#
# Created: Mon Dec 12 15:19:32 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(400, 467)
		self.verticalLayout = QtWidgets.QVBoxLayout(Form)
		self.verticalLayout.setObjectName("verticalLayout")
		self.splitter = QtWidgets.QSplitter(Form)
		self.splitter.setOrientation(QtCore.Qt.Vertical)
		self.splitter.setObjectName("splitter")
		self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
		self.treeWidget.setObjectName("treeWidget")
		self.treeWidget.headerItem().setText(0, "1")
		self.graphicsView = QtWidgets.QGraphicsView(self.splitter)
		self.graphicsView.setObjectName("graphicsView")
		self.verticalLayout.addWidget(self.splitter)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Form = QtWidgets.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	Form.show()
	sys.exit(app.exec_())

