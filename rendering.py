import bpy
import mathutils

#Function denoises image and also changes render engine to Cycles
def denoise_data(context):
    #Change render engine to Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    
    #Check an option with denoising in properties
    bpy.context.scene.view_layers['View Layer'].cycles.denoising_store_passes = True

    #Change number of samples from 128 to 64
    #Aim is to adjust settings for less efficient computers
    bpy.context.scene.cycles.samples = 64
    
    #Enable nodes usage
    bpy.context.scene.use_nodes = True
    
    #Deletes existing nodes
    nodesField = bpy.context.scene.node_tree
    for currentNode in nodesField.nodes:
        nodesField.nodes.remove(currentNode)
    
    #Add, place, connect nodes which denoise image
    node_tree = bpy.context.scene.node_tree
    node_1 = node_tree.nodes.new("CompositorNodeRLayers")
    node_1.location = (-470, 440)
    node_2 = node_tree.nodes.new("CompositorNodeDenoise")
    node_2.location = (40, 440)
    node_3 = node_tree.nodes.new("CompositorNodeComposite")
    node_3.location = (530, 440)
    node_tree.links.new(node_1.outputs["Noisy Image"], node_2.inputs[0])
    node_tree.links.new(node_1.outputs["Denoising Normal"], node_2.inputs[1])
    node_tree.links.new(node_1.outputs["Denoising Albedo"], node_2.inputs[2])
    node_tree.links.new(node_2.outputs["Image"], node_3.inputs[0])
   

#Function shows face orientation
def show_face_orientation(context):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.overlay.show_face_orientation = not space.overlay.show_face_orientation
                    break


#Function reverses normals
#what changes face orientation
def reverse_normals(context):
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.flip_normals()


#Function removes lights
#Function used while light setting
def remove_lights():
    #If active mode is edit mode switch to object mode
    if bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()
        
    #Select lights and remove them
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete(use_global=False, confirm=False)


