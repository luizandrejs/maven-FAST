'''
This file is part of an ICSE'18 submission that is currently under review.
For more information visit: https://github.com/icse18-FAST/FAST.

This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
'''

import math
import os
import pickle
import sys
import pathlib
import shutil
import re
import glob

import competitors
import fast
import metric

usage = """USAGE: python3 py/prioritize.py <projectPath> <algorithm> <repetitions>
OPTIONS:
  <dataset>: project with test suite to prioritize.
    exemples: '../my-projects/calculator', 'C:/users/user/projects/my-system'
  <algorithm>: algorithm used for prioritization.
    options: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all, STR, I-TSD, ART-D, ART-F, GT, GA, GA-S
  <repetitions>: number of prioritization to compute.
    options: positive integer value, e.g. 50
NOTE:
  STR, I-TSD are BB prioritization only.
  ART-D, ART-F, GT, GA, GA-S are WB prioritization only."""


def bboxPrioritization(name, projectPath, v, ctype, k, n, r, b, repeats, selsize):
    javaFlag = True if v == "v0" else False

    prog = os.path.basename(os.path.normpath(projectPath))

    fin = "{}/.fast/input/{}-{}.txt".format(projectPath, prog, ctype)
    #if javaFlag:
    #    fault_matrix = "input/{}_{}/fault_matrix.pickle".format(prog, v)
    #else:
    #    fault_matrix = "input/{}_{}/fault_matrix_key_tc.pickle".format(prog, v)
    outpath = "{}/.fast/output/".format(projectPath)
    ppath = outpath + "prioritized/"

    if name == "FAST-" + selsize.__name__[:-1]:
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                if javaFlag:
                    stime, ptime, prioritization = fast.fast_(
                        fin, selsize, r=r, b=b, bbox=True, k=k, memory=False)
                else:
                    stime, ptime, prioritization = fast.fast_(
                        fin, selsize, r=r, b=b, bbox=True, k=k, memory=True)
                writePrioritization(ppath, name, ctype, run, prioritization)
                #apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                #apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                #if javaFlag:
                #    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                #else:
                    #print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "FAST-pw":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                if javaFlag:
                    stime, ptime, prioritization = fast.fast_pw(
                        fin, r, b, bbox=True, k=k, memory=False)
                else:
                    stime, ptime, prioritization = fast.fast_pw(
                        fin, r, b, bbox=True, k=k, memory=True)
                print(prioritization)
                print('tamanho = ' + str(len(prioritization)))
                writePrioritization(ppath, name, ctype, run, prioritization)
                #apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                #apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                #if javaFlag:
                    #print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                #else:
                    #print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")
            shutil.rmtree("{}".format(outpath))

    elif name == "STR":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.str_(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                #apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                #apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                #if javaFlag:
                #    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                #else:
                    #print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "I-TSD":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.i_tsd(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                #apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                #apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                #if javaFlag:
                #    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                #else:
                    #print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    else:
        print("Wrong input.")
        print(usage)
        exit()


def wboxPrioritization(name, prog, v, ctype, n, r, b, repeats, selsize):
    javaFlag = True if v == "v0" else False

    fin = "input/{}_{}/{}-{}.txt".format(prog, v, prog, ctype)
    if javaFlag:
        fault_matrix = "input/{}_{}/fault_matrix.pickle".format(prog, v)
    else:
        fault_matrix = "input/{}_{}/fault_matrix_key_tc.pickle".format(prog, v)

    outpath = "output/{}_{}/".format(prog, v)
    ppath = outpath + "prioritized/"

    if name == "GT":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.gt(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "FAST-" + selsize.__name__[:-1]:
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                if javaFlag:
                    stime, ptime, prioritization = fast.fast_(
                        fin, selsize, r=r, b=b, memory=False)
                else:
                    stime, ptime, prioritization = fast.fast_(
                        fin, selsize, r=r, b=b, memory=True)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "FAST-pw":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                if javaFlag:
                    stime, ptime, prioritization = fast.fast_pw(fin, r, b)
                else:
                    stime, ptime, prioritization = fast.fast_pw(
                        fin, r, b, memory=True)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "GA":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.ga(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "GA-S":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.ga_s(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "ART-D":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.artd(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    elif name == "ART-F":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.artf(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                apfd = metric.apfd(prioritization, fault_matrix, javaFlag)
                apfds.append(apfd)
                stimes.append(stime)
                ptimes.append(ptime)
                print("  Progress: 100%  ")
                print("  Running time:", stime + ptime)
                if javaFlag:
                    print("  APFD:", sum(apfds[run]) / len(apfds[run]))
                else:
                    print("  APFD:", apfd)
            rep = (name, stimes, ptimes, apfds)
            writeOutput(outpath, ctype, rep, javaFlag)
            print("")
        else:
            print(name, "already run.")

    else:
        print("Wrong input.")
        print(usage)
        exit()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def writePrioritization(path, name, ctype, run, prioritization):
    fout = "{}/{}-{}-{}.pickle".format(path, name, ctype, run+1)
    pickle.dump(prioritization, open(fout, "wb"))


def writeOutput(outpath, ctype, res, javaFlag):
    if javaFlag:
        name, stimes, ptimes, apfds = res
        fileout = "{}/{}-{}.tsv".format(outpath, name, ctype)
        with open(fileout, "w") as fout:
            fout.write("SignatureTime\t\tPrioritizationTime\t\t\n")
            for st, pt in zip(stimes, ptimes):
                tsvLine = "{}\t{}\t\n".format(st, pt)
                fout.write(tsvLine)
    else:
        name, stimes, ptimes, apfds = res
        fileout = "{}/{}-{}.tsv".format(outpath, name, ctype)
        with open(fileout, "w") as fout:
            fout.write("SignatureTime\tPrioritizationTime\tAPFD\n")
            for st, pt, apfd in zip(stimes, ptimes, apfds):
                tsvLine = "{}\t{}\t{}\n".format(st, pt, apfd)
                fout.write(tsvLine)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def codeFormat(code):

    return re.compile(r"\s+").sub(" ", code).strip()

def getLanguagae(filePath):

    return pathlib.PurePosixPath(filePath).suffix

def openAndWriteInFile(fileName, append_write, code):
    f = open(fileName, append_write)
    f.write(code)
    f.close()

def createFolderIfNotExists(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

def createFastPath(projectPath):
    fastPath = projectPath+"/.fast"

    if not os.path.exists(fastPath):
        os.makedirs(fastPath)

    return fastPath

def parameterizer(filePath):

    projectName = os.path.basename(os.path.normpath(filePath))

    inputFolderPath = '{}/.fast/input'.format(filePath)
    
    createFolderIfNotExists(inputFolderPath)

    fileName = "{}/{}-bbox.txt".format(inputFolderPath, projectName)
        
    arr = glob.glob(filePath + "/**/*Test.java", recursive = True)

    for fileTest in arr:

        f = open(fileTest, "r")

        code = codeFormat(f.read()) + '\n'

        if os.path.exists(fileName):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        openAndWriteInFile(fileName, append_write, code)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong input.")
        print(usage)
        exit()
    projectPath, algname, repeats = sys.argv[1:]

    entity = 'bbox'

    repeats = int(repeats)
    algnames = {"FAST-pw", "FAST-one", "FAST-log", "FAST-sqrt", "FAST-all",
                "STR", "I-TSD",
                "ART-D", "ART-F", "GT", "GA", "GA-S"}
    entities = {"bbox", "function", "branch", "line"}

    if not os.path.exists(projectPath): 
        print("<projectPath> input incorrect or not exists.")
        print(usage)
        exit()
    elif entity not in entities:
        print("<entity> input incorrect.")
        print(usage)
        exit()
    elif algname not in algnames:
        print("<algorithm> input incorrect.")
        print(usage)
        exit()
    elif repeats <= 0:
        print("<repetitions> input incorrect.")
        print(usage)
        exit()

    fastPath = createFastPath(projectPath)
    parameterizer(projectPath)     

    v = 'v0'

    directory = "{}/.fast/output/".format(projectPath)
    createFolderIfNotExists(directory)
    directory += "prioritized/"
    createFolderIfNotExists(directory)

    # FAST parameters
    k, n, r, b = 5, 10, 1, 10

    # FAST-f sample size
    if algname == "FAST-all":
        def all_(x): return x
        selsize = all_
    elif algname == "FAST-sqrt":
        def sqrt_(x): return int(math.sqrt(x)) + 1
        selsize = sqrt_
    elif algname == "FAST-log":
        def log_(x): return int(math.log(x, 2)) + 1
        selsize = log_
    elif algname == "FAST-one":
        def one_(x): return 1
        selsize = one_
    else:
        def pw(x): pass
        selsize = pw

    if entity == "bbox":
        bboxPrioritization(algname, projectPath, v, entity, k, n, r, b, repeats, selsize)
    else:
        prog = os.path.basename(os.path.normpath(projectPath))
        wboxPrioritization(algname, prog, v, entity, n, r, b, repeats, selsize)
