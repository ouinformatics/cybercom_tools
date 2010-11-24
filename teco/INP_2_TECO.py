#!/usr/bin/python
from db_push import getModelINP
import sys
RUN_ID = sys.argv[1]
MODEL_ID = sys.argv[2]
OUT_FILE = sys.argv[3]
f1 = getModelINP(RUN_ID,MODEL_ID,OUT_FILE)

