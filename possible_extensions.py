# 1) Add random lines after rectangle creation
'''
# Add some random lines (draw any vertical or horizontal lines from somewhere where i > 0 to j > 0,
    #  if it is not adjacent to another parallel line). Lines should be drawn towards the middle
    coords = np.transpose(np.nonzero(bin)).tolist()
    coords.remove([0,0])
    coords.remove([bin_height - 1,0])
    coords.remove([0, bin_length - 1])
    coords.remove([bin_height - 1,  bin_length - 1])
    i_coords = random.choices(coords, k=10)

    for i_coord in i_coords:
        if i_coord[0] == 0 or i_coord[0] == (bin_height - 1):
            direction = 'vertical'
        elif i_coord[1] == 0 or i_coord[1] == (bin_length - 1):
            direction == 'horizontal'
        else:
            direction = random.choice(('horizontal', 'vertical'))
        if direction == 'horizontal':
            print(i_coord)
            # if right of midpoint or midpoint, go left until the next space is non-zero
            # else if left of midpoint, go right until next space is non-zero
            if i_coord[0] >= bin_height // 2:
                bin[i_coord] += 3
                current_coord = (i_coord[0] - 1, i_coord[1])
                while bin[current_coord] == 0:
                    bin[current_coord] += 4
                    current_coord = (current_coord[0] - 1, current_coord[1])
                bin[current_coord] += 3
            else:
                bin[i_coord] += 3
                current_coord = (i_coord[0] + 1, i_coord[1])
                while bin[current_coord] == 0:
                    bin[current_coord] += 4
                    current_coord = (current_coord[0] + 1, current_coord[1])
                bin[current_coord] += 3
            
        elif direction == 'vertical':
            # if above midpoint or midpoint, go down until the next space is non-zero
            # else if below midpoint, go up until next space is non-zero
            pass
'''