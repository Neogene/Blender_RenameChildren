bl_info = {
    "name": "Rename children using parent name",
    "blender": (2, 80, 0),
    "version": (0,0,1),
    "category": "Object",
    "author": "Andrea Leganza"
}

import bpy

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")  

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


class ChildrenRename(bpy.types.Operator):
    """Rename all children using parent name"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.rename_children"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Rename children using parent name"         # Display name in the interface.
    bl_info = "Rename children using parent name and appening 0..9"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.  #bpy.context.selected_objects

    def execute(self, context):        # execute() is called when running the operator.

        print('Starting...')

        selected_objects = bpy.context.selected_objects #bpy.data.objects

        if len(selected_objects)>0 :

            children = bpy.data.meshes 
                
            for ob in selected_objects:
                  
                i = 0
                
                for child in children:
                   # print (child.name)
                    if ob.data == child:
                        if not child.name.split('_')[0] == ob.name:
                            print("Mesh '%s' is the child of Object '%s' -> '%s'." % (child.name, ob.name, ob.name + '_i' + str(i).zfill(2)))
                            child.name = ob.name + '_' + str(i).zfill(2)
                            i += 1
                        else :
                            print(str(child.name) +" was lready renamed")
        else:
            print ("No object selected")
            ShowMessageBox("No objects selected", "Error", 'ERROR')
             
        print('...done')
        ShowMessageBox("Completed", "Information", 'INFO')

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ChildrenRename.bl_idname)

def register():
    bpy.utils.register_class(ChildrenRename)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.OUTLINER_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ChildrenRename)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()