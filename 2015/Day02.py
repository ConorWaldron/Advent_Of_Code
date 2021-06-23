"""
Advent of Code 2015, Day 2

Part A Problem Description 
Calculate the amount of wrapping paper needed for all the presents on the list
for each present you need the surface area =2*L*W + 2*L*H +2*H*W
plus extra slack equal to the area of the smallest size

Part B Problem Description
Calculate how much ribbon needed for presents
need lenght equal to smallest perimeter of each box
and length for bow equal to cubic feet volume

"""

import time
start_time = time.time() #starts timer


#Import present dimension list. This requires the user to save the instructions
#as a text file called "Day2_input_2015.txt" in the same directory as the .py file
with open ("Day2_input_2015.txt", "r") as myfile:
    Present_Dimensions=myfile.readlines()
    
#Use the .split property of string to convert 'lxhxw' into 'l', 'h', 'w' 
#use int to convert string '3' to integer 3
List_dimensions = [(int(var.split('x')[0]), int(var.split('x')[1]), int(var.split('x')[2])) for var in Present_Dimensions] 

def Requirments_of_One_Present(Dimension_Tuple):
    Surface_Area = 2*(Dimension_Tuple[0]*Dimension_Tuple[1] + Dimension_Tuple[0]*Dimension_Tuple[2] + Dimension_Tuple[2]*Dimension_Tuple[1])
    Slack = Dimension_Tuple[0]*Dimension_Tuple[1]*Dimension_Tuple[2]/max(Dimension_Tuple)  #calculates area of smallest side
    Paper_Required = Surface_Area + Slack
    Smallest_Perimeter = 2*(Dimension_Tuple[0]+Dimension_Tuple[1]+Dimension_Tuple[2]-max(Dimension_Tuple))
    Volume = Dimension_Tuple[0]*Dimension_Tuple[1]*Dimension_Tuple[2]
    Ribbon_Required = Smallest_Perimeter + Volume
    return Paper_Required, Ribbon_Required

Total_Paper_Required = 0  #initilise paper required to 0
Total_Ribbon_Required = 0 #initilise ribbon required to 0

"""
#First method, requires function to be called twice per present
for var in List_dimensions:  #loop over all presents
    Total_Paper_Required += Requirments_of_One_Present(var)[0] #add paper for each present to total
    Total_Ribbon_Required += Requirments_of_One_Present(var)[1] #add paper for each present to total
"""

#Second method, only requires function to be called once per present
for var in List_dimensions:  #loop over all presents
    Paper_Ribbon_Required = Requirments_of_One_Present(var)
    Total_Paper_Required += Paper_Ribbon_Required[0]
    Total_Ribbon_Required += Paper_Ribbon_Required[1]

print('The total area of paper rquired is {} feet squared'.format(Total_Paper_Required))
print('The total length of ribbon rquired is {} feet'.format(Total_Ribbon_Required))


end_time = time.time()
duration = end_time - start_time
print('The code took {} milliseconds to execute'.format(1000*duration))