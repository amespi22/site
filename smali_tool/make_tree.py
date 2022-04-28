#! /usr/bin/env python
import os
import sys
import argparse
"""
Dot must be installed for this to work
The script must be located in the directory
created by "apktool -d file_name"
when calling the script please make output file name
end in ".dot"
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='function_name', metavar='N', type=str, nargs='+',
                           help='Root function for tree')

    parser.add_argument('-n', action='store', dest='iterations',
                    default=10, type=int,
                    help='Number of iterations')

    parser.add_argument('-f', action='store', dest='output_file',
                    default="out.dot",
                    help='Name of output file, end in ".dot"')

    parser.add_argument('-root', action='store', dest = 'function_name',
                    help='Root function for tree')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    parser.add_argument('-Ns', action='store_false', default=True,
                    dest='no_static',
                    help='Remove static functions and/or objects')

    parser.add_argument('-Nf', action='store_false', default=True,
                    dest='no_final',
                    help='Remove final objects')

    parser.add_argument('-Np', action='store_false', default=True,
                    dest='no_protected',
                    help='Remove protected functions and/or objects')

    parser.add_argument('-Ny', action='store_false', default=True,
                    dest='no_synthetic',
                    help='Remove synthetic functions and/or objects')

    results = parser.parse_args()
    f_name = results.output_file
    #open all files and store them in ram
    fs = start(".")
    td = open (f_name, "w")
    td.write("digraph test {\n")
    td.close()
    #find_func = ["Ljavax/crypto/Cipher;->doFinal"]
    find_func = results.function_name

    smali_files = [(open_and_read(x),x)for x in fs]

    #traverse all files for the function you want
    x = traverse(find_func, smali_files, f_name, results)
    for z in range(results.iterations):
        x = traverse(x, smali_files, f_name, results)

    #recursively traverse all files for any functions that called original function
    #build tree with file name and function
    td = open (f_name, "a")
    td.write("}")
    td.close()
    make_pdf_s = "dot {} -Tpdf > {}.pdf".format(
            f_name,f_name[:f_name.find(".")])

    v = sys.version_info
    if v[0] == 2:
        import commands
        s,o = commands.getstatusoutput(make_pdf_s)
    else:
        if v[0] == 3:
            import subprocess
            s,o = subprocess.getstatusoutput(make_pdf_s)

def traverse(find_func, smali_files, f_name, results):
    ret_fcs = []
    td = open (f_name, "a")
    for ff in find_func:
        mfs = [x for x in smali_files if ff in x[0]]
        for m in mfs:
            fcs = get_calling_function(m, ff, results)
            ret_fcs += fcs
            for f in fcs:
                #print("{} called in {} by function {}".format(ff, m[1], f))
                td.write(""" "{}" -> "{}"; """.format
                        (ff.replace(";", ";\n"),f.replace(";", ";\n")))
    return ret_fcs

def start(s):
    #print("s = {}".format(s))
    ds,fs = get_dir_contents(s)
    for d in ds:
        fs += start(d)
    return fs

def get_calling_function(fils, match, results):
    c , path = fils
    funs = seperate_functions(c.split("\n"))
    fc = []
    for f in funs:
        if match in f:
            #get the first line
            s = f[:f.find("\n")]
            s = s.replace('.method', '')
            s = s.replace('public', '')
            s = s.replace('private', '')
            s = s.replace('bridge', '')
            s = s.replace('constructor', '')

            if (results.no_static):
                s = s.replace('static', '')
            if (results.no_final):
                s = s.replace('final', '')
            if (results.no_synthetic):
                s = s.replace('synthetic', '')
            if (results.no_protected):
                s = s.replace('protected', '')

            s = s.strip()
            #shake off .smali and the beginning .
            fc.append("L{};->{}".format(path[path.find('/',2) +1:-6],s))
    return fc

def seperate_functions(cs):
    fs = []
    found_method = 0
    s = ""
    for line in cs:
        if ".method" in line:
            s = line + "\n"
            found_method = 1
        else:
            if ".end method" in line:
                s += line + "\n"
                found_method = 0
                fs.append(s)
            else:
                if found_method:
                    s += line + "\n"
    return fs


def open_and_read(f):
    fi = open(f, "r")
    return fi.read()

def get_dir_contents(dir_name):
    cs = os.listdir(dir_name)
    #print(cs)
    f = []
    d = []
    for c in cs:
        if os.path.isdir(dir_name + "/" + c):
            d.append(dir_name + "/" + c)
        else:
            if c.endswith(".smali"):
                f.append(dir_name + "/" + c)
    return (d,f)

if __name__ == "__main__":
    main()

