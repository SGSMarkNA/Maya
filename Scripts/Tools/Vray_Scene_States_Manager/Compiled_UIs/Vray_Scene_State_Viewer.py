# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\isln-smb\aw_config\Git_Live_Code\Software\Maya\Scripts\Tools\Vray_Scene_States_Manager\Vray_Scene_State_Viewer.ui'
#
# Created: Mon Dec 12 15:19:32 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Vray_Scene_States_Viewer(object):
	def setupUi(self, Vray_Scene_States_Viewer):
		Vray_Scene_States_Viewer.setObjectName("Vray_Scene_States_Viewer")
		Vray_Scene_States_Viewer.resize(504, 646)
		self.centralwidget = QtWidgets.QWidget(Vray_Scene_States_Viewer)
		self.centralwidget.setObjectName("centralwidget")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.Update_Button = QtWidgets.QPushButton(self.centralwidget)
		self.Update_Button.setObjectName("Update_Button")
		self.verticalLayout_3.addWidget(self.Update_Button)
		self.rebuild_Render_layer_states_button = QtWidgets.QPushButton(self.centralwidget)
		self.rebuild_Render_layer_states_button.setObjectName("rebuild_Render_layer_states_button")
		self.verticalLayout_3.addWidget(self.rebuild_Render_layer_states_button)
		self.Asset_Grid_groupBox = QtWidgets.QGroupBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Asset_Grid_groupBox.sizePolicy().hasHeightForWidth())
		self.Asset_Grid_groupBox.setSizePolicy(sizePolicy)
		self.Asset_Grid_groupBox.setMinimumSize(QtCore.QSize(0, 100))
		self.Asset_Grid_groupBox.setObjectName("Asset_Grid_groupBox")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Asset_Grid_groupBox)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.Asset_Grid_widget = Asset_Grid(self.Asset_Grid_groupBox)
		self.Asset_Grid_widget.setBaseSize(QtCore.QSize(0, 100))
		self.Asset_Grid_widget.setObjectName("Asset_Grid_widget")
		self.verticalLayout_2.addWidget(self.Asset_Grid_widget)
		self.verticalLayout_3.addWidget(self.Asset_Grid_groupBox)
		self.entity_tree_view = Asset_Tree_View(self.centralwidget)
		self.entity_tree_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.entity_tree_view.setObjectName("entity_tree_view")
		self.verticalLayout_3.addWidget(self.entity_tree_view)
		Vray_Scene_States_Viewer.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(Vray_Scene_States_Viewer)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 504, 26))
		self.menubar.setObjectName("menubar")
		Vray_Scene_States_Viewer.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(Vray_Scene_States_Viewer)
		self.statusbar.setObjectName("statusbar")
		Vray_Scene_States_Viewer.setStatusBar(self.statusbar)

		self.retranslateUi(Vray_Scene_States_Viewer)
		QtCore.QMetaObject.connectSlotsByName(Vray_Scene_States_Viewer)

	def retranslateUi(self, Vray_Scene_States_Viewer):
		Vray_Scene_States_Viewer.setWindowTitle(QtWidgets.QApplication.translate("Vray_Scene_States_Viewer", "MainWindow", None, -1))
		self.Update_Button.setText(QtWidgets.QApplication.translate("Vray_Scene_States_Viewer", "Update To Version 2", None, -1))
		self.rebuild_Render_layer_states_button.setText(QtWidgets.QApplication.translate("Vray_Scene_States_Viewer", "Rebuild Render Layer States", None, -1))
		self.Asset_Grid_groupBox.setTitle(QtWidgets.QApplication.translate("Vray_Scene_States_Viewer", "Asset Grid", None, -1))

from Scripts.Tools.Vray_Scene_States_Manager.Custom_Widgets import Asset_Grid, Asset_Tree_View

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Vray_Scene_States_Viewer = QtWidgets.QMainWindow()
	ui = Ui_Vray_Scene_States_Viewer()
	ui.setupUi(Vray_Scene_States_Viewer)
	Vray_Scene_States_Viewer.show()
	sys.exit(app.exec_())

