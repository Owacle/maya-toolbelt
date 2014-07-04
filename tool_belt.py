'''
=Toolbelt=
@author:Melt van der Spuy
@summary: library of little tools to help with other scripts.

Tools:
- Zero Channels
- Centre Camera
- Add Items to Node Editor window
- Get Panel Type
- Find the left or right version of an item
'''

import bd_rig.rig_utils.ctrls as ctrls
import maya.cmds as cmds

#ctrls.add_nulls('Group')

# links the visibility of the second arg to the attr in the first arg
#ctrls.vis_switch('COG_Ctrl.scaleZ', ['nurbsSphere1'])

# makes a link between an attribute and a constraint weight
# second part is the control and attribute that control the weight
# ctrls.reverse_constraint('nurbsSphere1_parentConstraint1', 'COG_Ctrl','flip_Constraint')

import bd_ui_scripts.bd_rig_shelf_scripts as rig_shelf
import datetime
import sys
from pymel.core import *
import os

def find_model_pack():
    """go and find it based on the currently open file"""
    name_of_this_scene = ''
    path_to_model_packs = 'T:/dwtv/vgt/00Prod/03_Designs/'


def get_world_notes():

    file_name = fileDialog2(dialogStyle=1, okCaption='Open', startingDirectory='T:/dwtv/vgt/Maya_VGT/scenes/Props/')
    #print file_name
    #file_name = ['T:/dwtv/vgt/Maya_VGT/scenes/Props/C/CardboardGameA/06_Rig/WIP/VGT_CardboardGameA_Rig_v013_BD.ma']
    #file_name = ['T:/dwtv/vgt/Maya_VGT/scenes/Props/L/LightFixtureA/06_Rig/WIP/VGT_LightFixtureA_Rig_v008_BD.ma']
    with open(file_name[0], 'r') as openfile:
        all_lines = openfile.readlines()
    openfile.close()
    first_line = 0
    last_line = 0
    for i in range(250):
        if 'World' in all_lines[i]:
            for j in range(i,250):
                if '.nts' in all_lines[j]:
                   first_line = j
                   for k in range(j,250):
                       if ');' in all_lines[k]:
                           last_line = k
                           break
                   break
            break
    #print first_line
    #print last_line
    all_together = ''
    #print all_lines[first_line:last_line+1]
    for line in all_lines[first_line:last_line+1]:

        all_together += line
    #all_together = all_lines[first_line:last_line]
    start = all_together.find('(')
    all_together = all_together[start+1:]
    all_together = all_together.replace('\\n', '\n')
    print all_together


def lock_transforms(items, locked=True):
    for item in items:
        cmds.setAttr(item+'.tx', lock=locked )
        cmds.setAttr(item+'.ty', lock=locked )
        cmds.setAttr(item+'.tz', lock=locked )
        cmds.setAttr(item+'.rx', lock=locked )
        cmds.setAttr(item+'.ry', lock=locked )
        cmds.setAttr(item+'.rz', lock=locked )
        cmds.setAttr(item+'.sx', lock=locked )
        cmds.setAttr(item+'.sy', lock=locked )
        cmds.setAttr(item+'.sz', lock=locked )

def make_uv_instance(*args):
    cmds.instance()
#
def set_lambert():
    meshes = cmds.ls(sl=True)
    for mesh in meshes:
        cmds.sets(mesh, edit=True, forceElement='initialShadingGroup')

def scale_and_parent(maintain_offset=False):
    '''
    do both
    '''
    first, second = cmds.ls(sl=True)[0:2]
    prntConstraint = cmds.parentConstraint( first,second, maintainOffset=maintain_offset)
    sclConstraint = cmds.scaleConstraint( first,second)

def insert_world_note(who, note):

    if cmds.window("WorldNote", exists=True) :
        cmds.deleteUI("WorldNote")
        cmds.windowPref("WorldNote", removeAll=True)

    win_main = cmds.window("WorldNote", title="World Note" )

    obj = cmds.ls('World*')
    current_notes = cmds.getAttr(obj[0]+'.notes')+'\n'
    d = datetime.datetime.now()
    date_string = d.strftime('%m-%d-%Y')
    user_name = who
    production = 'BD VGT'
    my_notes = note
    cmds.setAttr(obj[0]+'.notes',current_notes + date_string + ' ' + user_name + ' ' + production + '\n' + my_notes, type='string')
    cmds.select('World*')


