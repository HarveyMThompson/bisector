#!/usr/bin/env python
# coding: utf-8

# In[27]:


# Python implementation of the Bisector algorithm for use in Tkinter
import numpy as np
import streamlit as st
import streamlit_scrollable_textbox as stx
import matplotlib.pyplot as plt

# For creating the csv file
import sympy as sp

###############################################################################
# Functions
###############################################################################

# define bisector functions
def bisector_calculation(a,b,tol):
    
    L=b-a     # domain length
    dx=0.25*L    # step size reduction parameter
    x1=a+dx
    x0=a+2*dx
    x2=a+3*dx

    # objective function
    # obj = variables['Objective']
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
    while (converged==0):
        ncalls=ncalls+1
        fa=obj(a); f1=obj(x1); f0=obj(x0); f2=obj(x2); fb=obj(b);
        outstr+=('iteration {0:5d} of bisector search, domain length = {1:10.5f}\n'.format(ncalls,L))
        outstr+=('a={0:6.3f} f(a)={1:6.3f}\n'.format(a,fa))
        outstr+=('x1={0:6.3f} f(x1)={1:6.3f}\n'.format(x1,f1))
        outstr+=('x0={0:6.3f} f(x0)={1:6.3f}\n'.format(x0,f0))
        outstr+=('x2={0:6.3f} f(x2)={1:6.3f}\n'.format(x2,f2))
        outstr+=('b={0:6.3f} f(b)={1:6.3f}\n'.format(b,fb))
        if ((f2 > f0) and (f0 > f1)):
                b=x0
                x0=x1
        elif ((f2 < f0) and (f0 < f1)):
            a=x0
            x0=x2
        elif ((f1 > f0) and (f2 > f0)):
            a=x1
            b=x2
        else:
            outstr+=('Degenerate search - bisector test conditions not satisfied\n')
            sys.exit()
        
        # update bisector search positions
        xpts.append(0.5*(a+b))
        fpts.append(obj(0.5*(a+b)))
        L=0.5*L
        # check tolerance
        if (L < tol):
            converged=1
        else:
            dx=0.25*L
            x1=a+dx
            x0=a+2*dx
            x2=a+3*dx
                    
    # end while loop
                  
    xmin=0.5*(a+b); fmin=obj(xmin)
    outstr+=('search completed after = {0:5d} xmin={1:10.5f} fmin = {2:10.5f}\n'.format(ncalls,xmin,fmin))
    print('finished')
    
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
    
    # Get the current axis
    # plot2 = plt.figure(figsize=[8,8])  # NB plot2 needs to be different from plot1
    # plot2 = plt.figure()  # NB plot2 needs to be different from plot1
    #plt.figure(figsize=(6,6))
    plt.figure()

    # Plot the objective function
    xout = st.session_state.xout
    yout = st.session_state.yout
    plt.plot(xout, yout, label='Objective Function')

    # Plot out the bisector points - NB always need to use 
    xpts = st.session_state.xpts
    fpts = st.session_state.fpts
    plt.scatter(xpts, fpts, label='Bisector Points', color='red', marker='x')
    
    xm = []
    fm = []
    xm.append(xmin)
    fm.append(fmin)
    # Plot the minimum point
    plt.scatter(xm, fm, label = 'Minimum point', color='blue', marker='o')

    # Configure plot details
    plt.ylabel('y')
    plt.xlabel('x')
    plt.title('Bisector Search on '+st.session_state.expression)
    plt.legend()
    return plt

# Function to create an animated plotting function
def animate_plot():

    # Get current parameter values
    xmin = st.session_state.xmin
    fmin = st.session_state.fmin
    
    # Get the current axis
    # plot2 = plt.figure(figsize=[8,8])  # NB plot2 needs to be different from plot1
    # plot2 = plt.figure()  # NB plot2 needs to be different from plot1
    #plt.figure(figsize=(6,6))
    plt.figure()

    # Plot the objective function
    xout = st.session_state.xout
    yout = st.session_state.yout
    plt.plot(xout, yout, label='Objective Function')

    # Plot out the bisector points - NB always need to use 
    xpts = st.session_state.xpts
    fpts = st.session_state.fpts
    
    # create a set of points with st.session_state.npts points in it
    # st.session_state.npts increases up to st.session_state.ncalls
    npts = st.session_state.npts - 1
    plt.scatter(xpts[0:npts], fpts[0:npts], label='Bisector Points', color='red', marker='x')
    
    xm = []
    fm = []
    xm.append(xmin)
    fm.append(fmin)
    # Plot the minimum point
    plt.scatter(xm, fm, label = 'Minimum point', color='blue', marker='o')

    # Configure plot details
    plt.ylabel('y')
    plt.xlabel('x')
    plt.title('Bisector Search on '+st.session_state.expression)
    plt.legend()
    return plt

###############################################################################
# Main program
###############################################################################

# st.set_page_config(layout='wide')

st.title("Bisector Algorithm Program")
st.write("This application enables you to experiment with bisector solution of 1-D equations")

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
tol = cols[2].number_input("Tolerance",0.0001,0.1,0.01)

cols2 = st.columns([1,1,1])
xmin,fmin = bisector_calculation(minx,maxx,tol)

cols2[0].text("xmin="+"{:.4f}".format(xmin))
cols2[1].text("fmin="+"{:.4f}".format(fmin))

# plot out calculations
if 'plotgraph' not in st.session_state:
    st.session_state.plotgraph = 1
    if st.button("Plot Graph and Calculations"):
        figplt = create_plot()
        st.pyplot(figplt)        
        # st.text(st.session_state.Calcs)
        st.write("Bisector Calculations")
        stx.scrollableTextbox(st.session_state.Calcs,height=200)
else:
    figplt = create_plot()
    st.pyplot(figplt)        
    # st.text(st.session_state.Calcs)
    st.write("Bisector Calculations")
    stx.scrollableTextbox(st.session_state.Calcs,height=200)

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
