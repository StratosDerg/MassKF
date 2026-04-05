# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Mass KeyFrame",
    "blender": (4,4,2),
    "category": "Animation",
    "author": "StratosDerg",
    "warning": "",
    "description": "Support for adding and duplicating keyframes to properties."
}

import bpy # type: ignore
from mathutils import * # type: ignore
 
def masskf(op, context, path, index, value=None, copy=False):
        for obj in context.selected_objects:
            try:
                objkf(context=context, path=path, index=index, value=value, copy=copy)
            except AttributeError as e:
                op.report({'ERROR'}, f"Keyframing Failed on {obj.name}: {str(e)}")
                return {'CANCELLED'}
            except ValueError as e:
                if "rigid_body" in path and obj.rigid_body == None:
                    bpy.ops.rigidbody.object_add()
#                if path.startswith("modifiers["):
                    
                try:
                    objkf(context=context, path=path, index=index, value=value, copy=copy)
                except:
                    op.report({'ERROR'}, f"Keyframing Failed on {obj.name}, is it the same type?")
                    continue
def objkf(context, path, index, value=None, copy=False):
    if copy:
        obj.path_assign(path, value)
    obj.keyframe_insert(
        data_path=path, index=index, frame=context.scene.frame_current
    )

class MKFDupeAll(bpy.types.Operator):
    """Duplicate a property from active and add a keyframe to all selected objects"""
    bl_idname = "anim.mkf_dupe_all"
    bl_label = "Dupicate Keyframe to Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.property:
            active = context.property
            block, path, index = active
            value = block.path_resolve(path)
            masskf(
                op=self, context=context, path=path, index=index, value=value, copy=True
                )

        return {'FINISHED'}
   
class MKFAddAll(bpy.types.Operator):
    """Add a keyframe of selected property to all selected objects"""
    bl_idname = "anim.mkf_add_all"
    bl_label = "Add Keyframe to Selected Objects"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        if context.property:
            active = context.property
            block, path, index = active
            masskf(
                self=self, context=context, path=path, index=index, copy=False
                )
        
        return {'FINISHED'}

# class MKFDupeFrom(bpy.types.Operator):
#     """Duplicate a property from active and add a keyframe to all selected objects excluding active"""
#     bl_idname = "anim.mkf_dupe_from"
#     bl_label = "Add Keyframe to Selected Objects"
#     bl_options = {'REGISTER','UNDO'}

#     def execute(self,context):
#         if context.property:
#             active = context.property
#             block, path, index = active
#             masskf(
#                 context=context, path=path, index=index, copy=True, active=False
#                 )
        
#         return {'FINISHED'}

# class MKFAddFrom(bpy.types.Operator):
#     """Add a keyframe for selected property to all selected objects excluding active"""
#     bl_idname = "anim.mkf_add_from"
#     bl_label = "Add Keyframe to Selected Objects"
#     bl_options = {'REGISTER','UNDO'}

#     def execute(self,context):
#         if context.property:
#             active = context.property
#             block, path, index = active
#             masskf(
#                 context=context, path=path, index=index, copy=False, active=False
#                 )
        
#         return {'FINISHED'}

def menu_func(self,context):
    layout = self.layout
    if context.area.ui_type=='PROPERTIES':
        layout.separator()

        layout.menu("UI_MT_mkf_submenu")

class MKFMenu(bpy.types.Menu):
    bl_idname = "UI_MT_mkf_submenu"
    bl_label = "Mass Keyframe"

    def draw(self,context):
        layout = self.layout

        # Submenu Layout
        layout.operator("anim.mkf_dupe_all",text="Duplicate a keyframe to Selected")
        layout.operator("anim.mkf_add_all",text="Add a keyframe to Selected")
        # layout.operator("anim.mkf_dupe_from",text="Duplicate a keyframe from Active")
        # layout.operator("anim.mkf_add_from",text="Add a keyframe to from Active")


def register():
    bpy.utils.register_class(MKFDupeAll)
    bpy.utils.register_class(MKFAddAll)
    # bpy.utils.register_class(MKFAddFrom)
    # bpy.utils.register_class(MKFDupeFrom)
    bpy.utils.register_class(MKFMenu)
    
    bpy.types.UI_MT_button_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MKFDupeAll)
    bpy.utils.unregister_class(MKFAddAll)
    # bpy.utils.unregister_class(MKFAddFrom)
    # bpy.utils.unregister_class(MKFDupeFrom)    
    bpy.utils.unregister_class(MKFMenu)
    
    bpy.types.UI_MT_button_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
