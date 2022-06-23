import os


def check_netlist_for_errors(qucs_qucsator_folder,netlist_path):
    '''
    Uses qucsator through the command line to check if the (modified) netlist is valid.
    '''
    if not os.path.exists(qucs_qucsator_folder+'\qucsator.exe'):
        raise FileNotFoundError('Wrong qucsator folder')
        
    if not os.path.exists(netlist_path):
        raise FileNotFoundError('Could not find netlist')

    ret_code = os.system('%s\qucsator -c -i %s'%(qucs_qucsator_folder,netlist_path))
    if ret_code==False:
        # print('Netlist OK')
        return True
    else:
        # print('Netlist not compatible')
        return False

    
def run_simulation(qucs_qucsator_folder,netlist_path,output_path):
    '''
    Runs qucsator to simulate the netlist and save the output at output_path.
    Return 0 if the program is successful. 
    '''
    if not os.path.exists(qucs_qucsator_folder+'\qucsator.exe'):
        raise FileNotFoundError('Wrong qucsator folder')
    if not os.path.exists(netlist_path):
        raise FileNotFoundError('Could not find netlist')


    ret_code = os.system('%s\qucsator -i %s -o %s'%(qucs_qucsator_folder,netlist_path,output_path))
    print(ret_code)
    if not os.path.exists(output_path):
        raise ValueError('Output file not at %s',output_path)
    return ret_code


def load_netlist(filename):
    '''
    Loads a netlist into a string
    '''
    with open(netlist_path,'r') as f:
        netlist_content = f.read()
    # print(netlist_content)
    netlist_dict = deserialize_netlist(netlist_content)
    return netlist_dict

def save_run_and_load_modified_netlist(qucs_qucsator_folder,netlist_filename,output_filename,netlist_dict):
    '''
    Inputs:
    qucs_qucsator_folder: location of qucsator
    netlist_filename: location to save/overwrite the netlist_dictionary
    output_filename: location to output the simulated data
    netlist_dict: dictionary of a (possibly) modified netlist.
    '''

    netlist_modified = serialize_netlist(netlist_dict)
    # print(netlist_modified)
    # new_netlist_path =  qucs_netlist_folder+os.sep+'netlist2.txt'
    with open(netlist_filename,'w') as f:
        f.write(netlist_modified)
    ret_code = run_simulation(qucs_qucsator_folder,netlist_filename,output_filename)
    if ret_code == -1:
        return None
    ds = load_data(output_filename)
    return ds
    # print(netlist_content)