import bpy
import bmesh
from mathutils import Vector

#Function selects gaps in mesh
def gaps_on(context):
    #If active mode is not edit mode, switch to edit mode
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.editmode_toggle()
    
    #Switch to vertex selection mode
    bpy.ops.mesh.select_mode(type='VERT')
    
    #Select holes in mesh
    bpy.ops.mesh.select_non_manifold()


#Function removes gaps in mesh 
def gaps_remove(context):
    #If active mode is not edit mode, switch to edit mode
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.editmode_toggle()
    
    #Switch to vertex selection mode
    bpy.ops.mesh.select_mode(type='VERT')
    
    #Select holes in mesh
    bpy.ops.mesh.select_non_manifold()
    
    #Add faces where holes are
    bpy.ops.mesh.edge_face_add()


#Function selects additional interior faces
def extra_faces_on(mesh_data, self, context):
    #Deselect everything
    bpy.ops.mesh.select_all(action='DESELECT')
    
    #Get the active mesh
    obj = bpy.context.edit_object
    mesh_data = obj.data

    bpy.ops.mesh.select_mode(type='FACE')
    camera_origin = Vector( ( 0, 0, 10 ) )
    
     # First do the built in selection
    bpy.ops.mesh.select_interior_faces()

    # Keep all indices in this selection
    indices = []
    
    #If we are in object mode switch it to edit mode
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.editmode_toggle()
    
    #Get a bmesh representation for our mesh data
    bm = bmesh.from_edit_mesh( mesh_data )
    bm.faces.active = None
    
    #Add counter to an iterable and return the enumerate object
    for index, face in enumerate( bm.faces ):
        if face.select:
            indices.append( ( index, face.calc_center_median_weighted() ) )

    # Deselect everything
    bpy.ops.mesh.select_all(action='DESELECT')


    # Switch to object mode to do scene raycasting
    bpy.ops.object.mode_set( mode = 'OBJECT' )
    outside = []
    view_layer = bpy.data.scenes["Scene"].view_layers["View Layer"]
    
    for index_data in indices:
        index = index_data[ 0 ]
        center = index_data[ 1 ]
        direction = center - camera_origin
        direction.normalize()

        # Cast a ray from the "camera" position to the face we think is interior
        result, location, normal, face_index, object, matrix = bpy.context.scene.ray_cast( view_layer, camera_origin, direction )

        if face_index == index:
            outside.append( face_index )

    # Build a list of interior faces that is compatible with built-it selection
    invisible_interior_faces = [ data[ 0 ] for data in indices if data[ 0 ] not in outside ]
    
    #Show result in the system console
    print( 'Selected ',len( invisible_interior_faces ),' interior faces' )
    
    #Show the result on the screen
    self.report({'INFO'}, "Selected " + str(len( invisible_interior_faces )) + " interior face(s).")

    # Select the faces
    if len( invisible_interior_faces ) > 0:

        for index in invisible_interior_faces:
            mesh_data.polygons[ index ].select = True
            
    #Set edit mode to show the results on the screen
    bpy.ops.object.mode_set( mode = 'EDIT' )
    bmesh.update_edit_mesh(mesh_data, True)

    
#Function removes additional interior faces  
def extra_faces_remove(mesh_data, self, context):
    
    #Deselect everything
    bpy.ops.mesh.select_all(action='DESELECT')
    
    
     # Get the active mesh
    obj = bpy.context.edit_object
    mesh_data = obj.data


    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(mesh_data)
    bm.faces.active = None

    
    #Count faces before selection
    faces_before = len(bm.faces)
    face_after = len(bm.faces)
    
    #Select interior faces
    extra_faces_on(mesh_data, self, context)

    
    # Delete faces if they are selected
    if len(context.selected_objects) > 0:
        bpy.ops.mesh.delete( type = 'FACE' )
        
     # Get the active mesh
    obj = bpy.context.edit_object
    mesh_data = obj.data


    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(mesh_data)
    bm.faces.active = None
    
    #Count faces after removal
    faces_after = len(bm.faces)
    faces_removed = faces_before - faces_after
    
    #Show info about removed faces    
    self.report({'INFO'}, "Removed " + str(faces_removed) + " interior face(s).")
    bmesh.update_edit_mesh(mesh_data, True)
    

#Function removes vertices that are replicated 
def merge_verts(self, context):
    #If active mode is not edit mode, switch to edit mode
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.editmode_toggle()
        
    #Select everything
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Get the active mesh
    obj = bpy.context.edit_object
    me = obj.data


    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None

    #Count vertices before removal
    nr_before = len(bm.verts)
    
    #Remove replicated vertices
    bpy.ops.mesh.remove_doubles()
    
    #Count vertices after removal
    nr_after = len(bm.verts)

    #Count how many vertices were removed
    amount_removed = nr_before - nr_after
    
    #Show info on the screen
    self.report({'INFO'}, "Removed " + str(amount_removed) + " additional vertice(s).")
    
    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    bmesh.update_edit_mesh(me, True)
    
    return {"FINISHED"}


