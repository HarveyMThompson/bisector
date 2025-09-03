# Python implementation of the Fibonacci algorithm for use in Streamlit
import numpy as np
import streamlit as st
# import streamlit_scrollable_textbox as stx - difficulties using within SCC
import matplotlib.pyplot as plt

# For creating the csv file
import sympy as sp
import time
import sys

###############################################################################
# Functions
###############################################################################

# define fiboinaccu functions
# Fibonacci algorithm
def create_fibonacci(N):
    
    # set Fibonacci sequence data
    fib=np.zeros(N+1)
    fib[0]=1
    fib[1]=2
    for i in range(1,N):
        fib[i+1]=fib[i]+fib[i-1]
    
    # set Fibonacci intervals
    rho=np.zeros(N)
    for i in range(N):
        rho[i]=1.0-fib[N-1-i]/fib[N-i]
    
    return rho

def fibonacci_calculation(a,b):
    
    # initial setup parameters
    N=st.session_state.niters    # number of Fibonacci terms
    rho=create_fibonacci(N)    # create Fibonacci sequeence
    a0=a    # left boundary
    b0=b     # right boundary
    L=b0-a0     # domain length
    
    # objective function
    obj = st.session_state.obj

    # store points and functions values
    xout = np.linspace(a,b,101)
    yout = obj(xout)

    outstr=''
    converged=0
    ncalls=0    # number of call to bisector
    xpts = []    # xiteration points
    fpts = []    # xiterations function values
    ncalls = 0
    for i in range(N):
        ncalls=ncalls+1
        a1=a0+rho[i]*(b0-a0)
        b1=b0-rho[i]*(b0-a0)
        fa0=obj(a0); fa1=obj(a1); fb0=obj(b0); fb1=obj(b1);
        outstr+=('iteration {0:5d} of fibonacci, rho = {1:10.5f} domain length = {2:10.5f}\n'.format(i+1,rho[i],np.abs(b0-a0)))
        outstr+=('a0={0:6.3f} f(a0)={1:6.3f}\n'.format(a0,fa0))
        outstr+=('a1={0:6.3f} f(a1)={1:6.3f}\n'.format(a1,fa1))
        outstr+=('b1={0:6.3f} f(b1)={1:6.3f}\n'.format(b1,fb1))
        outstr+=('b0={0:6.3f} f(b0)={1:6.3f}\n'.format(b0,fb0))
        if (fa1 < fb1):
            b0=b1
        else:
            a0=a1
        xpts.append(0.5*(a0+b0))
        fpts.append(obj(0.5*(a0+b0)))

    xmin=0.5*(a0+b0); fmin=obj(xmin)
    outstr+=('Fibonacci completed after = {0:5d} xmin={1:10.5f} fmin = {2:10.5f}\n'.format(N,xmin,fmin))
         
    # save dictionary data
    st.session_state.Calcs = outstr
    st.session_state.xout = xout
    st.session_state.yout= yout
    st.session_state.xpts= xpts
    st.session_state.fpts= fpts    
    st.session_state.xmin=xmin
    st.session_state.fmin=fmin
    st.session_state.ncalls = ncalls

    return xmin, fmin

# Function to create a plotting function
def create_plot():

    # Get current parameter values
    xmin = st.session_state.xmin
    fmin = st.session_state.fmin
    plt.figure()

    # Plot the objective function
    xout = st.session_state.xout
    yout = st.session_state.yout
    plt.plot(xout, yout, label='Objective Function')

    # Plot out the bisector points - NB always need to use 
    xpts = st.session_state.xpts
    fpts = st.session_state.fpts
    plt.scatter(xpts, fpts, label='Fibonacci Points', color='red', marker='x')
    
    xm = []
    fm = []
    xm.append(xmin)
    fm.append(fmin)
    # Plot the minimum point
    plt.scatter(xm, fm, label = 'Minimum point', color='blue', marker='o')

    # Configure plot details
    plt.ylabel('y')
    plt.xlabel('x')
    plt.title('Fibonacci Search on '+st.session_state.expression)
    plt.legend()
    return plt

# Function to create an animated plotting function
def animate_plot():

    # Get current parameter values
    xmin = st.session_state.xmin
    fmin = st.session_state.fmin
    plt.figure()

    # Plot the objective function
    xout = st.session_state.xout
    yout = st.session_state.yout
    plt.plot(xout, yout, label='Objective Function')

    # Plot out the bisector points
    xpts = st.session_state.xpts
    fpts = st.session_state.fpts
    
    # create a set of points with st.session_state.npts points in it
    # st.session_state.npts increases up to st.session_state.ncalls
    npts = st.session_state.npts - 1
    plt.scatter(xpts[0:npts], fpts[0:npts], label='Fibonacci Points', color='red', marker='x')
    
    xm = []
    fm = []
    xm.append(xmin)
    fm.append(fmin)
    # Plot the minimum point
    plt.scatter(xm, fm, label = 'Minimum point', color='blue', marker='o')

    # Configure plot details
    plt.ylabel('y')
    plt.xlabel('x')
    plt.title('Fibonacci Search on '+st.session_state.expression)
    plt.legend()
    return plt

###############################################################################
# Main program
###############################################################################

# st.set_page_config(layout='wide')

st.title("Fibonacci Algorithm Program")
st.write("This application enables you to experiment with fibonacci solution of 1-D equations")

st.write("Parameter settings")

# initialise the objective function
exp = st.text_input("Objective Function",value='7*x**2-20*x+22')
if exp is not None:
    expression = exp
else:
    expression = '7*x**2-20*x+22'
x = sp.symbols('x')

try:
    obj_function = sp.sympify(expression)
except Exception as e:
    st.error(f"An error occured using sympify: str{e}")
    st.stop()
    
try:
    obj = sp.lambdify(x, obj_function, 'numpy')
except Exception as e:
    st.error(f"An error occured using lambdify: str{e}")
    st.stop()
    
st.session_state.obj = obj
st.session_state.expression = expression

cols = st.columns([1,1,1])
minx = cols[0].number_input("Minimum x",-5.0,0.0,-2.0,0.1)
maxx = cols[1].number_input("Maximum x",0.0,5.0,2.0,0.1)
niters = cols[2].number_input("Number of Iterations",1,20,8,1)
st.session_state.niters = niters

cols2 = st.columns([1,1,1])
xmin,fmin = fibonacci_calculation(minx,maxx)

cols2[0].text("xmin="+"{:.4f}".format(xmin))
cols2[1].text("fmin="+"{:.4f}".format(fmin))

# plot out calculations
if 'plotgraph' not in st.session_state:
    st.session_state.plotgraph = 1
    if st.button("Plot Graph"):
        figplt = create_plot()
        st.pyplot(figplt)        
        # st.text(st.session_state.Calcs)
        st.write("Fibonacci Calculations")
        # stx.scrollableTextbox(st.session_state.Calcs,height=200)
else:
    figplt = create_plot()
    st.pyplot(figplt)        
    # st.text(st.session_state.Calcs)
    # st.write("Bisector Calculations")
    # stx.scrollableTextbox(st.session_state.Calcs,height=200)

# animate calculations
if st.button("Animate Graph"):
    st.session_state.npts = 1
    figplt = animate_plot()
    the_plot = st.pyplot(figplt)
    for i in range(st.session_state.ncalls-1):
        st.session_state.npts += 1
        time.sleep(0.5)
        figplt = animate_plot()
        the_plot.pyplot(figplt)        
