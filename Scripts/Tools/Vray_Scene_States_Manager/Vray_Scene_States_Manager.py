import os
import string
import yaml
import QT
import QT.DataModels.Qt_Roles_And_Enums
import Scripts.Tools.Vray_Scene_States_Manager.Custom_Widgets
import maya.cmds as cmds
try:
	cmds.loadPlugin("vrayformaya",qt=True)
except:
	pass
if int(cmds.about(version=True)) == 2017:
	import Compiled_UIs.Vray_Scene_State_Manager
	Compiled_Vray_Scene_State_Manager = Compiled_UIs.Vray_Scene_State_Manager
else:
	import Compiled_UIs.pyside_V1.Vray_Scene_State_Manager
	Compiled_Vray_Scene_State_Manager = Compiled_UIs.pyside_V1.Vray_Scene_State_Manager
try:
	_maya_check = True
	import Scripts.UIFns.Find_UI
	import Scripts.Global_Constants.Nodes
	import Scripts.NodeCls.M_Nodes
except ImportError as  e:
	print e
	_maya_check = False
	
Custom_Widgets = Scripts.Tools.Vray_Scene_States_Manager.Custom_Widgets
Vray_Scene_State_Manager_Item_Model  =  Custom_Widgets.Vray_Scene_State_Manager_Item_Model
Qt_Roles_And_Enums   =  QT.DataModels.Qt_Roles_And_Enums
File_Dialog_Options  =  QT.DataModels.Qt_Roles_And_Enums.File_Dialog_Options
Qt        = QT.Qt
QtCore    = QT.QtCore
QtGui     = QT.QtGui
QtSlot    = QT.QtSlot
QtSignal  = QT.QtSignal
uic       = QT.uic


QT.ui_Loader.registerCustomWidget(Custom_Widgets.Render_States_List_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Part_Sets_List_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Beauty_Overide_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Invisible_Overide_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Matte_Overide_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Entity_Tree_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Asset_Tree_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Filtered_Proxy_List_View)
QT.ui_Loader.registerCustomWidget(Custom_Widgets.Standered_List_View)

# if int(cmds.about(version=True)) == 2017:
	# ui_file = os.path.realpath(os.path.dirname(__file__)+"\Vray_Scene_State_Manager.ui")
# else:
	# ui_file = os.path.realpath(os.path.dirname(__file__)+"\Vray_Scene_State_Manager.ui")
# uiform, uibase = uic.loadUiType(ui_file)

# isinstance(uiform, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)

class Render_State_Layer(object):
	
	def __init__(self, render_state):
		self.render_state = render_state
		isinstance(self.render_state, Custom_Widgets.Render_State_Item)
		self.Beauty_state    = self.render_state.Beauty
		self.Matte_state     = self.render_state.Matte
		self.Invisible_state = self.render_state.Invisible
		self.Build_Shaders()
		self.Build_Layer()
		
	def Build_Shaders(self):
		self.Beauty_Pass    = Scripts.NodeCls.M_Nodes.ShadingNode("Beauty_Pass")
		self.Matte_Pass     = Scripts.NodeCls.M_Nodes.ShadingNode("Matte_Pass")
		self.Invisible_Pass = Scripts.NodeCls.M_Nodes.ShadingNode("Invisible_Pass")
		
		self.Beauty_Pass.plug_access.outColor.setValue([1,1,1])
		self.Matte_Pass.plug_access.outColor.setValue([0,0,0])
		self.Invisible_Pass.plug_access.outColor.setValue([1.0, 0.0, 1.0])
		
		self.Beauty_Pass_SG    = Scripts.NodeCls.M_Nodes.Shading_Engine("Beauty_Pass_SG")
		self.Matte_Pass_SG     = Scripts.NodeCls.M_Nodes.Shading_Engine("Matte_Pass_SG")
		self.Invisible_Pass_SG = Scripts.NodeCls.M_Nodes.Shading_Engine("Invisible_Pass_SG")
		
		self.Beauty_Pass_SG.Assine_To_Material(self.Beauty_Pass)
		self.Matte_Pass_SG.Assine_To_Material(self.Matte_Pass)
		self.Invisible_Pass_SG.Assine_To_Material(self.Invisible_Pass)
		

	def Build_Layer(self):
		self.Render_Layer = Scripts.NodeCls.M_Nodes.RenderLayer(self.render_state.data())
		if len(self.Render_Layer.members):
			self.Render_Layer.removeMembers(self.Render_Layer.members)
		nodes = []
		for item in self.render_state.get_all_but_unassied_parts():
			isinstance(item, Custom_Widgets.Part_Set_Reference_Item)
			nodes.append(item._data.node)
		self.Render_Layer.addMembers(nodes)
		self.Render_Layer.makeCurrent()
		cmds.refresh(f=True)
		for item in self.Beauty_state.Children:
			self.Beauty_Pass_SG.addElement(item._data.node.members)
			cmds.refresh(f=True)
		for item in self.Matte_state.Children:
			self.Matte_Pass_SG.addElement(item._data.node.members)
			cmds.refresh(f=True)
		for item in self.Invisible_state.Children:
			self.Invisible_Pass_SG.addElement(item._data.node.members)
			cmds.refresh(f=True)
			
