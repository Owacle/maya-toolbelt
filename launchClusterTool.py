import sys
import os
import maya.mel as mel

path = 'T:/dwtv/vgt/crew/rig_scripts/DW_Scripts/mel/'
melFiles = os.listdir('T:/dwtv/vgt/crew/rig_scripts/DW_Scripts/mel')

for file in melFiles:
    mel.eval( 'source "%s%s"'%(path,file))

sys.path.append('T:/dwtv/vgt/crew/rig_scripts')
sys.path.append('T:/dwtv/vgt/crew/rig_scripts/DW_Scripts')

from PySide import QtCore,QtGui,shiboken

from py import UILib
reload(UILib)

windowVar = ''
def open_win():
    global windowVar
    try:
        windowVar.close()  # @UndefinedVariable
    except:
        pass

    toolWin = UILib.ToolBoxWin()
    toolWin.show()
    windowVar = toolWin

open_win()
