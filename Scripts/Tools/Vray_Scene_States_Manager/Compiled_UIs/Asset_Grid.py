# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\isln-smb\aw_config\Git_Live_Code\Software\Maya\Scripts\Tools\Vray_Scene_States_Manager\Asset_Grid.ui'
#
# Created: Mon Dec 12 15:19:32 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(399, 77)
		self.gridLayout = QtWidgets.QGridLayout(Form)
		self.gridLayout.setObjectName("gridLayout")
		self.frame = QtWidgets.QFrame(Form)
		self.frame.setFrameShape(QtWidgets.QFrame.Box)
		self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
		self.frame.setObjectName("frame")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
		self.verticalLayout.setObjectName("verticalLayout")
		self.asset_name_label = QtWidgets.QLabel(self.frame)
		self.asset_name_label.setAlignment(QtCore.Qt.AlignCenter)
		self.asset_name_label.setObjectName("asset_name_label")
		self.verticalLayout.addWidget(self.asset_name_label)
		self.asset_states_comboBox = QtWidgets.QComboBox(self.frame)
		self.asset_states_comboBox.setObjectName("asset_states_comboBox")
		self.verticalLayout.addWidget(self.asset_states_comboBox)
		self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
		self.frame_2 = QtWidgets.QFrame(Form)
		self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
		self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
		self.frame_2.setObjectName("frame_2")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.asset_name_label_2 = QtWidgets.QLabel(self.frame_2)
		self.asset_name_label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.asset_name_label_2.setObjectName("asset_name_label_2")
		self.verticalLayout_2.addWidget(self.asset_name_label_2)
		self.asset_states_comboBox_2 = QtWidgets.QComboBox(self.frame_2)
		self.asset_states_comboBox_2.setObjectName("asset_states_comboBox_2")
		self.verticalLayout_2.addWidget(self.asset_states_comboBox_2)
		self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
		self.asset_name_label.setText(QtWidgets.QApplication.translate("Form", "Asset Name", None, -1))
		self.asset_name_label_2.setText(QtWidgets.QApplication.translate("Form", "Asset Name", None, -1))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Form = QtWidgets.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	Form.show()
	sys.exit(app.exec_())

