# GENERATES A SET OF RECTANGLES FROM A LABEL
# def generate_from_label(LABEL, BIN_WIDTH=150, BIN_HEIGHT=100, NUM_RECTANGLES=20):
#     # Label = 8-tuple: 4 areas, 3 heights
#     bin_area = BIN_HEIGHT * BIN_WIDTH
#     items = []

#     assignment_matrix = np.zeros((4,3))
#     # Define legal boxes of matrix of height categories vs area categories
#     for i in range(12):
#         height_category = i % 3
#         area_category = i // 3
#         if height_category == 0:
#             min_height = 1
#             max_height = math.floor(BIN_HEIGHT/3)
#         elif height_category == 1:
#             min_height = math.floor(BIN_HEIGHT/3) + 1
#             max_height = math.floor(BIN_HEIGHT/2)
#         else:
#             min_height = math.floor(BIN_HEIGHT/2) + 1
#             max_height = BIN_HEIGHT
#         if area_category == 0:
#             min_area = 1
#             max_area = math.floor(bin_area/4)
#         elif area_category == 1:
#             min_area = (math.floor(bin_area/4) + 1)
#             max_area = math.floor(bin_area/3)
#         elif area_category == 2:
#             min_area = (math.floor(bin_area/3) + 1)
#             max_area = math.floor(bin_area/2)
#         else:
#             min_area = (math.floor(bin_area/2) + 1)
#             max_area = bin_area

#         min_width = min_area/max_height
#         max_width = max_area/min_height        
#         if 100 >= min_width and 1 <= max_width:
#             assignment_matrix[area_category][height_category] = 1

#     # Decide how many rectangles to assign to each box
#     a0, a1, a2 = math.floor(LABEL[0]* NUM_RECTANGLES), math.floor(LABEL[1]* NUM_RECTANGLES), math.floor(LABEL[2]* NUM_RECTANGLES)
#     a3 =  NUM_RECTANGLES - a0 - a1 - a2

#     h0, h1 = math.floor(LABEL[4]* NUM_RECTANGLES), math.floor(LABEL[5]* NUM_RECTANGLES)
#     h2 = NUM_RECTANGLES - h0 - h1

#     print(assignment_matrix)
#     breakloop = False
#     for area_index in range(3,-1,-1):
#         if breakloop:
#             break
#         for height_index in range(2,-1,-1):
#             if assignment_matrix[area_index][height_index] == 0:
#                 continue
#             else:
#                 # check if it is only value in row
#                 if assignment_matrix[area_index][(height_index+1)%3] == 0 and assignment_matrix[area_index][(height_index-1)%3] == 0:
#                     if area_index == 0:
#                         assignment_matrix[area_index][height_index] = a0
#                     elif area_index == 1:
#                         assignment_matrix[area_index][height_index] = a1
#                     elif area_index == 2:
#                         assignment_matrix[area_index][height_index] = a2
#                     else:
#                         assignment_matrix[area_index][height_index] = a3

#                 # check if it is only value in column (since this may be an indication of an error)
#                     if assignment_matrix[(area_index+1)%4][height_index] == 0 and assignment_matrix[(area_index-1)%4][height_index] == 0:
#                         if height_index == 0:
#                             height_value = h0
#                         elif height_index == 1:
#                             height_value = h1
#                         else:
#                             height_value = h2

#                         if area_index == 0:
#                             area_value = a0
#                         elif area_index == 1:
#                             area_value = a1
#                         elif area_index == 2:
#                             area_value = a2
#                         else:
#                             area_value = a3

#                         if height_value != area_value:
#                             breakloop = True
#                             break
    
#                 # check if it is only value in column    
#                 elif assignment_matrix[(area_index+1)%4][height_index] == 0 and assignment_matrix[(area_index-1)%4][height_index] == 0:
#                     if area_index == 0:
#                         assignment_matrix[area_index][height_index] = a0
#                     elif area_index == 1:
#                         assignment_matrix[area_index][height_index] = a1
#                     elif area_index == 2:
#                         assignment_matrix[area_index][height_index] = a2
#                     else:
#                         assignment_matrix[area_index][height_index] = a3

        
# generate_from_label((1/2, 1/3, 1/12, 1/12, 1/3, 1/3, 1/3, 1), NUM_RECTANGLES=100)