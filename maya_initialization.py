import os
import maya.cmds  as cmds
import maya.utils as utils
import maya.mel   as mel
import Scripts
if os.environ.has_key("AW_GLOBAL_SYSTEMS"):
	if not os.environ["AW_GLOBAL_SYSTEMS"] in os.sys.path:
		os.sys.path.append(os.environ["AW_GLOBAL_SYSTEMS"])

from Environment_Access import System_Paths, System_Settings, utilities

if System_Settings.USE_WING_DEBUG:
	try:
		import wingdbstub
	except:
		pass
	
MAYA_VERSION           = int(cmds.about(version=True))
MAYA_BATCH             = cmds.about(b=True)
MAYA_GUI               = False if MAYA_BATCH else True

os.environ["MAYA_GUI"] = "1" if MAYA_GUI else "0"

if MAYA_VERSION >= 2017:
	os.environ["QT_PACKAGE"] = "PySide2"
elif MAYA_VERSION >= 2013:
	os.environ["QT_PACKAGE"] = "PySide"
else:
	os.environ["QT_PACKAGE"] = "PyQt4"
	
cmds.setStartupMessage(os.path.join(os.environ["MAYA_LOCATION"],'icons',"MayaStartupImage.png").replace("/", "\\"))

if MAYA_GUI:
	utilities.add_To_System_Path(System_Paths._CODE_AW_SITE_PACKAGES)
	if MAYA_VERSION == 2015:
		# cmds.setStartupMessage(os.path.join(System_Paths._CODE_MAYA_XBM_PATH , "MayaStartupImage.png"))
		#----------------------------------------------------------------------
		utilities.add_To_Multi_Path_Environment_Key("MAYA_SCRIPT_PATH", [item.replace("\\", "/") for item in [System_Paths._CODE_MAYA_SCRIPT_PATH, System_Paths._CODE_MAYA_SCRIPT_PATH_2015, System_Paths._CODE_MAYA_BONUS_TOOLS_MEL, System_Paths._CODE_MAYA_BONUS_TOOLS_MEL_2015]])
		#----------------------------------------------------------------------
		utilities.add_To_Multi_Path_Environment_Key("XBMLANGPATH", [System_Paths._CODE_MAYA_BONUS_TOOLS_ICONS, System_Paths._CODE_MAYA_XBM_PATH])
		#----------------------------------------------------------------------
		utilities.add_To_System_Path(System_Paths._CODE_MAYA_BONUS_TOOLS_PYTHON)
		utilities.add_To_System_Path(System_Paths._CODE_MAYA_BONUS_TOOLS_PYTHON_2014)
		utilities.add_To_System_Path(System_Paths._CODE_MAYA_BONUS_TOOLS_PYTHON_2015)
		if not System_Settings.NO_USER_TOOLS:
			utilities.add_To_System_Path(System_Paths.MAYA_USER_TOOLS_DIR)
			utils.executeDeferred ('mel.eval("bonusToolsMenu")')
	utils.executeDeferred ('import Scripts.global_Shelf_Builder')
	utils.executeDeferred ('import Scripts.callbacks')
	utils.executeDeferred ('import Scripts.Maya_Runtime_Commands')
	utils.executeDeferred ('import Scripts.menu_item_addons')
	if not System_Settings.NO_USER_TOOLS:
		utils.executeDeferred ('import Maya_UserTools; Maya_UserTools.pythonScripts()')
	try:
		import socket
		HOST = socket.getfqdn()
		PORT = "5555" 	# The same port as used by the server
		name = "{}:{}".format(HOST,PORT)
		cmds.commandPort( bufferSize=16, echoOutput=False, name=name, noreturn=True, pickleOutput=False, prefix="", returnNumCommands=False, sourceType="python", securityWarning=False)
	except:
		pass
	# utils.executeDeferred ('import Scripts.Tools.Selection_Set_Manager.Selection_Set_Editor_Loader; G_Selection_Set_Editor = Scripts.Tools.Selection_Set_Manager.Selection_Set_Editor_Loader.Load_Editor()')
