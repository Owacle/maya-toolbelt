'''
=Toolbelt=
@author:Melt van der Spuy
@summary: the tools for making and connecting the baseball hat

'''

import bd_rig.rig_utils.ctrls as ctrls
import maya.cmds as cmds

#ctrls.add_nulls('Group')

# links the visibility of the second arg to the attr in the first arg
#ctrls.vis_switch('COG_Ctrl.scaleZ', ['nurbsSphere1'])

def make_hat_placement():
    """
    create the connection point for the hat within the character rig
    this will be used late for attaching the referenced hat
    """
    follicle_to_follow = 'Brow_Rivet_Follicle'
    #print('this is where to attach: %s',follicle_to_follow)
    if cmds.objExists(follicle_to_follow):
        print 'we have it'
    else:
        print 'not found'

def scale_and_parent(maintain_offset=False):
    '''
    do both
    '''
    first, second = cmds.ls(sl=True)[0:2]
    prntConstraint = cmds.parentConstraint( first,second, maintainOffset=maintain_offset)
    sclConstraint = cmds.scaleConstraint( first,second)

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
