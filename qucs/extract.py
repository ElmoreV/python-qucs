#!/usr/bin/env python

import re
import sys
import array, traceback
import pylab

class Data: pass
class Val(array.ArrayType):
    len=0
    dep=""




def load_data(filename):
    # Find all <tags/> in every line
    # if the tag is there it can either be
    # 'Qucs dataset'


    state="end"
    dat=Data()
    valdep=[]
    infile=open(filename)
    for line in infile.readlines():
        tagfnd=re.search("\<([^<>]*)\>",line)
        if tagfnd:
            tag=tagfnd.group(1)
            tag.strip()
            if re.search("Qucs Dataset ",line):
                continue
            if tag[0]=="/":
                # The data has ended, reformat the data if necessary
                state="end"
                # print("Number of Dimensions:",len(valdep))
                if len(valdep)>1:
                    # Reshape multidimensional data to an array
                    shape=[]
                    for i in range(len(valdep),0,-1):
                        shape.append(dat.__dict__[valdep[i-1]].len)
                    val=pylab.array(val)
                    val=pylab.reshape(val,shape)
                dat.__dict__[name]=val
            else:
                state="start"
                words=tag.split()
                #for indep: ['indep','name of indep var','size']
                # for dependent var: ['dep','name of dep var','depends on this indep var 1','and indep var 2','...']
                type=words[0]
                name=words[1].replace(".","_")
                name=name.replace(",","")
                name=name.replace("[","")
                name=name.replace("]","")
                if type=="indep":
                    val=Val("f")
                    val.len=int(words[2])
                else:
                    val=[]
                    valdep=words[2:]
        else:
            # There is no tag: it is data
            if state=="start":
                # Check for float or complex
                if "j" in line:
                    # Change 1+j1 to 1+1j
                    line=line.replace("j","")
                    line="%sj"%line.strip()
                    try:
                        val.append(complex(line))
                    except:
                        traceback.print_exc()
                        print(line) # add nan check
                        print(name)
                        print(len(val))
                else:
                    val.append(float(line))
            else:
                print("Parser Error:",line)

    return dat


if __name__ == "__main__":


    dat=load_data(sys.argv[1])

    print("Variables in",sys.argv[1])

    for key in dat.__dict__.keys():
        print("\nName =",key)
        try:
            print("\tLen=",dat.__dict__[key].len)
        except:
            pass
        try:
            print("\tDep=",dat.__dict__[key].dep)
        except:
            pass