def get_panel_type():
    '''
    returns type of panel under focus
    '''
    current_panel = cmds.getPanel(withFocus=True)
    current_panel_type = cmds.getPanel(typeOf=current_panel)
    return current_panel_type

def makeLocatorControl(ctrlName):

    allSelected = cmds.ls(sl=True)
    if len(allSelected) == 0:
        print "nothing selected"
        return

    for selected in allSelected:
        selParent = cmds.listRelatives( selected, parent=True)
        controlCircleName = selected + '_' + ctrlName + '_crv'

        controlCircle = cmds.circle( nr=(0,0,1), c=(0,0,0), name=controlCircleName, r=2)
        cmds.setAttr( controlCircleName+'.overrideEnabled', 1)
        cmds.setAttr( controlCircleName+'.overrideColor', 6)

        zero_group = cmds.group(em=True, name=controlCircleName[:-4]+'_zero')
    #   cmds.spaceLocator( name='sandwichChild_'+justOne )
        cmds.parent(controlCircle, zero_group)
        cmds.parent(zero_group, selected, relative=True)
        cmds.parent(zero_group, selParent)
        cmds.parent(selected, controlCircle)

    #temp Locator move TO target object
#   tempParentConstraint = cmds.parentConstraint(justOne, controlCircle)
#   cmds.delete(tempParentConstraint)
#   tempParentConstraint = cmds.parentConstraint(justOne, bakedCircle)

#   theParentConstraint = cmds.parentConstraint( sandwichChild, justOne)
#   listOfWeights = cmds.parentConstraint( theParentConstraint, query=True, wal=True)
#   otherWeights = cmds.parentConstraint( theParentConstraint, query=True, tl=True)
#   try:
#       sel = cmds.ls(sl=True)[0]
#   except:
#       print "nothing selected"
#       return
import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya
import re

'''
try:
    import ml_utilities as utl
    utl.upToDateCheck(8)
except ImportError:
    result = cmds.confirmDialog( title='Module Not Found',
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.',
                button=['Download Module','Cancel'],
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )

    if result == 'Download Module':
        cmds.showHelp('http://morganloomis.com/download/ml_utilities.py',absolute=True)
'''
def set_lambert():
    meshes = cmds.ls(sl=True)
    for mesh in meshes:
        cmds.sets(mesh, edit=True, forceElement='initialShadingGroup')

def scale_and_parent(maintain_offset=False):
    '''
    do both
    '''
    first, second = cmds.ls(sl=True)[0:2]
    prntConstraint = cmds.parentConstraint( first,second, maintainOffset=maintain_offset)
    sclConstraint = cmds.scaleConstraint( first,second)


def doubleParent():
    '''
    Make a double locator parent chain

    Usage example:
        want to attach an apple to a hand
        rather than parent the apple directly, constrain the apple to a locator which is the child of another
        then constrain the parent to the hand

    Addition:
        Add a control with the previous location baked

    '''


    #get the guy
    justOne = cmds.ls( sl=True )[0]

    start, end = utl.frameRange()
    print start
    #make a temp locator at the spot we copied
    if cmds.objExists('watch_this_space'):
        cmds.delete('watch_this_space')


    controlCircleName = 'sandwichControl_'+justOne
    offsetCircleName = 'sandwichOffset_'+justOne
    bakedCircleName = 'bakedControl_'+justOne
    sandwichChildName = 'sandwichChild_'+justOne


    controlCircle = cmds.circle( nr=(0,0,1), c=(0,0,0), name=controlCircleName, r=2)
    cmds.setAttr( controlCircleName+'.overrideEnabled', 1)
    cmds.setAttr( controlCircleName+'.overrideColor', 6)
    offsetCircle = cmds.circle( nr=(0,0,1), c=(0,0,0), name=offsetCircleName, r=1.5)
    cmds.setAttr( offsetCircleName+'.overrideEnabled', 1)
    cmds.setAttr( offsetCircleName+'.overrideColor', 9)


    #bakedCircle = cmds.circle( nr=(0,0,1), c=(0,0,0), name=bakedCircleName, r=2)
    #cmds.setAttr( bakedCircleName+'.overrideEnabled', 1)
    #cmds.setAttr( bakedCircleName+'.overrideColor', 10)

    sandwichChild = cmds.spaceLocator( name='sandwichChild_'+justOne )
    cmds.parent( offsetCircleName, controlCircleName)
    cmds.parent( sandwichChildName, offsetCircleName)

    #temp Locator move TO target object
    tempParentConstraint = cmds.parentConstraint(justOne, controlCircle)
    cmds.delete(tempParentConstraint)

    #tempParentConstraint = cmds.parentConstraint(justOne, bakedCircle)
    theParentConstraint = cmds.parentConstraint( sandwichChild, justOne)
    listOfWeights = cmds.parentConstraint( theParentConstraint, query=True, wal=True)
    otherWeights = cmds.parentConstraint( theParentConstraint, query=True, tl=True)
    #print listOfWeights
    #print theParentConstraint
    #print otherWeights
    cT = cmds.currentTime( query=True )
    cmds.currentTime( cT-1, update=False)
    cmds.setKeyframe( theParentConstraint[0]+'.'+listOfWeights[0], v=0 )
    cmds.currentTime( cT, update=False)
    cmds.setKeyframe( theParentConstraint[0]+'.'+listOfWeights[0], v=1 )
    #cmds.setKeyframe( v=1, at='translateX' )
    cmds.select('sandwichControl_'+justOne)







