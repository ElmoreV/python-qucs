
import re 
def deserialize_netlist(netlist_data):
    '''
    Reads the netlist data as a string,
    and outputs a Python dictionary where all elements are separated and all the parameters of the elements are 
    changeable.
    '''
    netlist = netlist_data.split('\n')
    data ={}
    # First line
    data['ID'] = netlist[0]
    for lines in netlist[1:]:
        # print(len(lines))
        if len(lines)>1:
            # print('line',lines)
            part_a = lines.split(':')
            component_name = part_a[0]
            part_b = ''
            for part in part_a[1:]:
                part_b+=':'+part
            # print(part_b)
            part_b=part_b[1:]
            part_b = part_b.split()
            name = part_b[0]
            if '.' in component_name or 'Eqn' in component_name:
                dict2 = {'component_name':component_name,
                        'name':name}
                part_b = part_b[1:]
            elif 'SPfile' in component_name:
                dict2={'component_name':component_name,
                    'name':name,
                'connect_1':part_b[1],
                'connect_2':part_b[2],
                'connect_3':part_b[3]
                }
                part_b=part_b[4:]
            else:
                dict2={'component_name':component_name,
                    'name':name,
                'connect_1':part_b[1],
                'connect_2':part_b[2],
                }
                part_b=part_b[3:]
            # print(part_b)
            part_c = ""
            for part in part_b:
                part_c += part+" "
            # part_c = str.join(part_b[3:],' ')
            
            # Split the string in part A="B" A="B" and group them like that
            # Many special characters are possible, except for a space, and a " in A
            # and just a " in B
            
            for match in re.finditer(r'([^" ]*)="([^"]*)"',part_c):
                # print(match.group(0))
                var_name = match.group(1)# match.group(0).split('=')[0]
                var_val = match.group(2)#.split('=')[1].strip('"')
                dict2[var_name]=var_val
            # print(dict2)
            data[name]=dict2
                
    return data

def serialize_netlist(netlist_dict):
    '''
    Reversing the above operation: creating a string from a netlist_dict
    serialize_netlist(deserialize_netlist(netlist_data)) should give an identical copy of
    the original netlist_data.
    '''
    string = netlist_dict['ID']+'\n\n'
    for key,val in netlist_dict.items():
        # print(key,val)
        if key=='ID':
            continue
        string2 = val['component_name']+':'+val['name']
        if 'connect_1' in val:
            string2+=' '+val['connect_1']+ ' '+val['connect_2']
            if 'connect_3' in val:
                string2+=' '+val['connect_3']
        for key2,val2 in val.items():
            if key2 not in ['component_name','name','connect_1','connect_2','connect_3']:
                string2 +=' '+key2+'="'+str(val2)+'"'
        string+=string2+'\n'
    return string
