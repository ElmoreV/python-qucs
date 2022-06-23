import os

from qucs.wrapper import check_netlist_for_errors,run_simulation,load_netlist,load_netlist,save_run_and_load_modified_netlist
from qucs.extract import load_data
from qucs.netlist import serialize_netlist,deserialize_netlist 


user = '...' 

qucs_netlist_folder = r'C:\Users\'+user+r'\.qucs'
qucs_qucsator_folder = r'C:\Users\'+user+r'\Documents\qucs-0.0.19-win32-mingw482-asco-freehdl-adms\bin'



netlist_path = qucs_netlist_folder+os.sep+'netlist.txt'
output_path = r'C:\Users\'+user'+r'\outputs\sim.txt'


# Run original simulation and load data
check_netlist_for_errors(qucs_qucsator_folder,netlist_path)
run_simulation(qucs_qucsator_folder,netlist_path,output_path)
ds = load_data(output_path)


# Load netlist
netlist_content  = load_netlist(netlist_path)
netlist_dict = deserialize_netlist(netlist_content)
# Change netlist here
# netlist_dict['SP1']['Start']= '1 GHz'
netlist_modified = serialize_netlist(netlist_dict)

# Save and run new modified netlist simulation
new_netlist_path =  qucs_netlist_folder+os.sep+'netlist2.txt'
new_output_path =  r'C:\Users\'+user'+r'\outputs\sim3.txt'

results = save_run_and_load_modified_netlist(qucs_qucsator_folder,new_netlist_path,new_output_path,netlist_modified)
print(results)