globalTransX = '0'
globalTransY = '0'
globalTransZ = '0'

globalRotX = '0'
globalRotY = '0'
globalRotZ = '0'

def getWorldValues(tField1, *args):
    global globalTransX
    global globalTransY
    global globalTransZ
    #print 'Getting Values:'
    allSelected = cmds.ls( sl=True )
    try:
        justOne = allSelected[0]
    except:
        OpenMaya.MGlobal.displayWarning('At least one things needs to be selected')
        return

    if cmds.objExists('watch_this_space'):
        cmds.delete('watch_this_space')

    locTempPosition = cmds.spaceLocator( name='watch_this_space' )
    if justOne:
        print "there is one"
        theParentConstraint = cmds.parentConstraint( justOne, locTempPosition)
        trnVal = cmds.xform( locTempPosition, query=True, worldSpace=True, rotatePivot=True )
        rotVal = cmds.xform( locTempPosition, query=True, worldSpace=True, rotation=True )
        cmds.delete(theParentConstraint)

        globalTransX = trnVal[0]
        globalTransY = trnVal[1]
        globalTransZ = trnVal[2]
        trX = cmds.textField("transXVal", edit=True, text=trnVal[0])
        trX = cmds.textField("transYVal", edit=True, text=trnVal[1])
        trX = cmds.textField("transZVal", edit=True, text=trnVal[2])

        globalRotX = rotVal[0]
        globalRotY = rotVal[1]
        globalRotZ = rotVal[2]
        rtX = cmds.textField("rotXVal", edit=True, text=rotVal[0])
        rtX = cmds.textField("rotYVal", edit=True, text=rotVal[1])
        rtX = cmds.textField("rotZVal", edit=True, text=rotVal[2])

        #trnVal = cmds.xform( justOne, query=True, worldSpace=True, matrix=True )
        #scaleVal = cmds.xform( justOne, query=True, worldSpace=True, scale=True )
        #print trnVal
        #print scaleVal
        cmds.delete(locTempPosition)
        cmds.select(justOne)
        return trnVal


def setTrans(*args):
    '''
        Make a locator in the correct spot
        Constrain it to that locator
        remove the constraint
    '''

    allSelected = cmds.ls( sl=True )
    try:
        justOne = allSelected[0]
    except:
        OpenMaya.MGlobal.displayWarning('At least one things needs to be selected')
        return
    trnXVal = cmds.textField("transXVal", query=True, text=True)
    trnYVal = cmds.textField("transYVal", query=True, text=True)
    trnZVal = cmds.textField("transZVal", query=True, text=True)

    #make a temp locator at the spot we copied
    if cmds.objExists('watch_this_space'):
        cmds.delete('watch_this_space')

    locTempPosition = cmds.spaceLocator( name='watch_this_space' )
    print locTempPosition
    #  ***NOTE***
    #  for the time being this LOOKS like what we want...
    #  Possible issue involving offset pivots
    cmds.xform( locTempPosition, worldSpace=True, translation=(trnXVal, trnYVal, trnZVal))


    print justOne
    tempConstraint = cmds.pointConstraint( locTempPosition, justOne )
    lAnimCurves = cmds.keyframe(justOne, query=True, name=True)
    #print lAnimCurves
    if lAnimCurves:
        #this has an issue resolving the namespace for some reason - get there later - for now, just key it
        #if justOne+'_translateX' in lAnimCurves:
            #print 'in-in'
        cmds.setKeyframe(justOne, attribute='translateX')
        cmds.setKeyframe(justOne, attribute='translateY')
        cmds.setKeyframe(justOne, attribute='translateZ')
    cmds.delete(tempConstraint)
    cmds.delete(locTempPosition)
    cmds.select(justOne)


