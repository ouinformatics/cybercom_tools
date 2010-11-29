#!/usr/bin/python
from INP_2_TECOf import getModelINP
import sys
RUN_ID = sys.argv[1]
MODEL_ID = sys.argv[2]
ConnSTR = sys.argv[3]
OUT_FILE = sys.argv[4]
f1 = getModelINP(RUN_ID,MODEL_ID,ConnSTR,OUT_FILE)

