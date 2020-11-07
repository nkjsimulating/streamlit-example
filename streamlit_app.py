from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


# Dr Niraj Kumar Jha
# Date -  05th Nov

"""
"""
"""
Quarter-car response to road, tyre/wheel, and body inputs
©Dr. Niraj Kumar Jha
"""

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt



#st.title("Quarter-car response to road, tyre/wheel, and body inputs")

k_tyre = st.sidebar.number_input("tyre stiffness", value=10000, step=1000) # tire stiffness (N/m)
k_spring = st.sidebar.number_input("spring stiffness", value=1000, step=500)
damping_spring =st.sidebar.number_input("damping spring", value=350, step=50) ## tuned for comfort CS = 24.67
                                                                             # tuned for handling CS = 1897.9
m_sprung = st.sidebar.number_input("sprung mass", value=325, step=50)    # 1/4 sprung mass (kg)
m_unsprung = st.sidebar.number_input("unsprung mass", value=65, step=5)  # 1/4 unsprung mass (kg)

# find relevant quantities
CHI= m_unsprung/m_sprung
X0 = damping_spring/m_sprung  # CS/M
X1 = k_tyre/m_sprung  # - K1 - KT/M
X2 = k_spring/m_sprung # - K2 - KS/M
X3 = np.linspace(0,25,2500) #- F  - FREQUENCY

#Defining the function
A = X1 * X2
B = X1 * X0 * X3
C = CHI*pow(X3, 4)- (X1 + X2 * CHI + X2) * (pow(X3, 2)) + X1 * X2
D = X1 * X0 * X3 - (1 + CHI) * X0*pow(X3, 3)
# QCAR / TRANSMISSIBILITY - (A + Bj)/ (C + Dj) (Zdotdot/ Zrdotdot)
RE = ((A * C) + (B * D)) / (pow(C,2) + pow(D,2))
IM = ((B * C) - (A * D)) / (pow(C,2) + pow(D,2))
A_sprungtoroad = np.sqrt(pow(RE,2) + pow(IM,2))

# QCAR / TRANSMISSIBILITY - (A + Bj)/ (C + Dj) (Zdotdot/ (Fb/M))
A = CHI*pow(X3, 4) - (X1+X2) * X3 * X3
B = X0 * pow(X3, 3)
C = CHI*pow(X3, 4)- (X1 + X2 * CHI + X2) * (pow(X3, 2)) + X1 * X2
D = X1 * X0 * X3 - (1 + CHI) * X0*pow(X3, 3)
RE = ((A * C) + (B * D)) / (pow(C,2) + pow(D,2))
IM = ((B * C) - (A * D)) / (pow(C,2) + pow(D,2))
A_sprungtobody = np.sqrt(pow(RE,2) + pow(IM,2))

# QCAR / TRANSMISSIBILITY - (A + Bj)/ (C + Dj) (Zdotdot/ (Fw/M))
A = X2 * X3 * X3
B = X0 * pow(X3, 3)
C = CHI*pow(X3, 4)- (X1 + X2 * CHI + X2) * (pow(X3, 2)) + X1 * X2
D = X1 * X0 * X3 - (1 + CHI) * X0*pow(X3, 3)
RE = ((A * C) + (B * D)) / (pow(C,2) + pow(D,2))
IM = ((B * C) - (A * D)) / (pow(C,2) + pow(D,2))
A_sprungtowheel = np.sqrt(pow(RE,2) + pow(IM,2))

# Create the plot
fig = plt.figure(figsize = (10, 5))
plt.plot(X3, A_sprungtoroad,'r',linewidth=4)
plt.plot(X3, A_sprungtobody,'g',linewidth=4)
plt.plot(X3, A_sprungtowheel,'b',linewidth=4)

plt.legend(loc=0,fontsize = 'xx-large')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.ylabel('Response Gain', fontsize=18)
plt.xlabel('Frequency (Hz)', fontsize=18)


st.pyplot(plt)

