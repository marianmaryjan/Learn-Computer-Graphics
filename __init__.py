bl_info = {
    "name": "Learn Computer Graphics",
    "author": "Marta Zawadzka",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Development > New Object",
    "description": "Helps in learning Computer Graphics",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

from learn_computer_graphics import mesh
from learn_computer_graphics import curves
from learn_computer_graphics import rendering

####################################################
#Connecting main script with mesh.py

class highlight_gaps(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.highlight_gaps"
    bl_label = "Highlight gaps"


    def execute(self, context):
        mesh.gaps_on(context)
        return {'FINISHED'}



class remove_gaps(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.remove_gaps"
    bl_label = "Remove gaps"


    def execute(self, context):
        mesh.gaps_remove(context)
        return {'FINISHED'}
    
    
class highlight_interior_faces(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.highlight_interior_faces"
    bl_label = "Highlight interior faces"


    def execute(self, context):
        current_mesh = bpy.context.scene.objects[ 0 ]
        current_mesh_data = current_mesh.data
        bpy.ops.object.mode_set( mode = 'EDIT' )
        mesh.extra_faces_on(current_mesh_data, self, context)
        return {'FINISHED'}
    
    
class remove_interior_faces(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.remove_interior_faces"
    bl_label = "Remove interior faces"


    def execute(self, context):
        current_mesh = bpy.context.scene.objects[ 0 ]
        current_mesh_data = current_mesh.data
        bpy.ops.object.mode_set( mode = 'EDIT' )
        mesh.extra_faces_remove(current_mesh_data, self, context)
        return {'FINISHED'}

class replicated_vertices(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.replicated_vertices"
    bl_label = "Merge vertices"


    def execute(self, context):
        mesh.merge_verts(self, context)
        return {'FINISHED'}
   
   

#######################################   
#Connecting main script with curves.py
class curves_analysis_on(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.curves_analysis_on"
    bl_label = "Do curves analyse"


    def execute(self, context):
        mesh.merge_verts(self, context)
        curves.analyse_curves(self,context)
        return {'FINISHED'}


    
#######################################   
#Connecting main script with rendering.py

class denoising(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.denoising"
    bl_label = "Denoise data before rendering"


    def execute(self, context):
        rendering.denoise_data(context)
        return {'FINISHED'}


class face_orientation(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.face_orientation"
    bl_label = "Toggle face orientation showing"


    def execute(self, context):
        rendering.show_face_orientation(context)
        return {'FINISHED'}
    

class fix_face_orientation(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.fix_face_orientation"
    bl_label = "Reverse normals"


    def execute(self, context):
        rendering.reverse_normals(context)
        return {'FINISHED'}


class lighting(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "marta.lighting"
    bl_label = "Set studio lighting"


    def execute(self, context):
        rendering.set_lighting(self, context)
        return {'FINISHED'}
    


####################################################
#Creating buttons - defining look of all panel
#and assigning them appropriate functionalities


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Learn Computer Graphics"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        

#Mesh buttons
            
        layout.label(text="MESH ISSUES")
        
        # Gaps in mesh
        layout.label(text="Gaps in mesh:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.highlight_gaps")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.remove_gaps")
        
        
        #Additional faces within object
        layout.label(text="Additional faces within object:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.highlight_interior_faces")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.remove_interior_faces")
        
        #Replicated vertices
        layout.label(text="Replicated vertices:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.replicated_vertices")
        
        
        
       
#Curves buttons
        layout.label(text=" ")
        layout.label(text="CURVES ISSUES")
        
        # Too bent curves
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.curves_analysis_on")
        

#Rendering buttons
        layout.label(text=" ")
        layout.label(text="RENDERING")
        
        # Denoising
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.denoising")
        
        #Face orientation
        layout.label(text="Face orientation:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.face_orientation")

        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.fix_face_orientation")
       
        
        #Light 
        layout.label(text="Light settings:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("marta.lighting")
        
        

        
    

##############################################################

def register():
    bpy.utils.register_class(highlight_gaps)
    bpy.utils.register_class(remove_gaps)
    bpy.utils.register_class(highlight_interior_faces)
    bpy.utils.register_class(remove_interior_faces)
    bpy.utils.register_class(replicated_vertices)
    
    
    bpy.utils.register_class(curves_analysis_on)
    
    bpy.utils.register_class(denoising)
    bpy.utils.register_class(face_orientation)
    bpy.utils.register_class(fix_face_orientation)
    bpy.utils.register_class(lighting)
   
    bpy.utils.register_class(LayoutDemoPanel)


def unregister():
    bpy.utils.unregister_class(highlight_gaps)
    bpy.utils.unregister_class(remove_gaps)
    bpy.utils.unregister_class(highlight_interior_faces)
    bpy.utils.unregister_class(remove_interior_faces)
    bpy.utils.unregister_class(replicated_vertices)
    
    
    bpy.utils.unregister_class(curves_analysis_on)

    bpy.utils.unregister_class(denoising)
    bpy.utils.unregister_class(face_orientation)
    bpy.utils.unregister_class(fix_face_orientation)
    bpy.utils.unregister_class(lighting)

    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()
