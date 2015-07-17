import sys
import os

# Get extend path
engine_path =  os.path.abspath(os.path.join(os.getcwd(), 'Ext'))
# # Load color log module
# colorlog_path = os.path.abspath(os.path.join(engine_path, 'colorlog'))
# sys.path.append(colorlog_path)

sys.path.append(engine_path)

