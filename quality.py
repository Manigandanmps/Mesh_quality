import openmesh as om 
import numpy as np
import math
import matplotlib.pyplot as plt

#function to calculate the distance between two points
def distance (point1, point2):
    return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2 +(point2[2]-point1[2])**2)

#Calculate the minimum angle of the triangle 
def min_angle (length1, length2, length3 ):
    side1 = length1**2 #side square 
    side2 = length2**2
    side3 = length3**2
    # print (side1, side2, side3)

    alpha =math.acos((side2 + side3 - side1)/ (2*length2*length3))
    betta =math.acos((side1 + side3 - side2)/ (2*length1*length3))
    gamma =math.acos((side1 + side2 - side3)/ (2*length1*length2))

    # print (alpha, betta, gamma)
    alpha = alpha *(180/math.pi)
    betta = betta * (180/math.pi)
    gamma = gamma * (180/math.pi)
    # print (alpha, betta, gamma)
    theta_max = max(alpha, betta, gamma)
    theta_min = min(alpha, betta, gamma)
    theta_tri = 60.0

    min_angle = min(alpha, betta, gamma)
    # skewness = max ((theta_max - theta_tri)/(180 - theta_tri), (theta_min - theta_tri)/(180 - theta_tri) )

    return min_angle

#Calculate skewness of the triangle 
def skewness_fn (length1, length2, length3 ):
    side1 = length1**2 #side square 
    side2 = length2**2
    side3 = length3**2
    # print (side1, side2, side3)

    alpha =math.acos((side2 + side3 - side1)/ (2*length2*length3))
    betta =math.acos((side1 + side3 - side2)/ (2*length1*length3))
    gamma =math.acos((side1 + side2 - side3)/ (2*length1*length2))

    # print (alpha, betta, gamma)
    alpha = alpha *(180/math.pi)
    betta = betta * (180/math.pi)
    gamma = gamma * (180/math.pi)
    # print (alpha, betta, gamma)
    theta_max = max(alpha, betta, gamma)
    theta_min = min(alpha, betta, gamma)
    theta_tri = 60.0

    # min_angle = min(alpha, betta, gamma)
    skewness = max ((theta_max - theta_tri)/(180 - theta_tri), (theta_min - theta_tri)/(180 - theta_tri) )

    return skewness
#Calculate aspect ratio of the triangle 
def aspect_ratio_fn(length1, length2, length3):
    s = (length1 + length2 + length3) / 2.0
    return ((length1 * length2 * length3)/(8.0 * (s - length1)* (s - length2) * (s-length3)))

def aspect_ratio_fn2(length1, length2, length3):
    min_ = min(length1, length2, length3)
    max_ = max(length1, length2, length3)
    return ((max_/min_)/(math.sqrt(3)))

#load the stl 
my_mesh = om.read_trimesh("remeshed_hq1.stl")

#Printing number of vertices, edges and faces in the mesh 
print ("No of vertices: " + str(my_mesh.n_vertices()))
print ("No of edges: " + str(my_mesh.n_edges()))
print ("No of face: " + str(my_mesh.n_faces()))

indices = my_mesh.ev_indices() # mesh.edge_vertex_indices()
i = 0
edge_length = []
for i in range(len(indices)):
    for j in range (1):
        #get the vertex index of the edge and pass to the mesh.points() to get correspinding points
        point1 = my_mesh.point(my_mesh.vertex_handle(indices[i][j])) 
        point2 = my_mesh.point(my_mesh.vertex_handle(indices[i][j+1]))
        length = distance (point1, point2)
        edge_length.append(length)

indices = my_mesh.fv_indices()  # mesh.face_vertex_indices()
# print(indices)
i = 0
min_angle_ = []
aspect_ratio_ = []
aspect_ratio_2 = []
skewness_ =[]
for i in range(len(indices)):
    for j in range (1):
        #get the vertex index of the edge and pass to the mesh.points() to get correspinding points
        point1 = my_mesh.point(my_mesh.vertex_handle(indices[i][j])) 
        point2 = my_mesh.point(my_mesh.vertex_handle(indices[i][j+1]))
        point3 = my_mesh.point(my_mesh.vertex_handle(indices[i][j+2]))
        length1 = distance (point2, point3)
        length2 = distance (point1, point3)
        length3 = distance (point1, point2)
        # print (length1, length2, length3)
        min_angle_tri = min_angle(length1, length2, length3)
        min_angle_.append(min_angle_tri)
        # aspect_ratio_tri=aspect_ratio_fn(length1, length2, length3)
        # aspect_ratio_.append(aspect_ratio_tri)
        aspect_ratio_tri = aspect_ratio_fn2(length1, length2, length3)
        # print (aspect_ratio_tri)
        aspect_ratio_2.append(aspect_ratio_tri)
        skewness_tri = skewness_fn (length1, length2, length3 )
        skewness_.append(skewness_tri)
        
        
        


#edge length 
# print (len(edge_length))
print("max edge length of mesh: " + str(max(edge_length)))
print("min edge length of mesh: " + str(min(edge_length)))

# plt.style.use('ggplot')
plt.hist(edge_length, bins=1)
plt.show()

#triangle angle    
# print (len(min_angle_))
print ("60 is verygood and 0 is verybad")
print("max angle of mesh: " + str(max(min_angle_)))
print("min angle of mesh: " + str(min(min_angle_)))
# print(max(min_angle_))
# print(min(min_angle_))

# plt.style.use('ggplot')
plt.hist(min_angle_, bins=10)
plt.show()


# #Aspect ratio
# # print (len(aspect_ratio_))
# print("max aspect ratio of mesh: " + str(max(aspect_ratio_)))
# print("min aspect ratio of mesh: " + str(min(aspect_ratio_)))
# # print(max(aspect_ratio_))
# # print(min(aspect_ratio_))

# # plt.style.use('ggplot')
# plt.hist(aspect_ratio_, bins=10)
# plt.show()

#Aspect ratio
# print (len(aspect_ratio_))
print ("1 is verygood and perfect triangle")
print("max aspect ratio of mesh: " + str(max(aspect_ratio_2)))
print("min aspect ratio of mesh: " + str(min(aspect_ratio_2)))
# print(max(aspect_ratio_))
# print(min(aspect_ratio_))

# plt.style.use('ggplot')
plt.hist(aspect_ratio_2, bins=10)
plt.show()

#Aspect ratio
# print (len(aspect_ratio_))
print ("0 is verygood and 1 is verybad")
print("max skewness of mesh: " + str(max(skewness_)))
print("min skewness  of mesh: " + str(min(skewness_)))
# print(max(aspect_ratio_))
# print(min(aspect_ratio_))

# plt.style.use('ggplot')
plt.hist(skewness_, bins=1)
plt.show()


#Test internal angle 
# a= [0, 0, 0]
# b = [0, 1, 0]
# c =[1, 0, 0]
# length1 = distance (b, c)
# length2 = distance (a, c)
# length3 = distance (a, b)
# test = min_angle(length1, length2, length3)
# print (test)