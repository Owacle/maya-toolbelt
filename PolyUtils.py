'''
Created on July 2, 2014

@author: Melt van der Spuy
'''

import maya.cmds as cmds
import ToolBoxFn

def is_type(in_obj, types):
    """
    get the object type by examining the shape
    in_obj = name of the transform - python string (probably returned by a ls(sl=true))
    type = python string
    """

    obj_shape = cmds.listRelatives(in_obj, shapes=True, noIntermediate=True)
    obj_type = cmds.nodeType(obj_shape)

    if obj_type == 'nurbsCurve':
        if 'wire' in types:
            out_connections = cmds.listConnections(obj_shape, source=False)
            for one_conn in out_connections:
                if cmds.nodeType(one_conn) == 'wire':
                    return True
    elif obj_type in types:
        return True
    else:
        return False

def return_objects_of_type(objects, types):
    """
    hand back a list of objects matching the type
    object = list of python strings (probably from a ls(sl=true))
    type = python string
    return = list of python strings (for the transforms)
             empty list if there are none
    """
    out_list = []
    for one_obj in objects:
        if is_type(one_obj, types):
            out_list.append(str(one_obj))

    return out_list


def load_selected_command(list_for_items, text_field):
    '''
    loads the currently selected items into the scrollField
    '''
    def load_selected(*args):
        selected = cmds.ls(sl=True)
        print('this is what\'s selected %s', selected)
        print('the list of items %s', list_for_items)
        list_for_items[:] = []
        for item in selected:
            list_for_items.append(item)
        cmds.textScrollList(text_field, edit=True, removeAll=True)
        cmds.textScrollList(text_field, edit=True, append=list_for_items)

    return load_selected

class RowWindow():
    """a class to quickly build a window with some rows of buttons"""
    def __init__(self, title='no title', width=300, height=500):
        self._title = title
        self._win_name = title+'_win'
        self._width = width
        self._height = height
        self._controls = []

    def add_row(self, type, name, command_str=''):
        self._controls.append({'type':type, 'name':name, 'cmd':command_str})

    def show(self):
        if cmds.window(self._win_name, exists=True):
            cmds.deleteUI(self._win_name)

        win = cmds.window(self._win_name, width=self._width, height=self._height, title=self._title)
        row_layout = cmds.columnLayout(rowSpacing=10)

        for control in self._controls:
            ctrl_type = control['type']
            if ctrl_type == 'button':
                cmds.button(label=control['name'], command=control['cmd'])
            elif ctrl_type == 'scrollField':
                cmds.scrollField()
            elif ctrl_type == 'textScrollList':
                cmds.textScrollList(control['name'])
            elif ctrl_type == 'text':
                cmds.text()

        cmds.showWindow(win)


class ClusterTools():
    """ A way of redoing a few of bill ballouts things without needing QT"""

    @staticmethod
    def extrap_to_clusters_ui():
        temp_list = ['one', 'two']
        extrap_win = RowWindow(title='Extrapolate to Clusters')
        extrap_win.add_row(type='scrollField', name='scr_field')
        extrap_win.add_row(type='textScrollList', name='text_field')
        extrap_win.add_row(type='button',name='test_button', command_str=load_selected_command(temp_list, 'text_field'))
        extrap_win.show()

    @staticmethod
    def extrap_to_clusters():
        """Just extrapolate from all the transforms to ONE geometry object"""
        sel = cmds.ls(sl=True)
        meshes = return_objects_of_type(sel, 'mesh')
        deforms = return_objects_of_type(sel, ['lattice', 'clusterHandle', 'wire'])
        for mesh in meshes:
            for deform in deforms:
                ToolBoxFn.extrapToCluster([deform, mesh])

