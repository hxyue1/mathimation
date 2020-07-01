"""
Todo:
    - add GitHub examples
    - Add dimensional arrows
    - Add and remove arrows
    - Moving matrices independently in batch
"""

from matplotlib import pyplot as plt
from matplotlib.text import Text
import numpy as np

class MatrixArtist:
    """Class to hold all the matplotlib.artist.Artist instances to plot a matrix
    
    Attributes:
        bbox (matplotlib.patches.Rectangle): Contains the perimeter.
        origin (tuple): (x,y) tuple for the bottom LH corner of the matrix        
    
    TODO: 
        - Update public attributes
    """
    def __init__(self, origin, width, height, data, rounding=3):
        """ Initialises instance of a MatrixArtist
        
        Args:
            origin (tuple): (x,y) tuple specifying the bottom LH corner of the matrix.
            width (int): how wide the matrix is to be.
            height (int): how tall the matrix is to be.
            data (two dimensional array): the input data for the matrix, can be a numpy array or list of lists.
            rounding (int): how many decimal places to round data to.
        """
        
        #Initialising perimeter
        self.bbox = plt.Rectangle(origin, width, height, ec='black', fc='white')
        self.origin = origin
        self.data=data
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
        """Draws all artists contained within the MatrixArtist instance on the givn axes.
        
        Args:
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
        
    def update_pos(self, coords, delta=False):
        """Updates the position of all artists contained within the MatrixArtist instance.
        
        Args:
            coords (tuple): (x,y) coordinates to either set the origin to or increment the origin by.
            delta (bool): if True increments origin by given coords, default is False.
        """
        
        #Updating origin and everything will follow
        if delta == True:
            dx = coords[0]
            dy = coords[1]
            self.origin = (self.origin[0] + dx, self.origin[1]+dy)
        elif delta == False:
            dx = coords[0] - self.origin[0]
            dy = coords[1] - self.origin[1]
            self.origin = coords
        
        
        #Updating bounding box
        self.bbox.set_xy((self.bbox.xy[0] + dx, self.bbox.xy[1] + dy))
        
        #Updating row markers
        for row in self.rows:
            x1, x2 = row.get_xdata()
            y1, y2 = row.get_ydata()
            x1 += dx
            x2 += dx
            y1 += dy
            y2 += dy
            
            row.set_data([x1, x2], [y1, y2])
            
        #Updating row markers
        for col in self.cols:
            x1, x2 = col.get_xdata()
            y1, y2 = col.get_ydata()
            x1 += dx
            x2 += dx
            y1 += dy
            y2 += dy
            
            col.set_data([x1, x2], [y1, y2])
        
        #Updating numbers
        for i in range(0,self.shape[0]):
            for j in range(0,self.shape[1]):
                x, y = self.nums[i][j].get_position()
                x += dx
                y += dy
                self.nums[i][j].set_position((x,y))
            
class BatchMatrixArtist:
    """Class to store a batch of MatrixArtists.
    
    The attributes for the batch object will be the same for all the MatrixArtists instances.
    
    Attributes:
        mats (list of MatrixArtists): A list of MatrixArtists which comprise the batch.
        displacement (tuple): (x,y) tuple to increment the origin of each MatrixArtist by from the first MatrixArtist in the batch.
    """
    def __init__(self, origin, width, height, data, displacement, rounding=3):
        mats = []
        
        #Looping through each matrix in the batch and initialising
        for b, matrix in enumerate(data):
            origin_temp = (origin[0]+displacement[0]*b, origin[1]+displacement[1]*b)
            mat = MatrixArtist(origin_temp, width, height, matrix, rounding)
            mats.append(mat)
        
        self.mats = mats
        self.origin = origin
        self.width = width
        self.height = height
        self.data = data
        self.shape = data.shape
        self.displacement = displacement
        
    def draw(self, ax):
        """Passes draw ax to each individual matrix
        
        Args:
            ax (matplotlib.axes.Axes): Instance of matplotlib.axes.Axes to draw the matrix onto.
            
        """
        for mat in self.mats:
            mat.draw(ax)
    
    def update_pos(self, coords, delta=False):
        """Passes args to each mat and excutes update_pos iteratively
        
        Args:
            coords (tuple): (x,y) coordinates to either set the origin to or increment the origin by.
            delta (bool): if True increments origin by given coords, default is False.
        """
        for mat in self.mats:
            mat.update_pos(coords, delta)
            