########################################################################
# uiform, QT.QMainWindow
#class Vray_Scene_States_Manager_MainWindow(uiform, QT.QMainWindow):


from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

class Vray_Scene_States_Manager_MainWindow(MayaQWidgetBaseMixin,QT.QMainWindow):
	ACTIVATE_RUN_SETUP     = QT.QtSignal(QT.QMainWindow)
	PART_SET_DELEATED      = QT.QtSignal((int,),(str,))
	PART_SET_CREATED       = QT.QtSignal((Custom_Widgets.Part_Set_Item,), (QT.QStandardItem,),(QtCore.QModelIndex,))
	RENDER_STATE_DELEATED  = QT.QtSignal((int,),(str,))
	RENDER_STATE_CREATED   = QT.QtSignal((Custom_Widgets.Render_State_Item,), (QT.QStandardItem,),(QtCore.QModelIndex,))
	ASSET_DELEATED         = QT.QtSignal((int,),(str,))
	ASSET_CREATED          = QT.QtSignal((Custom_Widgets.Asset_Item,), (QT.QStandardItem,),(QtCore.QModelIndex,))
	_Enable_Model_Editor   = False
	#----------------------------------------------------------------------
	def __init__(self, parent=None):
		isinstance(self, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)
		super(Vray_Scene_States_Manager_MainWindow,self).__init__(parent)
	#----------------------------------------------------------------------
	def _init(self):
		""""""
		self.ACTIVATE_RUN_SETUP.emit(self)
		# self.verticalGroupBox.hide()
		self.entity_tree_view.hide()
		self.isolateSelect_Button.hide()
		self.undo_stack =  QT.QUndoStack()
		
		if self._Enable_Model_Editor:
			self.part_sets_view.ITEM_MEMBERES_SELECTED.connect(self.add_Objects_To_Model_Editor)
			self.part_sets_view.ITEM_MEMBERES_DESELECTED.connect(self.remove_Objects_From_Model_Editor)
			
			self.beauty_overide_view.ITEM_MEMBERES_SELECTED.connect(self.add_Objects_To_Model_Editor)
			self.beauty_overide_view.ITEM_MEMBERES_DESELECTED.connect(self.remove_Objects_From_Model_Editor)
			
			self.matte_overide_view.ITEM_MEMBERES_SELECTED.connect(self.add_Objects_To_Model_Editor)
			self.matte_overide_view.ITEM_MEMBERES_DESELECTED.connect(self.remove_Objects_From_Model_Editor)
			
			self.invisible_overide_view.ITEM_MEMBERES_SELECTED.connect(self.add_Objects_To_Model_Editor)
			self.invisible_overide_view.ITEM_MEMBERES_DESELECTED.connect(self.remove_Objects_From_Model_Editor)
		
		self.model =  Vray_Scene_State_Manager_Item_Model(self)
		
		self.asset_item_filter_proxy_model = Custom_Widgets.Asset_Item_Filter_ProxyModel(self)
		self.asset_item_filter_proxy_model.setSourceModel(self.model)
		
		
		self.sorted_proxy_model = Custom_Widgets.Sorted_Item_Filter_ProxyModel(self)
		self.sorted_proxy_model.setSourceModel(self.model)
		self.sorted_proxy_model.setFilterCaseSensitivity(QT.Qt.CaseSensitivity.CaseInsensitive)
		self.run_Item_View_Assinments()
		#self.render_layer_helper_button.clicked.connect(self.Construct_Render_Layer_From_Render_State)
		#self.isolateSelect_Button.toggled.connect(self.isolate_Select_Render_State)
		self.render_states_view.clicked.connect(self.update_isolate_Select_Render_State)
		self.actionLoadPickle_Data = QT.QAction(self)
		self.actionLoadPickle_Data.setEnabled(True)
		self.actionLoadPickle_Data.setObjectName("actionLoadPickle_Data")
		self.actionLoadPickle_Data.setText("Load VG Data")
		self.actionLoadPickle_Data.triggered.connect(self.Construst_From_Pickle_Data)
		self.menuFile.addAction(self.actionLoadPickle_Data)
		self.Render_States_Filter_input.textChanged.connect(self.update_on_render_states_filter_Changed)
		self.Favorits_Only_checkBox.clicked.connect(self.update_on_render_states_filter_Changed)
		self.Assign_Selected_To_Matte_Parts_Button.clicked.connect(self.Multi_State_Matte_Assinment)
		self.Assign_Selected_To_Invisible_Parts_Button.clicked.connect(self.Multi_State_Invisible_Assinment)
		self.Assign_Selected_To_Beauty_Parts_Button.clicked.connect(self.Multi_State_Beauty_Assinment)
		self.Unassign_Selected_Parts_Button.clicked.connect(self.Multi_State_Unassined_Assinment)
		self.actionExport_To_Temp.triggered.connect(self.save_Yaml_Data_To_File)
		self.actionUpdate_From_Temp.triggered.connect(self.update_States_From_File)
		isinstance(self, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)
		self.asset_tree_view.selected_Items
		if cmds.objExists("VG_Model_BuilderScriptNode"):
			self.actionDumpPickle_Data = QT.QAction(self)
			self.actionDumpPickle_Data.setEnabled(True)
			self.actionDumpPickle_Data.setObjectName("actionDumpPickle_Data")
			self.actionDumpPickle_Data.setText("Dumb VG Data")
			self.actionDumpPickle_Data.triggered.connect(self.Extract_To_Pickle_Data)
			self.menuFile.addAction(self.actionDumpPickle_Data)
		if _maya_check:
			self.Script_Data = Custom_Widgets.Yaml_Config_Data.find_yaml_config_scripts()
			cmds.scriptJob(killWithScene=True, event=['SceneSaved',self.Save])
		self.Multi_State_Mode_Button.click()
		self.Multi_State_Mode_Button.click()
	@QT.QtSlot(bool)
	#----------------------------------------------------------------------
	def Toggle_Multi_State_Mode(self,val):
		""""""
		if val:
			isinstance(self, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)
			
			self.render_states_view.setSelectionMode(QT.QAbstractItemView.ExtendedSelection)
			self.render_states_view.setDragDropMode(QT.QAbstractItemView.NoDragDrop)
			
		else:
			self.render_states_view.setSelectionMode(QT.QAbstractItemView.SingleSelection)
			self.render_states_view.setDragDropMode(QT.QAbstractItemView.DragDrop)
			
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def update_on_render_states_filter_Changed(self):
		text = self.Render_States_Filter_input.text()
		if not text.endswith("*"):
			text += "*"
		self.sorted_proxy_model.setFilterWildcard(text)
	#----------------------------------------------------------------------
	@QT.QtSlot(list)
	def remove_Objects_From_Model_Editor(self, objs):
		self.Model_Editor.remove_Objects_From_Main_Connection(objs)
	#----------------------------------------------------------------------
	@QT.QtSlot(list)
	def add_Objects_To_Model_Editor(self, objs):
		self.Model_Editor.add_Objects_To_Main_Connection(objs)
		
	#----------------------------------------------------------------------
	def run_Item_View_Assinments(self):
		self.sorted_proxy_model = Custom_Widgets.Sorted_Item_Filter_ProxyModel(self)
		self.sorted_proxy_model.setSourceModel(self.model)
		self.model.run_Vray_States_Setup()
		self.entity_tree_view.setModel(self.model)
		self.All_Part_Sets_List.setModel(self.model)
		self.asset_tree_view.setModel(self.asset_item_filter_proxy_model)
		self.render_states_view.setModel(self.sorted_proxy_model)
		self.part_sets_view.setModel(self.sorted_proxy_model)
		self.invisible_overide_view.setModel(self.sorted_proxy_model)
		self.beauty_overide_view.setModel(self.sorted_proxy_model)
		self.matte_overide_view.setModel(self.sorted_proxy_model)
		self.asset_tree_view.set_Root_Item(self.model.Assets)
		
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def _update_on_Asset_Selection_Changed(self):
		isinstance(self, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)
		items = self.asset_tree_view.selected_Items()
		if len(items):
			self.All_Part_Sets_List.setRootIndex(items[0].Part_Sets.index())
	###----------------------------------------------------------------------
	##def contextMenuEvent(self, event):
		##menu = QT.QMenu(self)
		##menu.addAction(self.actionAdd_Part_Set)
		##menu.addAction(self.actionAdd_Render_State)
		##menu.exec_(event.globalPos())
	#----------------------------------------------------------------------
	def Assine_Part_Set_Refs_To_Overide_State(self,overide_state,items):
		""""""
		for item in items:
			if not overide_state.data() == item.get_Overide_assinment().data():
				item.parent().removeRow(item.row())
				overide_state.appendRow(item)
	#----------------------------------------------------------------------
	def Assine_Part_Sets_To_Selected_Render_States_Overide(self,overide_state):
		""""""
		isinstance(self, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)
		set_names = [item.data() for item in self.All_Part_Sets_List.selected_Items()]
		for render_state in self.render_states_view.selected_Items():
			isinstance(render_state,Custom_Widgets.Render_State_Item)
			if overide_state == "b":
				overide_item = render_state.Beauty
			elif overide_state == "m":
				overide_item = render_state.Matte
			elif overide_state == "i":
				overide_item = render_state.Invisible
			else:
				overide_item = render_state.Unassined
			all_refs = []
			for name in set_names:
				for part in render_state.Beauty_Parts + render_state.Matte_Parts + render_state.Invisible_Parts + render_state.Unassined_Parts:
					if part.data() == name:
						all_refs.append(part)
						break
			self.Assine_Part_Set_Refs_To_Overide_State(overide_item, all_refs)
			
	#----------------------------------------------------------------------
	def Multi_State_Beauty_Assinment(self):
		""""""
		self.Assine_Part_Sets_To_Selected_Render_States_Overide("b")
	#----------------------------------------------------------------------
	def Multi_State_Matte_Assinment(self):
		""""""
		self.Assine_Part_Sets_To_Selected_Render_States_Overide("m")
	#----------------------------------------------------------------------
	def Multi_State_Invisible_Assinment(self):
		""""""
		self.Assine_Part_Sets_To_Selected_Render_States_Overide("i")
	#----------------------------------------------------------------------
	def Multi_State_Unassined_Assinment(self):
		""""""
		self.Assine_Part_Sets_To_Selected_Render_States_Overide("u")
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def undo_it(self):
		self.undo_stack.undo()

	#----------------------------------------------------------------------
	@QT.QtSlot()
	def redo_it(self):
		self.undo_stack.redo()

	#----------------------------------------------------------------------
	@QT.QtSlot()
	def reset_Item_View(self):
		asset        = self.model.Assets.child(0)
		render_state = asset.Render_States.child(0)
		self.asset_tree_view.set_Root_Item(self.model.Assets)
		self.asset_tree_view.set_Current_Item(asset)
		
	#----------------------------------------------------------------------
	@QT.QtSlot()
	@QT.QtSlot(str)
	def add_Part_Set(self, name=None):
		return self.asset_tree_view.add_New_Part_Set(name=name)
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Remove_Selected_Part_Sets(self):
		self.asset_tree_view.delete_Selected_Part_Sets()
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Remove_Empty_Part_Sets(self):
		check = cmds.confirmDialog( title='Remove Empty Part Sets', message='Do to a memory sync issue between the Scene States Innerface and maya undo cash.\nPreforming this operation will also flush the undo cash.\nSo you will not be able to undo past this point\nDo you Want To Continue', button=['yes','no'], defaultButton='no', cancelButton='no', dismissString='no', icon="warning")
		if check == "yes":
			self.asset_tree_view.delete_Empty_Part_Sets()
			cmds.flushUndo() 
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Remove_Selected_Render_States(self):
		self.asset_tree_view.delete_Selected_Render_States()

	#----------------------------------------------------------------------
	@QT.QtSlot()
	@QT.QtSlot(str)
	def add_Asset(self, name=None,subAsset=False):
		self.asset_tree_view.add_New_Asset(name=name, subAsset=subAsset)
		item = self.model.Assets.Children[-1]
		self.asset_tree_view.set_Current_Item(item)
		isinstance(item, Custom_Widgets.Asset_Item)
		return item
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Remove_Selected_Assets(self):
		self.asset_tree_view.delete_Selected_Assets()


	#----------------------------------------------------------------------
	@QT.QtSlot()
	@QT.QtSlot(str)
	def add_Child_Asset(self, name=None):
		self.asset_tree_view.add_New_Asset(name=name, subAsset=True)
	#----------------------------------------------------------------------
	@QT.QtSlot()
	@QT.QtSlot(str)
	def add_Render_State(self, name=None):
		return self.asset_tree_view.add_New_Render_State(name=name)
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def open_File(self,filePath=None):
		""""""
		if _maya_check:
			self.Load_Temp_yaml()
			#self.model.from_Yaml()
			#self.Update_On_Render_State_Selection_Changed(self.model.Render_States.child(0).index())
			#self.undo_stack.clear()
	#----------------------------------------------------------------------
	def save_Yaml_Data_To_File(self,filePath=None):
		""""""
		if _maya_check:
			if filePath is None:
				filePath = os.path.join(os.environ["Temp"],"Temp_State_Manager_Data.yaml")
			data = self.model.to_Yaml_Object()
			Custom_Widgets.Yaml_Config_Data.save_config_data_to_file(data, filePath)
	#----------------------------------------------------------------------
	def open_Yaml_Data_From_File(self,filePath=None):
		""""""
		if _maya_check:
			if filePath is None:
				filePath = os.path.join(os.environ["Temp"],"Temp_State_Manager_Data.yaml")
			data = Custom_Widgets.Yaml_Config_Data.load_config_data_from_file(filePath)
			return data
	#----------------------------------------------------------------------
	def update_States_From_File(self,filePath=None):
		""""""
		new_yaml_data     = self.open_Yaml_Data_From_File(filePath)
		current_yaml_data = self.model.to_Yaml_Object()
		differences_data = Custom_Widgets.Yaml_Config_Data.Yaml_Differences_Data(current_yaml_data, new_yaml_data)
		output_Log = ""
		
		output_Log += "New Render States \n"
		
		for added_state in differences_data.added_render_states:
			
			output_Log += "\t{}\n".format(added_state.name)
			
			found_states = self.model.Assets.find_Render_States_By_Name(added_state.name)
			
			if not len(found_states):
				new_state = self.add_Render_State(added_state.name)
			else:
				new_state = found_states[0]
			
			added_state_containers = [added_state.Beauty,added_state.Matte,added_state.Invisible]
			new_state_containers   = [new_state.Beauty,new_state.Matte,new_state.Invisible]
			
			for added_state_container,new_state_container in zip(added_state_containers,new_state_containers):
				refs = []
				for link in added_state_container.links:
					child_search = new_state.Unassined.find_child_items(link.name)
					if len(child_search):
						child = child_search[0]
						refs.append(child)
				if len(refs):
					cmd = Custom_Widgets.Reparent_Items_Command(new_state_container, refs)
					self.undo_stack.push(cmd)
		
		output_Log += "\n"
		output_Log += "Render State Changes\n"
		output_Log += "\n"
		for changed_state in differences_data.render_state_Changes:
			
			found_states = self.model.Assets.find_Render_States_By_Name(changed_state)
		
			if len(found_states):
				
				output_Log += "\t{}\n".format(changed_state)
				
				render_state       = found_states[0]
				changed_state_data = differences_data.render_state_Changes[changed_state]
				Beauty_changes     = changed_state_data["Beauty"]
				Matte_changes      = changed_state_data["Matte"]
				Invisible_changes  = changed_state_data["Invisible"]
				container_names    = ["Beauty","Matte","Invisible"]
				change_containers  = [Beauty_changes,Matte_changes,Invisible_changes]
				state_containers   = [render_state.Beauty,render_state.Matte,render_state.Invisible]
		
			for change_container,state_container,container_name in zip(change_containers,state_containers,container_names):
				added_parts   = change_container['Added']
				removed_parts = change_container['Removed']
		
				added_ref   = []
				removed_ref = []
		
				for part in added_parts:
					child_search = render_state.Unassined.find_child_items(part.name)
					if len(child_search):
						child = child_search[0]
						added_ref.append(child)
		
				for part in removed_parts:
					child_search = state_container.find_child_items(part.name)
					if len(child_search):
						child = child_search[0]
						removed_ref.append(child)
		
				if len(added_ref):
					
					output_Log += "\t\tAdded Part Sets To {} State\n".format(container_name)
					for part in added_ref:
						output_Log += "\t\t\t{}\n".format(part.Text)
						
					cmd = Custom_Widgets.Reparent_Items_Command(state_container, added_ref)
					self.undo_stack.push(cmd)
		
				if len(removed_ref):
					output_Log += "\t\tRemoved Part Sets From {} State\n".format(container_name)
					for part in removed_ref:
						output_Log += "\t\t\t{}\n".format(part.Text)
						
					cmd = Custom_Widgets.Reparent_Items_Command(render_state.Unassined, removed_ref)
					self.undo_stack.push(cmd)
				output_Log += "\n"
		print(output_Log)
	#----------------------------------------------------------------------
	def show(self):
		super(Vray_Scene_States_Manager_MainWindow, self).show()
		if self._Enable_Model_Editor:
			self.Model_Editor.m_editor.widget.show()
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Save(self):
		self.model.scan_for_Master_Render_States()
		for asset in self.model.Assets.find_child_item_types(Custom_Widgets.Asset_Item.ITEM_TYPE):
			isinstance(asset, Custom_Widgets.Asset_Item)
			asset.Update_Enum_Render_States()
		data = self.model.to_Yaml_Object()
		self.Script_Data.save_Config_Data(data)
		
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Load(self):
		if _maya_check:
			data = self.Script_Data.load_Config_Data()
			if data != None:
				self.model.from_Yaml_Object(data)
				self.reset_Item_View()
				self.undo_stack.clear()
				self.sorted_proxy_model.sort()
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Construct_From_Display_Layers(self):
		if _maya_check:
			
			layers = Scripts.Global_Constants.Nodes.Display_Layers()
			if self.model.Assets.RowCount:
				asset = self.asset_tree_view.current_item()
			else:
				asset = self.add_Asset(name="Display_Layers_Asset", subAsset=False)
			
			for layer in layers:
				make_it = False
				isinstance(layer, Scripts.NodeCls.M_Nodes.DisplayLayer)
				name = layer.name + "_set"
				if not asset.child_item_exists(name):
					if layer.attributeExists("partSetLink"):
						ps_lnk = layer.Make_Plug("partSetLink")
						if not ps_lnk.value is None:
							if not asset.child_item_exists(ps_lnk.value.name):
								make_it = True
						else:
							make_it = True
					else:
						make_it = True
					
				if make_it:
					self.asset_tree_view.add_New_Part_Set(name=name)
					part = self.model.Assets.find_Part_Sets_By_Name(name)[0]
					part._data.unlockNode()
					asset.node_addNode([part.node])
					part.node_include_items(layer.members)
					part._data.lockNode()
	@QT.QtSlot()
	def sync_Display_Layers(self):
		for dl in Scripts.Global_Constants.Nodes.Display_Layers():
			isinstance(dl, Scripts.NodeCls.M_Nodes.DisplayLayer)
			ps_link = dl.Add_Simple_Attribute("partSetLink", 'message', shortName="pslnk", hidden=False, writable=True, readable=True, storable=True, keyable=False)
			if cmds.objExists(dl.nice_name+"_set"):
				if not ps_link.value is None:
					vrop = Scripts.NodeCls.M_Nodes.VRayObjectProperties(ps_link.value.name)
					vrop.unlockNode()
					if not vrop.attributeExists("displayLayerLink"):
						dl_link = vrop.Add_Simple_Attribute("displayLayerLink", 'message', shortName="dllnk", hidden=False, writable=True, readable=True, storable=True, keyable=False)
					else:
						dl_link = vrop.Make_Plug("displayLayerLink")
				else:
					vrop = Scripts.NodeCls.M_Nodes.VRayObjectProperties(dl.nice_name+"_set")
					vrop.unlockNode()
					dl_link = vrop.Add_Simple_Attribute("displayLayerLink", 'message', shortName="dllnk", hidden=False, writable=True, readable=True, storable=True, keyable=False)
				vrop.unlockNode()
				ps_link.Simple_Connect(dl_link)
				if len(dl.members):
					vrop.addElement(dl.members)
				vrop.lockNode()
	#----------------------------------------------------------------------
	def Construct_Render_Layer_From_Render_State(self):
		item = self.render_states_view.current_item()
		Render_State_Layer(item)
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Extract_To_Pickle_Data(self):
		""""""
		import Vg_EMI_Data_Extractor
		Vg_EMI_Data_Extractor.dump_EIM_Data()
	
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Construst_Honda_Rebuild_Data(self):
		""""""
		if len(cmds.ls("*.hondaRebuildData")):
			import Honda_Data_Parser
		data = Honda_Data_Parser.build_Honda_MetaData()
		for layer in data.trims.nodes:
			if not cmds.objExists(layer.display_layer_name):
				possable_options = [check for check in cmds.ls(typ="displayLayer") if layer.lower() in check.lower()]
				cmds.inViewMessage( statusMessage='<hl>Can Not Reconstruct From Pickle Data\nBecause The Following Display Layer\nWas Not Found In The Scene\n"%s".' % (layer), fadeInTime=200, fadeOutTime=1000, fadeStayTime=3000,fontSize=20, pos='midCenter', fade=True )
				cmds.error('Can Not Reconstruct From Pickle Data Because The Following Display Layer "%s" Was Not Found In The Scene\n possable options %s".' % (layer, ",".join(possable_options)) )
				return
		
		self.Construct_From_Display_Layers()
		self.sync_Display_Layers()
		if len(self.asset_tree_view.selected_Items()):
			asset_item = self.asset_tree_view.selected_Items()[0]
		else:
			asset_item = self.model.Assets.Children[0]
		isinstance(asset_item, Custom_Widgets.Assets_Item)
		for item in data.trims.collections:
			isinstance(item, Honda_Data_Parser.Honda_Metadata_Trim_Collection)
			if not item.eim_name.startswith("_RESET_ON"):
				self.add_Render_State(name=item.eim_name)
				# for rs in asset_item.Render_States.Children:
				render_state = asset_item.Render_States.Children[-1]
				isinstance(render_state, Custom_Widgets.Render_State_Item)
				found_items = []
				for name in item.get_Assigned_Display_Layers():
					for ref in render_state.Unassined.Children:
						try:
							if ref._data.node.assinedDisplayLayer == name:
								found_items.append(ref)
								break
						except:
							pass
			cmd = Custom_Widgets.Reparent_Items_Command(render_state.Beauty, found_items)
			self.undo_stack.push(cmd)
		# for rs in asset_item.Render_States.Children:
			# for i, bp in enumerate(rs.Beauty.Children):
				# if bp is not None:
					# if bp.type() == 0:
						# rs.Beauty.removeRow(bp.row())
		self.sorted_proxy_model.sort()
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def Construst_From_Pickle_Data(self):
		""""""
		import Vg_EMI_Data_Extractor
		data = Vg_EMI_Data_Extractor.load_EIM_Data()
		for item in data:
			for layer in item.layers:
				if not cmds.objExists(layer):
					possable_options = [check for check in cmds.ls(typ="displayLayer") if layer.lower() in check.lower()]
					cmds.inViewMessage( statusMessage='<hl>Can Not Reconstruct From Pickle Data\nBecause The Following Display Layer\nWas Not Found In The Scene\n"%s".' % (layer), fadeInTime=200, fadeOutTime=1000, fadeStayTime=3000,fontSize=20, pos='midCenter', fade=True )
					cmds.error('Can Not Reconstruct From Pickle Data Because The Following Display Layer "%s" Was Not Found In The Scene\n possable options %s".' % (layer, ",".join(possable_options)) )
					return
		
		self.Construct_From_Display_Layers()
		self.sync_Display_Layers()
		if len(self.asset_tree_view.selected_Items()):
			asset_item = self.asset_tree_view.selected_Items()[0]
		else:
			asset_item = self.model.Assets.Children[0]
		isinstance(asset_item, Custom_Widgets.Assets_Item)
		for item in data:
			isinstance(item, Vg_EMI_Data_Extractor.EIM_Config_Data)
			# self.actionAdd_Render_State.trigger()
			self.add_Render_State(name=item.code)
			# for rs in asset_item.Render_States.Children:
			render_state = asset_item.Render_States.Children[-1]
			isinstance(render_state, Custom_Widgets.Render_State_Item)
			found_items = []
			for name in item.layers:
				for ref in render_state.Unassined.Children:
					try:
						if ref._data.node.assinedDisplayLayer == name:
							found_items.append(ref)
							break
					except:
						pass
			cmd = Custom_Widgets.Reparent_Items_Command(render_state.Beauty, found_items)
			self.undo_stack.push(cmd)
		# for rs in asset_item.Render_States.Children:
			# for i, bp in enumerate(rs.Beauty.Children):
				# if bp is not None:
					# if bp.type() == 0:
						# rs.Beauty.removeRow(bp.row())
		self.sorted_proxy_model.sort()
	@QT.QtSlot()
	#----------------------------------------------------------------------
	def Apply_Current_State_To_Diaplay_Layers(self):
		item = self.render_states_view.current_item()
		isinstance(item, Custom_Widgets.Render_State_Item)
		for part in item.Beauty_Parts:
			if not part._data.node.assinedDisplayLayer == 'defaultLayer':
				cmds.setAttr(part._data.node.assinedDisplayLayer+".visibility",1)
		for part in item.Invisible_Parts:
			if not part._data.node.assinedDisplayLayer == 'defaultLayer':
				cmds.setAttr(part._data.node.assinedDisplayLayer+".visibility",1)
		for part in item.Matte_Parts:
			if not part._data.node.assinedDisplayLayer == 'defaultLayer':
				cmds.setAttr(part._data.node.assinedDisplayLayer+".visibility",1)
		for part in item.Unassined_Parts:
			if not part._data.node.assinedDisplayLayer == 'defaultLayer':
				cmds.setAttr(part._data.node.assinedDisplayLayer+".visibility",0)
	@QT.QtSlot()
	#----------------------------------------------------------------------
	def Show_All_Diaplay_Layers(self):
		for layer in Scripts.Global_Constants.Nodes.Display_Layers():
			isinstance(layer, Scripts.NodeCls.M_Nodes.DisplayLayer)
			layer.visibility.value = 1
	#----------------------------------------------------------------------	
	@QT.QtSlot(bool)
	def isolate_Select_Render_State(self, state):
		model_pan = cmds.getPanel(withLabel="Persp View")
		try:
			if state:
				current_selection = cmds.ls(sl=True)
				render_state = self.render_states_view.current_item()
				if render_state is None:
					cmds.headsUpMessage("Can not isolateing Please Select A Render State")
				else:
					members = render_state.get_all_but_unassied_node_members()
					cmds.isolateSelect( model_pan, state=False )
					cmds.select(clear=True)
					if len(members):
						cmds.select(members)
						cmds.isolateSelect( model_pan, state=state )
						cmds.isolateSelect( model_pan, addSelected=True )
					else:
						cmds.isolateSelect( model_pan, state=True )
						
					if len(current_selection):
						cmds.select(current_selection)
					else:
						cmds.select(clear=True)
			else:
				cmds.isolateSelect( model_pan, state=state )
		except:
			cmds.headsUpMessage("had a problem isolateing Could Not Panel withLabel Persp View")
		
	#----------------------------------------------------------------------
	@QT.QtSlot()
	def update_isolate_Select_Render_State(self):
		if self.isolateSelect_Button.isChecked():
			self.isolate_Select_Render_State(True)
	#----------------------------------------------------------------------
	def Create_Render_States_From_Name_List(self,names=[]):
		current_item = self.asset_tree_view.current_item()
		if current_item is not None:
			for name in names:
				found_items = current_item.find_Render_States_By_Name(name)
				if not len(found_items):
					self.add_Render_State(name=name)
	#----------------------------------------------------------------------
	def Create_Render_States_From_Assembly_Assets(self,items=[]):
		current_item = self.asset_tree_view.current_item()
		if current_item is not None:
			for item in items:
				found_items = current_item.find_Render_States_By_Name(item.name)
				if not len(found_items):
					#if item._vray_state_id_ref != None:
						#found_items = current_item.find_Child_By_UUID(item._vray_state_id_ref)
						#if len(found_items):
							#if not isinstance(found_items[0],Custom_Widgets.Render_State_Item):
								#found_items = []
					if not len(found_items):
						found_items = current_item.find_Render_States_By_asset_assembly_ref(item._excel_id_ref,item.__class__.__name__)
					if not len(found_items):
						new_item = self.add_Render_State(name=item.name)
						isinstance(new_item,Custom_Widgets.Render_State_Item)
						new_item.asset_assembly_ref_id   = item._excel_id_ref
						new_item.asset_assembly_ref_type = item.__class__.__name__
						#item._vray_state_id_ref = new_item.uid
						#item._scene_state_render_state_id = new_item.uid
						#item._scene_state_render_state_item = new_item
				if len(found_items):
					f_item = found_items[0]
					f_item.asset_assembly_ref_id   = item._excel_id_ref
					f_item.asset_assembly_ref_type = item.__class__.__name__
					#item._vray_state_id_ref = f_item.uid
					#item._scene_state_render_state_id = f_item.uid
					#item._scene_state_render_state_item = f_item
					f_item.setData(item.name)
	#----------------------------------------------------------------------
	def Create_Part_Sets_From_Name_List(self,names=[]):
		current_item = self.asset_tree_view.current_item()
		if current_item is not None:
			for name in names:
				found_items = current_item.find_Part_Sets_By_Name(name)
				if not len(found_items):
					self.add_Part_Set(name=name)
	#----------------------------------------------------------------------
	def Create_Part_Sets_From_Assembly_Assets(self,items=[]):
		current_item = self.Get_Active_Asset()
		if current_item is not None:
			for item in items:
				found_items = current_item.find_Part_Sets_By_Name(item.name+"_set")
				if not len(found_items):
					#if item._vray_state_id_ref != None:
						#found_items = current_item.find_Child_By_UUID(item._vray_state_id_ref)
						#if len(found_items):
							#if not isinstance(found_items[0],Custom_Widgets.Part_Set_Item):
								#found_items = []
					if not len(found_items):
						found_items = current_item.find_Part_Sets_By_asset_assembly_ref(item._excel_id_ref,item.__class__.__name__)
						
					if not len(found_items):
						new_item = self.add_Part_Set(name=item.name+"_set")
						isinstance(new_item,Custom_Widgets.Render_State_Item)
						new_item.asset_assembly_ref_id   = item._excel_id_ref
						new_item.asset_assembly_ref_type = item.__class__.__name__
						#item._vray_state_id_ref = new_item.uid
						#item._scene_state_part_set_id = new_item.uid
						#item._scene_state_part_set_item = new_item
				if len(found_items):
					f_item = found_items[0]
					f_item.asset_assembly_ref_id   = item._excel_id_ref
					f_item.asset_assembly_ref_type = item.__class__.__name__
					#item._vray_state_id_ref = f_item.uid
					#item._scene_state_part_set_id = f_item.uid
					#item._scene_state_part_set_item = f_item
					f_item.setData(item.name)
	#----------------------------------------------------------------------
	def Assine_Part_Set_Refs_To_Render_State_Overide(self, render_state_names, part_set_names,overide_state):
		""""""
		if isinstance(render_state_names,basestring):
			render_state_names = [render_state_names]
			
			current_item = self.asset_tree_view.current_item()
			if current_item is not None:
				render_states = []
				for render_state_name in render_state_names:
					found_items = current_item.find_Render_States_By_Name(render_state_name)
					if len(found_items):
						render_states.append(found_items[0])
	
				if len(render_states):
					overide_state = overide_state.lower()
	
					if len(overide_state):
						overide_state = overide_state[0]
	
					for render_state in render_states:
						if overide_state == "b":
							overide_item = render_state.Beauty
						elif overide_state == "m":
							overide_item = render_state.Matte
						elif overide_state == "i":
							overide_item = render_state.Invisible
						elif overide_state == "u":
							overide_item = render_state.Unassined
						else:
							overide_item = None
							continue
	
						part_sets = []
						for part_set_name in part_set_names:
							found_items = render_state.find_child_items(part_set_name)
							if len(found_items):
								part_sets.append(found_items[0])
	
						if len(part_sets):
							for part_set in part_sets:
								if not overide_item.data() == part_set.get_Overide_assinment().data():
									part_set.parent().removeRow(part_set.row())
									overide_item.appendRow(part_set)
	#----------------------------------------------------------------------
	def Assine_Part_Set_Refs_To_Overide_State(self,overide_state,items):
		""""""
		for item in items:
			if not overide_state.data() == item.get_Overide_assinment().data():
				item.parent().removeRow(item.row())
				overide_state.appendRow(item)
	#----------------------------------------------------------------------
	def Get_Active_Asset_Render_States(self):
		current_item = self.asset_tree_view.current_item()
		if current_item is not None:
			return current_item.Render_States.Children
		else:
			return []
	#----------------------------------------------------------------------
	def Get_Active_Asset(self):
		current_item = self.asset_tree_view.current_item()
		isinstance(current_item,Custom_Widgets.Asset_Item)
		return current_item
QT.ui_Loader.registerCustomWidget(Vray_Scene_States_Manager_MainWindow)

States_Manager = None
isinstance(States_Manager, Compiled_Vray_Scene_State_Manager.Ui_Vray_Scene_State_Manager)
isinstance(States_Manager, Vray_Scene_States_Manager_MainWindow)


def make_ui():
	global States_Manager, _remove_manager_job_id
	if States_Manager == None:
		States_Manager = QT.ui_Loader.load(os.path.join( os.path.dirname(__file__), "Vray_Scene_State_Manager.ui") )
		States_Manager._init()
		#States_Manager = Vray_Scene_States_Manager_MainWindow()
		States_Manager.show()
		States_Manager.move(200,100)
		States_Manager.Load()
		_remove_manager_job_id = cmds.scriptJob(runOnce=True, event= ["deleteAll",remove_manager])
	else:
		States_Manager.show()
	return States_Manager

def remove_manager():
	global States_Manager
	States_Manager.hide()
	check = States_Manager._Enable_Model_Editor
	States_Manager.setParent(None)
	States_Manager = None	
	#del States_Manager
	if check:
		cmds.deleteUI("MyModelEditor", editor = True)