def setRot(*args):
    '''
        Set the ROTATION based on the snapping values
        Make a locator
        rotate it to the right values
        point constrain it to the TARGET
        delete the point constraint
        parent constrain the TARGET to it
        remove the constraint
    '''

    justOne = cmds.ls( sl=True )[0]
    #print 'Rotating the first object selected'
    rotXVal = cmds.textField("rotXVal", query=True, text=True)
    rotYVal = cmds.textField("rotYVal", query=True, text=True)
    rotZVal = cmds.textField("rotZVal", query=True, text=True)

    #make a temp locator at the spot we copied
    if cmds.objExists('watch_this_space'):
        cmds.delete('watch_this_space')

    locTempPosition = cmds.spaceLocator( name='watch_this_space' )
    #  ***NOTE***
    #  for the time being this LOOKS like what we want...
    #  Possible issue involving offset pivots
    cmds.xform( locTempPosition, worldSpace=True, rotation=(rotXVal, rotYVal, rotZVal))

    #temp Locator move TO target object
    tempPointConstraint = cmds.pointConstraint(justOne, locTempPosition)
    cmds.delete(tempPointConstraint)

    tempParentConstraint = cmds.parentConstraint( locTempPosition, justOne )
    lAnimCurves = cmds.keyframe(justOne, query=True, name=True)
    #print lAnimCurves
    if lAnimCurves:
        #same problem with the rotation - damn
            #if justOne+'_rotateX' in lAnimCurves:
        cmds.setKeyframe(justOne, attribute='rotateX')
        cmds.setKeyframe(justOne, attribute='rotateY')
        cmds.setKeyframe(justOne, attribute='rotateZ')

    cmds.delete(tempParentConstraint)
    cmds.delete(locTempPosition)
    cmds.select(justOne)

def snapper():
    '''
        Builds the interface and pulls the values into the window
        Get the values of the one object into the window
    '''
    #check to see if the UI exists
    if cmds.window("snapperUI", exists=True):
        cmds.deleteUI("snapperUI")

    #create the window
    wSnapper = cmds.window("snapperUI", title = "Snapper", width=350, height=300, sizeable=False, toolbox=1)
    cmds.columnLayout()
    #cmds.frameLayout( label='CLICK to set')
    cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1, 80), (2, 90), (3,90), (4,90)], height=60 )
    cmds.button( label='translate', command=setTrans, height=30)
    trX = cmds.textField("transXVal", editable=False, text=globalTransX, backgroundColor=(1,0.7,0.7))
    trY = cmds.textField("transYVal", editable=False, text=globalTransY, backgroundColor=(0.6,1,0.6))
    trZ = cmds.textField("transZVal", editable=False, text=globalTransZ, backgroundColor=(0.7,0.7,1))
    '''
    trX = cmds.textField("transXVal", editable=False, text='0')
    trY = cmds.textField("transYVal", editable=False, text='0')
    trZ = cmds.textField("transZVal", editable=False, text='0')
    '''
    cmds.button( label='rotate', command=setRot, height=30)
    rtX = cmds.textField("rotXVal", editable=False, text=globalRotX, backgroundColor=(1,0.6,0.6))
    rtY = cmds.textField("rotYVal", editable=False, text=globalRotY, backgroundColor=(0.7,1,0.7))
    rtZ = cmds.textField("rotZVal", editable=False, text=globalRotZ, backgroundColor=(0.6,0.6,1))
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( labelVisible=False )
    cmds.button( label='Copy All', command=getWorldValues, width=350, height=40)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    #show the window
    cmds.showWindow(wSnapper)


