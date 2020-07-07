import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib import animation

#Rotation function
def rotation(coef, rot_origin, angle):
    """
    Args:
        coef (tuple): tuple of floats (m, c) representing the slope and intercept of the line to be rotated.
        rot_orgin (tuple): tuple of floats representing the origin which 'point' is rotated around.
        angle (float): angle of rotation (clockwise direction) in radians.
        
    Returns (tuple): tuple of floats representing the slope and the intercept of the rotated line (m', c').
        
    """
    
# =============================================================================
#     x_new = (point[0]-rot_origin[0])*np.cos(angle) + (point[1]-rot_origin[1])*np.sin(angle)+rot_origin[0]
#     y_new = -(point[0]-rot_origin[0])*np.sin(angle) + (point[1]-rot_origin[1])*np.cos(angle)+rot_origin[1]
# =============================================================================
    d = 1
    x1 = d/np.sqrt(coef[0]**2+1)+rot_origin[0]
    y1 = coef[0]*x1 + coef[1]
    
    x_new = (x1-rot_origin[0])*np.cos(angle) + (y1-rot_origin[1])*np.sin(angle)+rot_origin[0]
    y_new = -(x1-rot_origin[0])*np.sin(angle) + (y1-rot_origin[1])*np.cos(angle)+rot_origin[1]
    
    #m = (y2-y1)/(x2-x1)
    m_new = (y_new-rot_origin[1])/(x_new-rot_origin[0])
    
    #c = y -mx
    c_new = rot_origin[1] - m_new*rot_origin[0]

    return((m_new, c_new))

(x0, y0) = (1,1)
coef0 = [1,0]
fig, ax = plt.subplots(figsize=(8,8))
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
coefs = [coef0]



x_range = np.linspace(-20, 20, 100)
y_range = coef0[0]*x_range + coef0[1]



line,  = ax.plot(x_range, y_range)

tot_frames = 128
    
def animate(frame):
    
    if frame == 0:
        ax.scatter(x0,y0)
        line.set_data(x_range, y_range)
        
    elif frame > 0:
        angle = -np.pi/tot_frames
        print(coefs[frame-1], frame)
        (m_new, c_new) = rotation(coefs[frame-1], (x0, y0), angle)
        y_data = m_new*x_range + c_new
        
        line.set_ydata(y_data)
    
        #Updating stored slope and intercept
        coefs.append([m_new, c_new])
    return []

anim = animation.FuncAnimation(fig, func=animate, frames=tot_frames, blit=True)
Writer = animation.writers['ffmpeg']
writer = Writer(metadata=dict(artist='Me'), fps=128, bitrate=1800)
anim.save('line_rotation.mp4', writer=writer)