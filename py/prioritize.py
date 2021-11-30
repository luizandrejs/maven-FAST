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

from tools.FASTWatchdog import checkIfFilesHaveBeenModified, checkDeletedFile

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

    prog = getProjectName(projectPath)
    fastPath = "{}/.fast".format(projectPath)

    inpath = "{}/.fast/input/".format(projectPath)
    fin = "{}/{}-{}.txt".format(inpath, prog, ctype)
    #if javaFlag:
    #    fault_matrix = "input/{}_{}/fault_matrix.pickle".format(prog, v)
    #else:
    #    fault_matrix = "input/{}_{}/fault_matrix_key_tc.pickle".format(prog, v)
    outpath = "{}/.fast/output/".format(projectPath)
    ppath = outpath + "prioritized/"

    if name == "FAST-" + selsize.__name__[:-1]:
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            shutil.rmtree("{}".format(fastPath))

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
            writePrioritizationFiles(inpath, ppath, name, ctype, run, prioritization)
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

    elif name == "FAST-pw":

        ptimes, stimes, apfds = [], [], []
        for run in range(repeats):
            print(" Run", run)
            if javaFlag:
                stime, ptime, prioritization = fast.fast_pw(
                    fin, r, b, bbox=True, k=k, memory=False)
            else:
                stime, ptime, prioritization = fast.fast_pw(
                    fin, r, b, bbox=True, k=k, memory=True)
            writePrioritization(ppath, name, ctype, run, prioritization)
            writePrioritizationFiles(inpath, ppath, name, ctype, run, prioritization)
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

    elif name == "STR":
        if ("{}-{}.tsv".format(name, ctype)) not in set(os.listdir(outpath)):
            ptimes, stimes, apfds = [], [], []
            for run in range(repeats):
                print(" Run", run)
                stime, ptime, prioritization = competitors.str_(fin)
                writePrioritization(ppath, name, ctype, run, prioritization)
                writePrioritizationFiles(inpath, ppath, name, ctype, run, prioritization)
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
                writePrioritizationFiles(inpath, ppath, name, ctype, run, prioritization)
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

def writePrioritizationFiles(inputPath, prioritizedPath, name, ctype, run, prioritization):

    projectName = getProjectName(inputPath.replace(".fast/input", ""))
    indexTestFilesPaths = "{}/{}-indexTestFilesPaths.txt".format(inputPath, projectName)

    f = open(indexTestFilesPaths, "r")
    lines = f.readlines()

    priorizationTestCases = ""

    for testCaseIndex in prioritization:
        priorizationTestCases += lines[testCaseIndex-1]

    file = "{}/{}-{}-{}.txt".format(prioritizedPath, name, ctype, run+1)
    openAndWriteInFile(file, 'w', priorizationTestCases)
    createPriorizationFile(prioritizedPath, name, ctype, run+1)

def createPriorizationFile(prioritizedPath, projectName, ctype, run):

    header = '''package fast;\n\nimport org.junit.platform.runner.JUnitPlatform;\nimport org.junit.platform.suite.api.SelectClasses;\nimport org.junit.runner.RunWith;\n\n'''

    midle = '''\n@RunWith(JUnitPlatform.class)\n@SelectClasses({\n'''

    footer = '''})\nclass FASTPrioritizedSuite{}'''

    fastTestPackage = '{}/../../../src/test/java/fast'.format(prioritizedPath)

    createFolderIfNotExists(fastTestPackage)

    f1 = open('{}/FASTPrioritizedSuite.java'.format(fastTestPackage), 'w+')

    f2 = open("{}/{}-{}-{}.txt".format(prioritizedPath, projectName, ctype, run), "r")
    lines = f2.readlines()
    linesCopy = lines

    imports = ""
    priorizationTestCases = ""

    testCaseIndex = 0

    while testCaseIndex < len(lines):
        imports += 'import ' + lines[testCaseIndex-1].replace('src/test/java/', '').replace('/','.').replace('.java',';')
        priorizationTestCases += '\t' + linesCopy[testCaseIndex-1].split('/')[-1].replace('.java', '.class,')
        testCaseIndex = testCaseIndex + 1

    f1.write(header+imports+midle+priorizationTestCases+footer)