def UI():
    #check to see if the UI exists
    if cmds.window("exampleUI", exists=True):
        cmds.deleteUI("exampleUI")

    #create the window
    window = cmds.window("exampleUI", title = "Example UI", w=300, h=300, mnb=False, mxb=False, sizeable=False)

    #show the window
    cmds.showWindow(window)

def makeLocatorControl(ctrlName):

    allSelected = cmds.ls(sl=True)
    if len(allSelected) == 0:
        print "nothing selected"
        return

    for selected in allSelected:
        selParent = cmds.listRelatives( selected, parent=True)
        controlCircleName = selected + '_' + ctrlName + '_crv'

        controlCircle = cmds.circle( nr=(0,0,1), c=(0,0,0), name=controlCircleName, r=2)
        cmds.setAttr( controlCircleName+'.overrideEnabled', 1)
        cmds.setAttr( controlCircleName+'.overrideColor', 6)

        zero_group = cmds.group(em=True, name=controlCircleName[:-4]+'_zero')
    #   cmds.spaceLocator( name='sandwichChild_'+justOne )
        cmds.parent(controlCircle, zero_group)
        cmds.parent(zero_group, selected, relative=True)
        cmds.parent(zero_group, selParent)
        cmds.parent(selected, controlCircle)

    #temp Locator move TO target object
#   tempParentConstraint = cmds.parentConstraint(justOne, controlCircle)
#   cmds.delete(tempParentConstraint)

    #tempParentConstraint = cmds.parentConstraint(justOne, bakedCircle)

#   theParentConstraint = cmds.parentConstraint( sandwichChild, justOne)
#   listOfWeights = cmds.parentConstraint( theParentConstraint, query=True, wal=True)
#   otherWeights = cmds.parentConstraint( theParentConstraint, query=True, tl=True)
#   try:
#       sel = cmds.ls(sl=True)[0]
#   except:
#       print "nothing selected"
#       return


def makeClusters():

    selection = cmds.ls(selection=True)
    #get the curve name by stripping off the end
    curve = selection[0].split('.')[0]
    #get the
    selCV = selection[0][ selection[0].find('[')+1 : selection[0].find(']') ]
    #print selCV
    numSpans = cmds.getAttr( curve + '.spans' )
    degree = cmds.getAttr( curve + '.degree' )
    form = cmds.getAttr( curve + '.form')
    numCVs = numSpans + degree;
    if ( form == 2 ):
        numCVs -= degree
    try:
        state = int(selCV) % 2
    except:
        state = 0
        selCV = numCVs + 1

    if state == 0:
        selList = range(0, numCVs-1, 2) # evens
    else:
        selList = range(1, numCVs, 2) # odds

    selList = range(0,numCVs,1)
    for thisOne in range(0, numCVs):
       curvePoint =  curve + '.cv[' + str(thisOne) + ']'
       print curvePoint
       myCluster = cmds.cluster(curvePoint)
       print myCluster[1]
       placementLoc = cmds.spaceLocator()
       tempParentConstraint = cmds.parentConstraint(myCluster[1], placementLoc)
       cmds.delete(tempParentConstraint)
       cmds.pointConstraint(placementLoc, myCluster[1])
       '''
       #sandwichChild=cmds.spaceLocator()

       tempParentConstraint = cmds.parentConstraint(curvePoint, sandwichChild)
       cmds.delete(tempParentConstraint)
       '''

def findLeft():
    '''
    Find the object that is the LEFT version of the one selected
    '''
    try:
        justOne = cmds.ls(sl=True)[0]
    except:
        print "you need to select at least one"
        return

#check if we are switching left or right
    if ('_R|' in justOne) | ('R_' in justOne):
        sFind = 'R'
        sRepl = 'L'
    else:
        sFind = 'L'
        sRepl = 'R'

    newSel = justOne.replace('_'+ sFind +'_', '_'+ sRepl +'_')
    newSel = newSel.replace('_'+ sFind + '|','_'+ sRepl + '|')
    newSel = newSel.replace(sFind + '_',sRepl + '_')
    try:
        cmds.select(newSel)
    except:
        cmds.warning("No Mirror object exists: "+newSel)