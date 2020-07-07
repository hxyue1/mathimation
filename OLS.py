import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import animation
import pandas as pd
import numpy as np
import time

fig, ax = plt.subplots(figsize=(8,6))

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

y, X, betas, error = dgp(n=50, m=2, c=5, x_domain=(-10, 10), sigma=50)

plt.scatter(np.array(X[:,1]), np.array(y[:]), color='black', s=5)

x_dgp = np.linspace(-10, 10, 100)
y_dgp = betas[0,0] + x_dgp*betas[1,0]
ax.plot(x_dgp, y_dgp, color='black')

beta_hats = np.linalg.inv(X.T*X)*X.T*y
y_hat = beta_hats[0,0] + x_dgp*beta_hats[1,0]
OLS_fit = Line2D(x_dgp, y_hat, ls='--', color='black')
ax.add_artist(OLS_fit)

def animate(frame):
    
    if frame > 1:
        y_frame = y[:frame]
        X_frame = X[:frame, :]
        ax.cla()
        ax.scatter(np.array(X_frame[:,1]), np.array(y_frame[:]))
        beta_hats = np.linalg.inv(X_frame.T*X_frame)*X_frame.T*y_frame
        y_hat = beta_hats[0,0] + x_dgp*beta_hats[1,0]
        OLS_fit = Line2D(x_dgp, y_hat, ls='--', color='black')
        ax.add_artist(OLS_fit)
    return []

anim = animation.FuncAnimation(fig, animate,frames=50, interval=10000, blit=True)
Writer = animation.writers['ffmpeg']
writer = Writer(metadata=dict(artist='Me'), bitrate=1800)
anim.save('OLS_animation.mp4', writer=writer)
    