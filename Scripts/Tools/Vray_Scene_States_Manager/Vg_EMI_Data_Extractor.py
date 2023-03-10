import pickle
import os
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mm
import xml.etree.ElementTree as etree
import Coba_Data_Parser
import Coba_Json_Data_Parser
class EIM_Config_Data(object):
	def __init__(self, code, layers):
		self.code = code
		self.layers = layers

#----------------------------------------------------------------------
def Get_JSON_EMI_Data():
	""""""
	json_config_data = Coba_Json_Data_Parser.Json_Config_Data()
	pickle_file            = os.path.join(os.environ["temp"],"EMI_BUILD_DATA.pkl")
	pickle_Data            = list()
	for eim_build in json_config_data.Eim_Builds:
		isinstance(eim_build,Coba_Json_Data_Parser.EIM)
		config_data=dict(code=eim_build.name,dls=eim_build.get_layer_names(),rls=[])
		pickle_Data.append(config_data)
	with file(pickle_file,'w') as pkf:
		pickle.dump(pickle_Data,pkf)

#----------------------------------------------------------------------
def Get_XML_EMI_Data():
	""""""
	root = Coba_Data_Parser.Xml_From_Script(script="VGConfigXMLScriptNode")
	pickle_file            = os.path.join(os.environ["temp"],"EMI_BUILD_DATA.pkl")
	pickle_Data            = list()
	for config in root.SavedStates.ProductConfigurations:
		if not config.name == '__default__':
			config_data=dict(code=config.eim_name,dls=config.maya_display_layers(),rls=[])
			pickle_Data.append(config_data)
	with file(pickle_file,'w') as pkf:
		pickle.dump(pickle_Data,pkf)
#----------------------------------------------------------------------
def Get_EIM_Data():
	try:
		pm.mel.VGConfigWindow()
		cmds.deleteUI("windowVGConfigWindow",window=True)
		adjustDisplayLayer = pm.mel.adjustDisplayLayer
		adjustRenderLayer = pm.mel.adjustRenderLayer
		pickle_file            = os.path.join(os.environ["temp"],"EMI_BUILD_DATA.pkl")
		displayLayerController = pm.melGlobals["displayLayerController"]
		renderLayerController  = pm.melGlobals["renderLayerController"]
		displayLayers          = pm.melGlobals["displayLayers"]
		renderLayers           = pm.melGlobals["renderLayers"]
		exteriorColors         = pm.melGlobals["exteriorColors"]
		modelCodes             = pm.melGlobals["modelCodes"]
		pickle_Data            = list()
		code_count             = len(modelCodes)
		all_display_layers     = [layer for layer in cmds.ls(typ="displayLayer") if not layer == "defaultLayer"]
		for i,code in enumerate(modelCodes):
			config_data=dict(code=code,dls=[],rls=[])
			adjustDisplayLayer(displayLayerController,code)
			cmds.inViewMessage( statusMessage='<hl>Collecting Data For Eim %i of %i\n"%s"</hl>.' % (i+1,code_count,code), fadeInTime=0, fadeOutTime=0, fadeStayTime=200,fontSize=20, pos='midCenter', fade=True )
			cmds.refresh()
			active_dls =  []
			for layer in all_display_layers:
				if cmds.getAttr(layer+".v"):
					active_dls.append(layer)
			config_data['dls']= list(set(active_dls))
			#adjustRenderLayer(renderLayerController, code)
			#actvie_rls = []
			#for layer in renderLayers:
			#	cmds.refresh()
			#	if cmds.objExists(layer):
			#		if cmds.getAttr(layer+".renderable"):
			#			actvie_rls.append(layer)
			#config_data['rls']=actvie_rls
			pickle_Data.append(config_data)
		with file(pickle_file,'w') as pkf:
			pickle.dump(pickle_Data,pkf)
	except MelUnknownProcedureError:
		cmds.error("Cannot find procedure VGConfigWindow")
#----------------------------------------------------------------------
def dump_EIM_Data():
	if pm.objExists("JSON_document"):
		Get_JSON_EMI_Data()
	elif pm.objExists("VGConfigXMLScriptNode"):
		Get_XML_EMI_Data()
	else:
		Get_EIM_Data()
#----------------------------------------------------------------------
def load_EIM_Data():
	res = []
	pickle_file            = os.path.join(os.environ["temp"],"EMI_BUILD_DATA.pkl")
	with file(pickle_file,'r') as pkf:
		pickle_Data = pickle.load(pkf)
	for item in pickle_Data:
		res.append(EIM_Config_Data(item['code'],item['dls']))
	return res