#Function sets lighting
#Function adjusts distance for objects sizes
def set_lighting(self, context):
    #If active mode is edit mode switch to object mode
    if bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()
        
    #Apply transformations: location, rotation, scale
    bpy.ops.object.select_by_type(type='MESH')
    bpy.context.space_data.context = 'SCENE'
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    
    #Initialize maximal distances from planes
    max_distance_X = 0
    max_distance_Y = 0
    max_distance_Z = 0
    
    #Initialize minimal distances from planes 
    min_distance_X = 0
    min_distance_Y = 0
    min_distance_Z = 0
    
    #Initialize planes normals
    plane_no_X = mathutils.Vector((1.0, 0.0, 0.0))
    plane_no_Y = mathutils.Vector((0.0, 1.0, 0.0))
    plane_no_Z = mathutils.Vector((0.0, 0.0, 1.0))
    
    #Initialize planes coordinates
    plane_co_XZ = mathutils.Vector((1.0, 0.0, 1.0))
    plane_co_YZ = mathutils.Vector((0.0, 1.0, 1.0))
    plane_co_XY = mathutils.Vector((1.0, 1.0, 0.0))
    
    #Initialize temporary distance for each axis
    distance_X = 0
    distance_Y = 0
    distance_Z = 0
    
    #If active mode is edit mode switch to object mode
    if bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()
    
    #Select all objects and save them
    bpy.ops.object.select_by_type(type='MESH')
    my_objects = context.selected_objects
    
    #Count selected objects
    how_many = len(context.selected_objects)
    
    #Go thru all objects and their vertices
    for obj in my_objects:
        for v in obj.data.vertices:
            #Calculate maximal and minimal distance
            #From vertex on Y axis to XZ plane
            point = v.co
            distance_Y = mathutils.geometry.distance_point_to_plane(point, plane_co_XZ, plane_no_Y)
            if distance_Y > max_distance_Y:
                max_distance_Y = distance_Y 
            if distance_Y < min_distance_Y:
                min_distance_Y = distance_Y
            
            #Calculate maximal and minimal distance
            #From vertex on X axis to YZ plane
            distance_X = mathutils.geometry.distance_point_to_plane(point, plane_co_YZ, plane_no_X)
            if distance_X > max_distance_X:
                max_distance_X = distance_X
            if distance_X < min_distance_X:
                min_distance_X = distance_X
            
            #Calculate maximal and minimal distance
            #From vertex on Z axis to XY plane
            distance_Z = mathutils.geometry.distance_point_to_plane(point, plane_co_XY, plane_no_Z)
            if distance_Z > max_distance_Z:
                max_distance_Z = distance_Z
            if distance_Z < min_distance_Z:
                min_distance_Z = distance_Z

        
    #Find view matrix 
    for s in bpy.context.window.screen.areas:
            if s.type=="VIEW_3D":
                break
    v_mat = s.spaces[0].region_3d.view_matrix
    
    
    #Calculate medium distances for each axis
    medium_X = 0.5 * (min_distance_X + max_distance_X)
    medium_Y = 0.5 * (min_distance_Y + max_distance_Y)
    medium_Z = 0.5 * (min_distance_Z + max_distance_Z)
    
    #Initialize variable informing if light is on the scene
    light_is_here = False
    
    
    #################################################
    #Set lights for one selected Orthographic View 
    
    #Right Orthographic
    if v_mat[0].y == 1.0000 and v_mat[2].x == 1.0000:
        remove_lights()
        light_1 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 2.5, min_distance_Y * 1.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_2 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 3.5, medium_Y, max_distance_Z * 2), scale=(1, 1, 1))
        light_3 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 2.5, max_distance_Y * 1.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_is_here = True
        
    #Left Orthographic
    if v_mat[0].y == -1.0000 and v_mat[2].x == -1.0000:
        remove_lights()
        light_1 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 2.5, max_distance_Y * 1.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_2 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 3.5, medium_Y, max_distance_Z * 2), scale=(1, 1, 1))
        light_3 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 2.5, min_distance_Y * 1.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_is_here = True

    #Front Orthographic
    if v_mat[0].x == 1.0000 and v_mat[2].y == -1.0000001192092896:
        remove_lights()
        light_1 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 1.5, min_distance_Y * 2.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_2 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(medium_X, min_distance_Y * 3.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_3 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 1.5, min_distance_Y * 2.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_is_here = True

    #Back Orthographic
    if v_mat[0].x == -1.000000238418579 and v_mat[2].y == 1.0000001192092896:
        remove_lights()
        light_1 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 1.5, max_distance_Y * 2.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_2 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(medium_X, max_distance_Y * 3.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_3 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 1.5, max_distance_Y * 2.5, max_distance_Z * 2), scale=(1, 1, 1))
        light_is_here = True

    #Top Orthographic
    if v_mat[1].y == 1.0000 and v_mat[2].z == 1.0000:
        remove_lights()
        light_1 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 1.5, max_distance_Y * 2, max_distance_Z * 2.5), scale=(1, 1, 1))
        light_2 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(medium_X, max_distance_Y * 2, max_distance_Z * 3.5), scale=(1, 1, 1))
        light_3 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 1.5, max_distance_Y * 2, max_distance_Z * 2.5), scale=(1, 1, 1))
        light_is_here = True

    #Bottom Orthographic
    if v_mat[1].y == -1.0000 and v_mat[2].z == -1.0000:
        remove_lights()
        light_1 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(min_distance_X * 1.5, min_distance_Y * 2, min_distance_Z * 2.5), scale=(1, 1, 1))
        light_2 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(medium_X, min_distance_Y * 2, min_distance_Z * 3.5), scale=(1, 1, 1))
        light_3 = bpy.ops.object.light_add(type='POINT', align='WORLD', location=(max_distance_X * 1.5, min_distance_Y * 2, min_distance_Z * 2.5), scale=(1, 1, 1))  
        light_is_here = True
        
    #Check if light is added
    if light_is_here == True:
        bpy.data.lights["Point"].energy = 70
        bpy.data.lights["Point.001"].energy = 70
        bpy.data.lights["Point.002"].energy = 70
    else:
        #If Orthographic View was not set
        #Show info asking to set one of 6 Orthographic Views
        self.report({'INFO'}, "Set Orthographic View before Set studio lighting function.")
        
              
         
    
    
    