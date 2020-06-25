#Need to work on updating and incrementing position of artists
from matplotlib import pyplot as plt
from matplotlib.text import Text
import numpy as np

class MatrixArtist:
    def __init__(self, origin, width, height, data, rounding=3):
        
        #Initialising perimeter
        self.bbox = plt.Rectangle(origin, width, height, ec='black', fc='white')
        self.origin = origin
        self.shape = data.shape
        self.cell_size = (width/self.shape[1], height/self.shape[0])        
        self.text_offset = (self.cell_size[0]/4, -2*self.cell_size[1]/3)
        self.neg_offset = -3.5
        self.rounding = rounding
        
        #Initialising rows as artists and storing in a list
        rows = []
        for i in range(0, self.shape[0]-1):
            #Height offset from top of bbox
            y_offset = height-self.cell_size[1]*(i+1)
            row = plt.Line2D((origin[0],origin[0]+width), (origin[1] + y_offset, origin[1] + y_offset), color='black', lw=1, zorder=1)
            rows.append(row)
        self.rows = rows
        
        #Initialising cols as artists and storing in a list
        cols = []
        for i in range(0, self.shape[1]-1):
            #width offset from left of bbox
            x_offset = self.cell_size[0]*(i+1)
            col = plt.Line2D((origin[0] + x_offset, origin[0] + x_offset), (origin[1], origin[1] + height), color='black', lw=1, zorder=1)
            cols.append(col)
        self.cols = cols
            
        #Initialising text as artists and storing in a list of list
        nums = [[] for i in range(self.shape[0])]
        for i in range(0, self.shape[0]):
            for j in range(0, self.shape[1]):
                #Adjusting for negative numbers
                x_pos = origin[0]+self.text_offset[0] + self.cell_size[0]*j+self.neg_offset
                y_pos = origin[1]+height+self.text_offset[1] - self.cell_size[1]*i
                if data[i][j] < 0:
                    text_temp = Text(x_pos, y_pos, np.round(data[i][j], self.rounding), zorder=1)
                    text_temp.set_bbox(dict(alpha=1, facecolor='white' , edgecolor='white'))
                    nums[i].append(text_temp)
                elif data[i][j] >= 0:
                    text_temp = Text(x_pos + self.neg_offset, y_pos, np.round(data[i][j], self.rounding), zorder=1)
                    text_temp.set_bbox(dict(alpha=1, facecolor='white' , edgecolor='white'))
                    nums[i].append(text_temp)
        self.nums=nums
 
    def draw(self, ax):
        """
        ax (matplotlib.axes.Axes): Instance of matplotlib.axes.Axes to draw the matrix onto.
        """
        #Drawing bounding box
        ax.add_artist(self.bbox)
        
        #Drawing rows and columns
        for row in self.rows:
            ax.add_artist(row)
        for col in self.cols:
            ax.add_artist(col)
        
        #Drawing numbers
        for row in self.nums:
            for text in row:
                ax.add_artist(text)
        
        return(ax)
        
    def update_pos(self, coords):
        
        #Updating origin and everything will follow
        self.origin=coords
        
        self.bbox.set_xy(coords)
        