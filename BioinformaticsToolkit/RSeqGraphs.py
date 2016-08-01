import gi
import rpy2
import rpy2.robjects as robjects
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def testFun():

    print rpy2.__version__

def runFromFileTest():

    fileName = "Scripts/RTest.R" #"intermediateggplot2.R"
    contents = open(fileName).read()
    output = robjects.r(contents)
    print "HI"
    print fileName
    print output
    arg1 = 25
    subprocess.check_call(['Rscript', 'RTest.R'], shell=False)
