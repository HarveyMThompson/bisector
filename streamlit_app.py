# -*- coding: utf-8 -*-
"""
Created on Sept 3 2025

@author: harveythompson
"""

import streamlit as st

bisector_page = st.Page("v1_josh_bisector.py", title="Bisector Search Method")
golden_page = st.Page("v1_josh_golden.py",title="Golden Search Method")
fibonacci_page = st.Page("v2_josh_fibonacci.py",title="Fibonacci Search Method")

pg = st.navigation([bisector_page, golden_page, fibonacci_page])
pg.run()