import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import ffmpeg

mat_loc = [0,0]
num_rows = 5
num_cols = 5
height = 200
width = height*(num_cols/num_rows)*1.5
cell_size = (width/num_cols, height/num_rows)

nums = np.random.uniform(-1,1,(num_rows,num_cols))

fig, ax = plt.subplots(figsize=(18,12))

ax.set_xlim([-10,600])
ax.set_ylim([-10,400])

#Adding perimeter for matrix
rectangle = plt.Rectangle((0, 0), width, height, ec='black', fc='white')
rect_xy = rectangle.xy
ax.add_patch(rectangle)

#For the row markers
row_markers = []
for i in range(0,num_rows-1):
    line = plt.Line2D((0,width), (cell_size[1]+i*cell_size[1],cell_size[1]+i*cell_size[1]), color = 'black', lw=1)
    row_markers.append(line)
    ax.add_line(line)

#For the column markers
col_markers = []
for i in range(0,num_cols-1):    
    line = plt.Line2D((cell_size[0]+i*cell_size[0],cell_size[0]+i*cell_size[0]), (0,height), color = 'black', lw=1)
    col_markers.append(line)
    ax.add_line(line)

#Offset from top LH corner of cell
cell_offset = (cell_size[0]/4, -2*cell_size[1]/3)
#Offset for negative values
neg_offset = -3.5

#Adding numbers
nums_text = [[] for i in range(0,num_rows)]
text_pos = [[] for i in range(0,num_rows)]
for i in range(0, num_rows):
    for j in range(0, num_cols):
        if nums[i,j]<0:
            x_pos = mat_loc[0]+cell_offset[0]+j*cell_size[0] + neg_offset
            y_pos = mat_loc[1] + height + cell_offset[1]-i*cell_size[1]
            text = ax.text(x_pos, y_pos, np.round(nums[i,j],2), fontsize=18)
            text_pos[i].append([x_pos, y_pos])
            nums_text[i].append(text)
        elif nums[i, j]>=0:
            x_pos = mat_loc[0]+cell_offset[0]+j*cell_size[0]
            y_pos = mat_loc[1] + height + cell_offset[1]-i*cell_size[1]
            text = ax.text(x_pos, y_pos, np.round(nums[i,j],3), fontsize=18)
            text_pos[i].append([x_pos, y_pos])
            nums_text[i].append(text)

# animation function.  This is called sequentially
def animate(frame):
        
    #Updating position of perimeter
    rectangle.set_xy((rectangle.xy[0] + 1, rectangle.xy[1]))
    
    #Updating positions for row and col markers
    for i in range(0, num_rows-1):
        row_pos = row_markers[i].get_xydata()
        row_markers[i].set_data(row_pos[:,0]+1, row_pos[:,1])
        
    #Updating positions for row and col markers
    for i in range(0, num_cols-1):
        col_pos = col_markers[i].get_xydata()
        col_markers[i].set_data(col_pos[:,0]+1, col_pos[:,1])
            
    #Updating position for text
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            #Getting position of current text
            text_pos = nums_text[i][j].get_position()
            #Updating position
            nums_text[i][j].set_position((text_pos[0]+1, text_pos[1]))
            
    return []


anim = animation.FuncAnimation(fig, animate, #init_func=init,
                               frames=200, interval=20000000000, blit=True)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=64, metadata=dict(artist='Me'), bitrate=1800)
anim.save('basic_animation.mp4', writer=writer)

plt.show()

