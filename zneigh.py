#!/usr/bin/env python
import urllib2
import json
import sys, getopt

def read_vera(hostname):
    link="http://" + hostname + ":3480/data_request?id=user_data"
    try:
        f = urllib2.urlopen(link)
        data=f.read().decode(encoding='UTF-8',errors='ignore')
        return json.loads(data)
    except:
        pass
    return False

def getkey(_json,key):
    try:
        return str(_json[key])
    except:
        pass
    return ""

def getint(_s):
    try:
        return str(int(_s))
    except:
        return ""

def getnodes(data):
    s=""
    for dev in data["devices"]:
        dev_alt=getkey(dev,"altid")
        if dev_alt == getint(dev_alt) and len(dev_alt)>0:
            s+= dev_alt + ";"
    return s

def parselist(nodes,_keys):
    lst=nodes.split(';')
    _k=_keys.split(',')
    s = ";"
    for _item in lst:
        if _item in _k:
            s+= _item 
        s+= ";"
    return s

def print_help():
    print 'Usage: zneigh -H <VERA-IP>'
    print 'List all nodes in the network and show its neighbors'
    print 'you can copy the output and paste into a spreadsheet'

def main(argv):
    hostname="127.0.0.1"
    try:
        opts, args = getopt.getopt(argv,"hH:",["host="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-H", "--host"):
            hostname = arg


    data=read_vera(hostname)
    if data != False:
        nodes= getnodes(data) 
        print "id;parent;nodeid;manufacturer;model;name;neighbors;"+nodes
        for dev in data["devices"]:
            dev_id =    getkey(dev,"id")
            dev_name=   getkey(dev,"name")
            dev_man=    getkey(dev,"manufacturer")
            dev_parent= getkey(dev,"id_parent")
            dev_model=  getkey(dev,"model")
            dev_alt=    getkey(dev,"altid")

            if len(dev_alt)>0 and dev_alt==getint(dev_alt):
                print dev_id + ";" + dev_parent + ";" + dev_alt + ";" + dev_man + ";" + dev_model + ";" + dev_name +";",
                for state in dev["states"]:
                    if state["variable"] == "Neighbors":
                        #print "," + state["value"],
                        print parselist(nodes,state["value"]),
                print ""
    else:
        print "error from " + hostname
if __name__ == "__main__":
    main(sys.argv[1:])
