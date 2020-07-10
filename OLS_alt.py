import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import animation
import pandas as pd
import numpy as np
from scipy import linalg
import time

def dgp(n, m, c, x_domain, sigma):
    """
    Args:
        n (int): sample size.
        m (float): slope.
        c (float): intercept.
        x_domain (tuple): lb and upper bound of explanatory variable.
        sigma (float): 
    """
    X = np.ones((n,2))
    X[:,1] = np.random.uniform(x_domain[0], x_domain[1], n)
    X = np.matrix(X)
    
    betas = np.matrix([m, c]).T
    
    error = np.matrix(np.random.normal(0, sigma, n)).T
    
    y = X*betas + error
    
    return(y, X, betas, error)

np.random.seed(7)
y, X, betas, error = dgp(n=100, m=2, c=5, x_domain=(-10, 10), sigma=50)


#Initialising plot elements
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,8), gridspec_kw={'width_ratios': [5, 1]})
ax1.set_xlim(-12,12)
ax1.set_ylim(-150,150)
ax2.axis('off')

x_range = np.linspace(-12, 12, 100)
regression_line,  = ax1.plot(x_range, np.zeros(100), ls='--', color='black')

SSR_text = ax2.text(0.1, 0.8, '', fontsize=20)
n_text = ax2.text(0.1, 0.6, '', fontsize=20)


#List tracking true OLS coeficients 0,.., sample_size-1
OLS_coefs = []

#List tracking all fits at each frame 0,..,tot_frames-1
all_fits = []

def animate(frame):
    
    #For the first frame
    if frame == 1:
        y_temp = y[:1]
        X_temp = X[:1, :]
        
        #Updating and storing new fits
        OLS_coef = np.matrix([[y_temp[0,0]],[0]])
        current_fit = OLS_coef
        OLS_coefs.append(OLS_coef)
        all_fits.append(current_fit)
        
        #Adding first point
        ax1.scatter(np.array(X_temp[:,1]), np.array(y_temp[:]), color='black', s=10)
        
        #Drawing first fit
        y_hats = OLS_coef[0,0] + x_range*OLS_coef[1,0]
        regression_line.set_ydata(y_hats)
        
        #SSR calculation
        SSR_text.set_text('MSE: 0')
        n_text.set_text('n = 1')
                                
    elif frame > 1:
        
        #Getting current fit
        current_fit = all_fits[-1]
        desired_fit = OLS_coefs[-1]
        #Checking if current line matches up with OLS fit given all data
                  
        
        #If the current fit matches with the OLS estimate, we can add another point.
        if (current_fit == desired_fit).all():
            
            #Updating number of observations
            y_temp = y[:len(OLS_coefs)+1]
            X_temp = X[:len(OLS_coefs)+1]
            
            #Storing new OLS fit
            OLS_coef = np.linalg.inv(X_temp.T*X_temp)*X_temp.T*y_temp
            OLS_coefs.append(OLS_coef)
            
            #Updating scatter plot 
            ax1.scatter(np.array(X_temp[:,1]), np.array(y_temp[:]), color='black', s=10)
            
            #Updating text
            SSR = np.sum((np.array(y_temp - X_temp*OLS_coef))**2)/(len(y_temp))
            SSR_text.set_text('MSE: '+str(np.round(SSR, 3)))
            n_text.set_text('n = ' + str(len(y_temp)))
            
        else:
            y_temp = y[:len(OLS_coefs)+1]
            X_temp = X[:len(OLS_coefs)+1]
            
            #Incrementing slope and intercept to match desired fit
            slope_increment = np.sign(desired_fit[1,0]-current_fit[1,0])*0.1
            intercept_increment = np.sign(desired_fit[0,0]-current_fit[0,0])*1
            
            
            new_slope = current_fit[1,0] + slope_increment
            new_intercept = current_fit[0,0] + intercept_increment
            
            #When the slope is within a certain tolerance
            if abs(desired_fit[1,0]-current_fit[1,0]) < 0.5:                
                new_slope = desired_fit[1,0]
                #print('Slope within tolerance :', desired_fit[1,0]-current_fit[1,0])
            if abs(desired_fit[0,0]-current_fit[0,0]) < 1.5:
                new_intercept = desired_fit[0,0]
                #print('Intercept within tolerance :', desired_fit[0,0]-current_fit[0,0])
                
            #Updating the fit
            updated_fit = np.matrix([[new_intercept], [new_slope]])
            all_fits.append(updated_fit)
            
            #Redrawing the line
            y_hats = updated_fit[1,0]*x_range + updated_fit[0,0]
            regression_line.set_ydata(y_hats)
            
            #Updating text
            SSR = np.sum(np.array((y_temp - X_temp*updated_fit))**2)/(len(y_temp))
            SSR_text.set_text('MSE: '+ str(np.round(SSR, 3)))
            n_text.set_text('n = ' + str(len(y_temp)))
    return []

anim = animation.FuncAnimation(fig, animate,frames=200, interval=10000, blit=True)
Writer = animation.writers['ffmpeg']
writer = Writer(metadata=dict(artist='Me'), bitrate=1800, fps=8)
anim.save('OLS_animation.mp4', writer=writer)
    
