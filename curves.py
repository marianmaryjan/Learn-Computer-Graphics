import bpy
import bmesh
import mathutils
from collections import defaultdict
from learn_computer_graphics import mesh

#Function does curves analysis 
#assigns colors to vertices basing on curvature
def analyse_curves(self, context):  
    ####################################
    #At first it is necessary to remove additional vertices
    #It is to avoid situation when distance between 2 vertices is zero 
    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.editmode_toggle()
    #Select everything
    bpy.ops.mesh.select_all(action='SELECT')
    #Remove additional vertices
    mesh.merge_verts(self, context)
    bpy.ops.object.editmode_toggle()
    ####################################
    #If active mode is edit mode, switch to object mode
    if bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()
        
    #Check if any object is selected 
    #If not, show info to select an object 
    if not context.selected_objects:
        self.report({'INFO'}, "Select an object to analyse.")
    else:
        #Get the active mesh
        obj = context.selected_objects[0]
        mesh_active = obj.data
        
        #Assign to active or create new color layer
        if mesh_active.vertex_colors:
            color_layer = mesh_active.vertex_colors.active
        else:
            color_layer = mesh_active.vertex_colors.new()

        #Get the bmesh representation
        bm = bmesh.new()
        bm.from_mesh(bpy.context.active_object.data)
        bm.edges.ensure_lookup_table()
        
        #Initialize median, maximal and minimal curvature
        median = 0
        max = -2
        min = 2
        
        #Initialize dictionaries 
        e_dict = defaultdict(list)
        v_dict = defaultdict(list)
        c_dict = defaultdict(float)
        
        #Create dictionary with vertices indices and loops indices
        for f in bm.faces:
            for v_ix, l_ix in zip(f.verts, f.loops):
                v_dict[v_ix.index].append(l_ix.index)       
        print(v_dict)
               
        #Create dictionary with edges indices and its faces     
        for f in bm.faces:
            for e in f.edges:
                e_dict[e.index].append(f)    
        print(e_dict)
        
        #Go thru edges end calculate curvature
        for e in bm.edges:
            #For each edge save its normals and coordinates to variables
            p1 = e.verts[0].co
            p2 = e.verts[1].co
            n1 = e.verts[0].normal
            n2 = e.verts[1].normal
            
            #Calculate curvature
            curvature = (n2 - n1).dot(p2 - p1)
            curvature = curvature / (p2 - p1).length
            median += curvature
            
            #Save calculated curvature in dictionary
            #Curvature is assigned to edge
            c_dict[e.index] = curvature
            
            #Calculate maximal and minimal curvature
            if curvature > max: max = curvature
            if curvature < min: min = curvature
                
        #Calculate median curvature
        median = median/len(bm.edges)
        
        #Show info in system console
        print("Median: ", median)
        print("Maximal curvature: ", max)
        print("Minimal curvature: ", min)
        
        
        #Go thru dictionaries to get vertex and his loop indices
        #Paint them green - littlest values of curvature
        for e in bm.edges:
            curvature = c_dict[e.index]
            for v in e.verts: 
                for f in e_dict[e.index]:
                    for l in f.loops:
                        if l.index in v_dict[v.index]:
                           color_layer.data[l.index].color = (0, 1.0, 0, 1.0)
                          
                                
        #Go thru dictionaries to get vertex and his loop indices
        #Paint them yellow                      
        for e in bm.edges:
            curvature = c_dict[e.index]
            for v in e.verts:
                for f in e_dict[e.index]:
                    for l in f.loops:
                        if l.index in v_dict[v.index]:   
                            if abs(curvature) > (0.3) and abs(curvature) <= (0.7):
                                color_layer.data[l.index].color = (1.0, 1.0, 0, 1.0)
          
        #Go thru dictionaries to get vertex and his loop indices
        #Paint them orange                     
        for e in bm.edges:
            curvature = c_dict[e.index]
            for v in e.verts:
                for f in e_dict[e.index]:
                    for l in f.loops:
                        if l.index in v_dict[v.index]:  
                            if abs(curvature) > (0.7) and abs(curvature) <= (1.2):
                                color_layer.data[l.index].color = (1.0, 0.5, 0, 1.0)

                                
        #Go thru dictionaries to get vertex and his loop indices
        #Paint them red - biggest values of curvature                   
        for e in bm.edges:
            curvature = c_dict[e.index]
            for v in e.verts:
                for f in e_dict[e.index]: 
                    for l in f.loops:
                        if l.index in v_dict[v.index]:   
                            if abs(curvature) > (1.2) and abs(curvature) <= (2):
                                color_layer.data[l.index].color = (1.0, 0, 0, 1.0)                   
        
        
        #Switch active mode to Vertex Paint
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')

        
             