def writeOutput(outpath, ctype, res, javaFlag):
    if javaFlag:
        name, stimes, ptimes, apfds = res
        fileout = "{}/{}-{}.tsv".format(outpath, name, ctype)
        with open(fileout, "w") as fout:
            fout.write("SignatureTime\tPrioritizationTime\t\n")
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

def getProjectName(projectPath):
    return os.path.basename(os.path.normpath(projectPath))

def resetFastPaths(projectPath):

    #base path
    fastPath = projectPath+"/.fast"
    shutil.rmtree("{}".format(fastPath))
    createFolderIfNotExists(fastPath)

    #input
    inputPath = '{}/input'.format(fastPath)
    createFolderIfNotExists(inputPath)

    #output
    outuptPath = "{}/output".format(fastPath)
    createFolderIfNotExists(outuptPath)
    createFolderIfNotExists(outuptPath+'/prioritized')

    return fastPath

def defineAppendWrite(fileName):

    if os.path.exists(fileName):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    return append_write

def parameterizer(projectPath, entity):

    projectName = getProjectName(projectPath)

    fileName = "{}/.fast/input/{}-{}.txt".format(projectPath, projectName, entity)

    indexTestFilesPaths = "{}/.fast/input/{}-indexTestFilesPaths.txt".format(projectPath, projectName)

    baseMavenTestPath = "/src/test/java"

    # https://junit.org/junit5/docs/current/user-guide/#running-tests-build-maven-filter-test-class-names
    arr1 = glob.glob(projectPath + baseMavenTestPath + "/**/Test*.java", recursive = True)
    arr2 = glob.glob(projectPath + baseMavenTestPath  + "/**/*Test.java", recursive = True)
    arr3 = glob.glob(projectPath + baseMavenTestPath  + "/**/*Tests.java", recursive = True)
    arr4 = glob.glob(projectPath + baseMavenTestPath  + "/**/*TestCase.java", recursive = True)

    arr = arr1 + arr2 + arr3 + arr4

    for fileTest in arr:

        f = open(fileTest, "r")

        code = codeFormat(f.read()) + '\n'

        append_write = defineAppendWrite(fileName)
        openAndWriteInFile(fileName, append_write, code)

        append_write = defineAppendWrite(indexTestFilesPaths)
        testFile = os.path.relpath(fileTest, projectPath) + '\n'
        openAndWriteInFile(indexTestFilesPaths, append_write, testFile)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong input.")
        print(usage)
        exit()
    projectPath, algname = sys.argv[1:]

    algnames = {"FAST-pw", "FAST-one", "FAST-log", "FAST-sqrt", "FAST-all",
                "STR", "I-TSD",
                "ART-D", "ART-F", "GT", "GA", "GA-S"}
    entities = {"bbox", "function", "branch", "line"}

    if not os.path.exists(projectPath):
        print("<projectPath> input incorrect or not exists.")
        print(usage)
        exit()
    elif algname not in algnames:
        print("<algorithm> input incorrect.")
        print(usage)
        exit()

    # FAST parameters
    k, n, r, b = 5, 10, 1, 10
    v = 'v0'
    entity = 'bbox'
    repeats = 1

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

        if checkIfFilesHaveBeenModified(projectPath):
            resetFastPaths(projectPath)
            parameterizer(projectPath, entity)
            bboxPrioritization(algname, projectPath, v, entity, k, n, r, b, repeats, selsize)
        elif checkDeletedFile(projectPath):
            resetFastPaths(projectPath)
            parameterizer(projectPath, entity)
            bboxPrioritization(algname, projectPath, v, entity, k, n, r, b, repeats, selsize)
        else:
            print('No modifications were found in the project tests')

    else:
        prog = getProjectName(projectPath)
        wboxPrioritization(algname, prog, v, entity, n, r, b, repeats, selsize)
