#!/usr/bin/env python
#
# File: jazzparamgen.py
#
# Author: D. Adriaansen
#
# Date: 24 Feb 2021
#
# Purpose: Generate a parameter file based on user input
#
# Notes:
#___________________________________________________________________

# Python libs
import os, sys, glob, operator, string, subprocess, calendar, time, copy, datetime, socket
from jazzparamgencolors import *
import jazzparamgen_pdef as P
from functools import reduce

# Parameter handling via ConfigMaster
p = P.Params()
p.init("Jazz Parameter Generation Simple params")
TMODE = p.opt['tmode']
START = p.opt['start']
END = p.opt['end']
INTERVAL = p.opt['interval']
ZMODE = p.opt['zmode']
WWIDTH = p.opt['wwidth']
WHGT = p.opt['whgt']
OUTFILE = p.opt['outfile']
INURL = p.opt['inurl']
INLIST = p.opt['inlist']
DATADIR = p.opt['rap_data_dir']
DATAHOST = p.opt['rap_data_dir_host']
TOPOURL = p.opt['topo_url']
LATMAX = p.opt['latmax']
LATMIN = p.opt['latmin']
LONMAX = p.opt['lonmax']
LONMIN = p.opt['lonmin']
VIEWPROJ = p.opt['viewproj']
MNAMES = p.opt['mnames']
MMETHOD = p.opt['mmethod']
REMOTE = p.opt['remote']
REMUSER = p.opt['remuser']
COLORURL = p.opt['colorurl']
EXCLUDE = p.opt['exclude']
SPDBPATH = p.opt['spdbpath']
SPDBHOST = p.opt['spdbhost']
LATLONLINES = p.opt['drawlatlon']
ADDSKEWT = p.opt['addskewt']
SKEWTURL = p.opt['skewtURL']
SKEWTHOST = p.opt['skewthost']
INCLUDE = p.opt['must_include']
DEBUG = p.opt['debug']
PMDV_EXE = p.opt['pmdv_exe']

# Function to print parameters
def print_params():
  print('')
  print('PARAMETERS:')
  print(('TMODE     = %s' % (TMODE)))
  print(('START     = %s' % (START)))
  print(('END       = %s' % (END)))
  print(('INTERVAL  = %s' % (INTERVAL)))
  print(('ZMODE     = %s' % (ZMODE)))
  print(('WWIDTH    = %s' % (WWIDTH)))
  print(('WHGT      = %s' % (WHGT)))
  print(('OUTFILE   = %s' % (OUTFILE)))
  print(('INURL     = %s' % (INURL)))
  print(('DATADIR   = %s' % (DATADIR)))
  print(('DATAHOST  = %s' % (DATAHOST)))
  print(('TOPOURL   = %s' % (TOPO_URL)))
  print(('LATMAX    = %2.5f' % (LATMAX)))
  print(('LATMIN    = %2.5f' % (LATMIN)))
  print(('LONMAX    = %2.5f' % (LONMAX)))
  print(('LONMIN    = %2.5f' % (LONMIN)))
  print(('DEBUG     = %s' % (DEBUG)))
  print(('INLIST    = %s' % (INLIST)))

# Define a usage function for the user
def usage():
  print ('')
  print ('FATAL! You must provide either rap_data_dir, inurl, or inlist.')
  print ('Please re-configure and try again')
  print ('Exiting...\n')
  exit(1)

# Define a not found function for the user
def missing(MDVPATH):
  print ('')
  print ('ERROR! The file you requested does not exist.')
  print ('Please check the path and try again.')
  print (('%s' % (MDVPATH)))
  exit(1)

# Define function to call commands
def call(cmd):
  subprocess.call('%s' % (cmd), shell=True, executable='/bin/csh')

# Define a function for writing the beginning of a new Jazz file
def write_beg(fout):

  if DEBUG:
    print("\nWRITING BEGINNING BLOCK")

  # First print some required Jazz and XML stuff
  fout.write("<?xml version=\"1.0\"?>\n")
  fout.write("\n")
  fout.write("<Jazz version=\"1.0\">\n")
  fout.write("\n")

# Define function for printing out a MDV layer
def write_layer(fout,layername,mdvparent,cmapname,gnum,COLORURL):

  if DEBUG:
    print("\nWRITING MDV LAYER %s" % (layername))

  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"MDV\"\n")
  fout.write("name=\"%s\"\n" % (layername))
  fout.write("location=\"%s\"\n" % (mdvparent))
  fout.write("field=\"%s\"\n" % (layername))
  fout.write("render=\"grid\"\n")
  fout.write("colorscale=\"%s/%s\"\n" % (COLORURL,cmapname))
  fout.write("menuGroup=\"menu%d\"\n" % (gnum))
  fout.write("visibilityGroups=\"none\"\n")
  fout.write("menuName=\"%s\"\n" % (layername))
  fout.write("/>\n")

# Function for writing SPDB info
def write_spdb(spdbhost,spdburl,spdbtype,beginoff,endoff,mode):

  if DEBUG:
    print("\nWRITING SPDB %s" % (spdbtype))

  if spdbtype == "AcTrack":
    spdbServer = "AcTrack"
  else:
    spdbServer = spdbtype.title()

  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"SYMPROD\"\n")
  fout.write("name=\"%s\"\n" % (str.upper(spdbtype)))
  fout.write("location=\"spdbp:%s2Symprod:icing//%s.rap.ucar.edu::%s/%s\"\n" % (spdbServer,spdbhost,spdburl,spdbtype))
  fout.write("before=\"%dmins\"\n" % (int(beginoff)))
  fout.write("after=\"%dmins\"\n" % (int(endoff)))
  fout.write("textOff=\"0.7\"\n")
  fout.write("request=\"interval\"\n")
  fout.write("menuName=\"%s\"\n" % (str.upper(spdbtype)))
  fout.write("uniqueMode=\"%s\"\n" % (mode))
  fout.write("/>\n")

# Function for writing the topography block
def write_topo(fout,TOPOURL,COLORURL):

  if DEBUG:
    print("\nWRITING TOPO")

  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"MDVTOPO\"\n")
  fout.write("name=\"Topography\"\n")
  fout.write("location=\"%s\"\n" % (TOPOURL))
  fout.write("field=\"HGT\"\n")
  fout.write("colorscale=\"%s/topo.colors\"\n" % (COLORURL))
  fout.write("/>\n")

# Function for writing the map area line
def write_area(fout,LATMIN,LATMAX,LONMIN,LONMAX):

  if DEBUG:
    print("\nWRITING AREA")

  fout.write("<Area\n")
  fout.write("name=\"FULL DOMAIN\"\n")
  fout.write("minLon=\"%3.5f\"\n" % (LONMIN))
  fout.write("maxLon=\"%3.5f\"\n" % (LONMAX))
  fout.write("minLat=\"%3.5f\"\n" % (LATMIN))
  fout.write("maxLat=\"%3.5f\"\n" % (LATMAX))
  fout.write("defaultView=\"true\"\n")
  fout.write("/>\n")

# Function for writing the map layers
def write_map_layers(fout):

  if DEBUG:
    print("\nWRITING MAP LAYERS")

  fout.write("<Layer\n")
  fout.write("vis=\"on\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"N America\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/NW_Continents.map\"\n")
  fout.write("color=\"white\"\n")
  fout.write("width=\"1\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"US Counties\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/us_counties.map\"\n")
  fout.write("color=\"yellow\"\n")
  fout.write("width=\"0\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"on\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"State Borders\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/usa.map\"\n")
  fout.write("color=\"white\"\n")
  fout.write("width=\"1\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"US NEXRADS\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/US_nexrad.map\"\n")
  fout.write("color=\"magenta\"\n")
  fout.write("width=\"0\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"ASOS\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/iciclesfc.map\"\n")
  fout.write("color=\"cyan\"\n")
  fout.write("width=\"0\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"Labeled Airports\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/awc_labeled_airports.map\"\n")
  fout.write("color=\"green\"\n")
  fout.write("width=\"0\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"Great Lakes\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/great_lakes.map\"\n")
  fout.write("color=\"white\"\n")
  fout.write("width=\"0\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"US Highways\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/conus_ushwys.map\"\n")
  fout.write("color=\"red\"\n")
  fout.write("width=\"1\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"off\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"Interstates\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/conus_interstates.map\"\n")
  fout.write("color=\"red\"\n")
  fout.write("width=\"1\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"on\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"World States\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/world_states.map\"\n")
  fout.write("color=\"white\"\n")
  fout.write("width=\"1\"\n")
  fout.write("/>\n")
  fout.write("<Layer\n")
  fout.write("vis=\"on\"\n")
  fout.write("type=\"CIDDMAP\"\n")
  fout.write("name=\"Canada\"\n")
  fout.write("location=\"https://apps.ral.ucar.edu/maps/canada.map\"\n")
  fout.write("color=\"white\"\n")
  fout.write("width=\"1\"\n")
  fout.write("/>\n")

# Function for writing the time line
def write_time(fout,TMODE):

  if DEBUG:
    print("\nWRITING TIME CONTROL")

  if TMODE == "archive":
    fout.write("\n")
    fout.write("<Time mode =\"archive\" start=\"%s\" end=\"%s\" interval=\"%s\" update=\"60mins\"/>\n" \
                % (START,END,INTERVAL))
  else:
    fout.write("\n")
    fout.write("<Time mode=\"realtime\" start=\"-8hrs\" end=\"+0hrs\" interval=\"30mins\" update=\"5mins\"/>\n")

# Function for writing height scale
def write_alt(fout,ZMODE):

  if DEBUG:
    print("\nWRITING ALT CONTROL")

  if ZMODE == "pressure":
    fout.write("\n")
    fout.write("<Altitude units=\"mb\" bottom=\"1000\" top=\"50\" interval=\"25\" default=\"700\"/>\n")
  elif ZMODE == "flvl":
    fout.write("\n")
    fout.write("<Altitude units=\"FL\" bottom=\"0\" top=\"300\" interval=\"10\" default=\"100\"/>\n")
  elif ZMODE == "feet":
    fout.write("\n")
    fout.write("<Altitude units=\"ft\" bottom=\"0\" top=\"40000\" interval=\"1000\" default=\"6000\"/>\n")
  else:
    fout.write("\n")
    fout.write("<Altitude dataDrivenProperties=\"true\"/>\n")

# Function for writing the end of the file
def write_end(fout):

  if DEBUG:
    print("\nWRITING END BLOCK")

  fout.write("\n")
  if (VIEWPROJ=='LambertConformal'):
    fout.write("<View projection=\"LambertConformal\" originLon=\"-95\" originLat=\"25\" stdLat1=\"25\"/>\n")
  elif (VIEWPROJ=='PolarStereographic'):
    fout.write("<View projection=\"PolarStereographic\" tangentLon=\"225.0\" poleIsNorth=\"true\" centralScale=\"1.0\"/>\n")
  fout.write("\n")
  fout.write("<Window width=\"%d\" height=\"%d\" xOrigin=\"0\" yOrigin=\"0\" backgroundColor=\"black\"/>\n" \
              % (WWIDTH,WHGT))
  fout.write("\n")
  fout.write("\n")
  fout.write("<AvailableTimesTool/>")
  fout.write("\n")
  fout.write("<SwapFieldsTool/>")
  fout.write("\n")
  fout.write("<ModelRunSelectorTool/>")
  fout.write("\n")
  fout.write("<TimeAndAnimationTool/>")
  fout.write("\n")
  fout.write("<DistanceAndAzimuthTool distanceUnit=\"km\"/>")
  fout.write("\n")
  fout.write("<XSections dataDrivenProperties=\"true\" showGridLines=\"true\" enableZoom=\"rubberband\"> </XSections>\n")
  fout.write("\n")
  if LATLONLINES:
    fout.write("<LatLonReferenceLines foregroundColor=\"black\" backgroundColor=\"white\" fontSize=\"5\"> </LatLonReferenceLines>\n")
    fout.write("\n")
  if ADDSKEWT:
    fout.write("<SkewT location=\"mdvp:://%s.rap.ucar.edu::%s\" temperatureField=\"TMP\" rhField=\"RH\" dewpointField=\"DEW_PT_TEMP\" uField=\"RH\" vField=\"RH\" > </SkewT>\n" % (SKEWTHOST,SKEWTURL))
    fout.write("\n")
  fout.write("</Jazz>")

# Define a function for setting menu name
def set_mname(layerlist,MDVPATH,MMETHOD):

  if DEBUG:
    print("\nSETTING MENU FOR %s" % (MDVPATH))

  if MMETHOD == 'strict':
    # Set the menuname based on the MDVPATH
    if (str.find(MDVPATH,'diagnostic'))>0 and (str.find(MDVPATH,'cip'))>0:
      mname = 'CIP Diagnostic'
    if (str.find(MDVPATH,'pressure'))>0 and (str.find(MDVPATH,'cip'))>0:
      mname = 'CIP Pressure'
    if (str.find(MDVPATH,'derived'))>0 or (str.find(MDVPATH,'pressure_derived'))>0 and (str.find(MDVPATH,'model'))>0:
      mname = 'Model Derived'
    if (str.find(MDVPATH,'pressure'))>0 and (str.find(MDVPATH,'model'))>0 and (str.find(MDVPATH,'pressure_derived'))<0:
      mname = 'Model Pressure'
    if (str.find(MDVPATH,'hybrid'))>0:
      mname = 'Model Hybrid'
    if (str.find(MDVPATH,'fip'))>0 and (str.find(MDVPATH,'diagnostic'))>0:
      mname = 'FIP Diagnostic'
    if (str.find(MDVPATH,'fip'))>0 and (str.find(MDVPATH,'pressure'))>0:
      mname = 'FIP Pressure'
    if (str.find(MDVPATH,'lightning'))>0:
      mname = 'Lightning'
    if (str.find(MDVPATH,'metar_mapper'))>0:
      mname = 'Metar'
    if (str.find(MDVPATH,'pirep_mapper'))>0:
      mname = 'Pirep'
    if (str.find(MDVPATH,'refl'))>0:
      mname = 'NSSL 2D Radar Merged Tiles'
    if (str.find(MDVPATH,'convert'))>0:
      mname = 'Converted Radar Data'
    if (str.find(MDVPATH,'mapper'))>0 and (str.find(MDVPATH,'radar'))>0:
      mname = 'Radar Mapper'
    if (str.find(MDVPATH,'east'))>0 and (str.find(MDVPATH,'east_derived'))<0:
      mname = 'Satellite East'
    if (str.find(MDVPATH,'west'))>0 and (str.find(MDVPATH,'west_derived'))<0:
      mname = 'Satellite West'
    if (str.find(MDVPATH,'east_derived'))>0:
      mname = 'Satellite East Derived'
    if (str.find(MDVPATH,'west_derived'))>0:
      mname = 'Satellite West Derived'
    if (str.find(MDVPATH,'conus'))>0 and (str.find(MDVPATH,'satellite'))>0:
      mname = 'Satellite CONUS'

    # Set the mname to '' if we couldn't define it
    try:
      mname
    except:
      mname = ''

  if MMETHOD == 'lazy':

    # If the menu name was unable to be determined, return empty.
    try:
      mname
    except:
      # Try and set the mname to part of the MDVPATH sent in
      ps1 = str.split(MDVPATH,"/")
      # Find the date string index
      for mi in ps1:
        try:
          int(mi)
          ds_idx = ps1.index(mi)
          break
        except:
          ds_idx = -1

      if not 'mdv' in ps1 or ds_idx < 0:
        mname = ''
      else:
        if ds_idx >= 0 and 'mdv' in ps1:
          if ds_idx == ps1.index('mdv')+1:
            mname = ps1[ps1.index('mdv')+1]
          else:
            mname = reduce(os.path.join,list(ps1[ps1.index('mdv')+1:ds_idx]))
        else:
          mname = ''

  # For tiling support, append the tile number
  if (str.find(MDVPATH,'tile'))>0:
    ss1 = str.split(MDVPATH,'/')
    tileidx = [z for z, item in enumerate(ss1) if 'tile' in item]
    mname = mname + " %s" % (ss1[tileidx[0]])

  # Return the menu name
  return(mname)

# Define a helper function to figure out the mdvp URL prefix
def mdvurl_prefix(MDVPATH):

  s1 = str.split(MDVPATH,"::")
  return(s1[0]+"::"+s1[1]+"::")

# Define a helper function to return the code from a PrintMdv call
def pmdv_status(MDVPATH):

  pmdv_cmd = subprocess.Popen([PMDV_EXE,'-url','%s' % (MDVPATH),'-mode','latest'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if DEBUG:
    print('pmdv_status cmd: '+' '.join(pmdv_cmd.args))
  pmdv_cmd.communicate()
  return(pmdv_cmd.returncode)

# Define a helper function to return the latest file path from a PrintMdv call
def pmdv_latest_file_path(MDVPATH):
  
  if pmdv_status(MDVPATH)==0:
    pmdv_cmd = subprocess.Popen([PMDV_EXE,'-url','%s' % (MDVPATH),'-mode','latest'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    grep_cmd = subprocess.check_output(['grep','path:'],stdin=pmdv_cmd.stdout)
    return(mdvurl_prefix(MDVPATH)+str.split(grep_cmd.decode())[-1])
  else:
    missing(MDVPATH)

# Define a helper function to return a list of MDV field names
def get_mdv_field_names(MDVPATH):

  # NOTE: Here MDVPATH is an absolute path of an MDV file rather than a relative path
  if pmdv_status(MDVPATH)==0:
    pmdv_cmd = subprocess.Popen([PMDV_EXE,'-url','%s' % (MDVPATH)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    grep_cmd = subprocess.check_output(['grep','field_name:'],stdin=pmdv_cmd.stdout)
    return(str.split(grep_cmd.decode()))
  else:
    missing(MDVPATH)

# Define a helper function to return a boolean if this file path should be skipped
def skipFile(INPATH):

  # False = don't skip file, process it
  # True = skip file, don't process it

  # Double check INCLUDE and EXCLUDE. The user can't have it both ways- either they use INCLUDE or EXCLUDE.
  if INCLUDE != [] and EXCLUDE != []:
    print("\nWARNING! CAN ONLY USE INCLUDE OR EXCLUDE BUT NOT BOTH! PLEASE RECONFIGURE.\n")
    sys.exit(1)

  # If they are both empty, then just return False (don't skip file) since the user doesn't want to include or exclude anything
  if INCLUDE == [] and EXCLUDE == []:
    print(("RETURNING FALSE IN skipFile FOR: %s" % (INPATH)))
    return False

  # If EXCLUDE is empty, then we need to use INCLUDE
  if EXCLUDE == []:
    # Matches heren will FORCE processing.
    for es in INCLUDE:
      if es in INPATH:
        # Return false if any of the include strings are found
        if DEBUG:
          print(("RETURNING FALSE IN skipFile FOR: %s" % (INPATH)))
        return False
    # If we make it here, we never returned so just return true for this path and skip it.
    if DEBUG:
      print(("RETURNING TRUE IN skipFile FOR: %s" % (INPATH)))
    return True
  else:
    # Matches here will SKIP processing.
    for es in EXCLUDE:
      if es in INPATH:
        # Return true if any of the exclude strings are found
        if DEBUG:
          print(("RETURNING TRUE IN skipFile FOR: %s" % (INPATH)))
        return True
    # If we make it here, we never returned so just return false for this path and process it.
    if DEBUG:
      print(("RETURNING FALSE IN skipFile FOR: %s" % (INPATH)))
    return False

# Define a helper function to return a list of directories using SSH
def get_ssh_dir_list(REMUSER,DATAHOST,DATADIR):

  ls_cmd = subprocess.Popen(['ssh','-Y','%s@%s.rap.ucar.edu' % (REMUSER,DATAHOST),'ls','-1d','%s/*/' % (DATADIR)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  return(str.split(ls_cmd.communicate()[0].decode()))

# Define a function for determining the input list
def get_file_list(DATAHOST,DATADIR,REMOTE):

  # Create an MDV URL if it's not one
  DATAURL = 'mdvp:://%s.rap.ucar.edu::%s' % (DATAHOST,DATADIR)

  # First check to see if there's a file for the current MDV path
  if pmdv_status(DATAURL)==0:
    INLIST.append('%s' % (pmdv_latest_file_path(DATAURL)))
  else:

    # If no files found at MDVPATH initially, get the subdirectories at MDVPATH and theck all of them for files
    # Use SSH to do this remotely.

    # Initialize a list of directories we want to check
    dirCheckList = []

    # Get a list of all files at MDVPATH. Only save directories.
    if REMOTE:
      dirList = get_ssh_dir_list(REMUSER,DATAHOST,DATADIR)
      for rd in dirList:
        dirCheckList.append(rd[:-1])
    else:
      dirList = glob.glob('%s/*' % (DATADIR))
      for rd in dirList:
        if os.path.isdir(rd):
          dirCheckList.append(rd)

    # Keep looping until we've exhausted all the MDV files
    while dirCheckList!=[]:

      # Counter to keep track pf position
      dirCnt = 0

      # Print for user
      if DEBUG:
        print("\nCURRENT LIST OF DIRECTORIES TO CHECK:")
        for d in dirCheckList:
          print(d)

      # Create a deep copy of dirCheckList so we can modify it independently of the original value
      currDirList = copy.deepcopy(dirCheckList)

      # Loop one pass through currDirList, and modify (add/remove) items from the original dirCheckList
      while dirCnt < len(currDirList):
        DATAURL = 'mdvp:://%s.rap.ucar.edu::%s' % (DATAHOST,currDirList[dirCnt])
        print(("\nPROCESSING: %s" % DATAURL))
        if pmdv_status(DATAURL)==0:
          print(("FOUND %s" % (pmdv_latest_file_path(DATAURL))))

          # Remove this item from dirCheckList, since we found an MDV file at this PATH
          dirCheckList.remove(currDirList[dirCnt])

          # Append the latest MDV file from this PATH
          if not skipFile(currDirList[dirCnt]):
            if DEBUG:
              print("APPENDING %s TO INLIST" % (DATAURL))
            INLIST.append('%s' % (pmdv_latest_file_path(DATAURL)))

          # Advance position
          dirCnt = dirCnt + 1
        else:
          # Get a list of files at this PATH because we didn't find any MDV files
          print(("\nCHECKING FOR MORE DATA IN: %s" % (currDirList[dirCnt])))

          if REMOTE:
            dirList = get_ssh_dir_list(REMUSER,DATAHOST,currDirList[dirCnt])
            # Append all the directories found to dirCheckList since next time through we will check these
            for i in dirList:
              dirCheckList.append(i[:-1])
          else:
            dirList = glob.glob('%s/*' % (currDirList[dirCnt]))
            # Append all the directories found to dirCheckList since next time through we will check these
            for i in dirList:
              if os.path.isdir(i):
                dirCheckList.append(i)

          # Remove this item from dirCheckList though, because we don't need to check it again
          dirCheckList.remove(currDirList[dirCnt])

          # Advance position
          dirCnt = dirCnt + 1

  # Return a list of MDV files at all PATH's processed
  #print(INLIST)
  return(INLIST)

#######################################################################

# Check OUTFILE. If it's empty for some reason, warn the user and use a default value
if OUTFILE=='':
  print("")
  print("FATAL! NO OUTFILE PROVIDED. YOU MUST PROVIDE AN OUTPUT FILENAME.")
  print("CONFIGURE OPTION \'outfile\' AND TRY AGAIN.")
  sys.exit(1)

# If the INURL is set, set INLIST to a single item of INURL
if INURL!='':
  print("")
  print("WARNING! OVERRIDING INLIST AND RAP_DATA_DIR SINCE INURL WAS PROVIDED!")
  del(DATADIR)
  DATADIR = ''
  del(INLIST)
  INLIST = []
  INLIST.append(INURL)
# If INURL is empty, use DATADIR to set the INLIST
elif DATADIR!='':
  print("")
  print("WARNING! OVERRIDING INLIST AND INURL SINCE RAP_DATA_DIR WAS PROVIDED!")
  del(INURL)
  INURL = ''
  del(INLIST)
  INLIST = []
  # Set the INLIST based on DATADIR
  if REMOTE:
    print("")
    print("")
    print("!! !! !! !! !! !! !! !! !! !! !!")
    print("WARNING!")
    print("YOU ARE ATTEMPTING TO ACCESS FILES REMOTELY WITH THIS SCRIPT USING SSH.")
    print("UNEXPECTED BEHAVIOR CAN RESULT IF SSH KEYS ARE NOT IN PLACE.")
    print("PLEASE ENTER \"y\" TO CONTINUE OR \"n\" TO EXIT:")
    remChk = input()
    print("!! !! !! !! !! !! !! !! !! !! !!")
    print("")
    print("")
    if remChk=='y':
      INLIST = get_file_list(DATAHOST,DATADIR,REMOTE)
    else:
      sys.exit(0)
  else:
    INLIST = get_file_list(DATAHOST,DATADIR,REMOTE)
# If INURL and DATADIR are emtpy, the use the INLIST provided by the user
elif INLIST!=[]:
  pass
# If we make it here, make sure INLIST is set because the other two options weren't!
elif INLIST==[]:
  usage()
else:
  print("\nUNKNOWN MODE\n")
  sys.exit(1)

# Remove existing OUTFILE if present - user has explicitly requested a single file
if os.path.exists('%s' % (OUTFILE)):
  print("\nREMOVING %s" % (OUTFILE))
  cmd = 'rm -rf %s' % (OUTFILE)
  call(cmd)

# Open the output file
fout = open('%s' % (OUTFILE),"w")
 
# First, write the header
write_beg(fout)

print('')
print('PROCESSING URL LIST:')
for i in INLIST:
  print(i)

# Set the menu counter to 0
mcnt = 1

# Loop over INLIST
for f in INLIST:

  # Reset the list of layers
  layerlist = []

  # Make sure the item is an mdv file
  if not '.mdv' in f:
    print("")
    print("WARNING! '.mdv' NOT IN CURRENT URL.")
    print("USING PrintMdv TO DETERMINE INFO FOR:")
    print(f)

    # Make sure it has mdvp:: syntax. If not, assume localhost but use the hostname instead of localhost
    if 'mdvp::' not in f:
      f = 'mdvp:://%s::%s' % (socket.gethostname(),f)
    f = pmdv_latest_file_path(f)
    print(("\nNow processing file: %s" % (f)))
  else:
    print(("\nNow processing file: %s" % (f)))

  # Get the list of MDV layers from the file
  tmplist = get_mdv_field_names(f)
  for v in tmplist:
    if v != "field_name:":
      layerlist.append(v)

  # Send the layerlist to determine the menu name
  try:
    mname = MNAMES[mcnt-1]
  except:
    mname = set_mname(layerlist,f,MMETHOD)
  if mname == '':
    mname = 'test'
    print ('')
    print (('WARNING: Menu name unable to be determined for path %s' % (f)))
    print ('Setting to: \'test\'')
    #print ('WARNING: Menu name unable to be determined for path %s' % (f))
    #print ('Skipping to next path')
    print ('')
    #continue

  # Determine the parent directory for the current MDVPATH
  # This assumes that the YYYYMMDD containing directory is the only dir in the path that's numeric (not mix alpha-numeric)
  #mdvparent = f[:-20]
  if not '.mdv' in f:
    mdvparent = f
  else:
    ps1 = str.split(f,"/")
    dirs = []
    for d in ps1:
      try:
        int(d)
        break
      except:
        dirs.append(d)
    mdvparent = '/'.join(dirs)

  # Next write the menu line for the current group of layers
  fout.write("<MenuGroup name=\"menu%d\" label=\"%s\" parentGroup=\"GRIDS_MENU\"/>\n" % (mcnt,mname))
  
  # Finally, for all of the layers in layerlist, write the layer block for each
  for v in layerlist:

    # First determine the cmapname
    cmap = set_cmap(v)

    # Next write the block
    write_layer(fout,v,mdvparent,cmap,mcnt,COLORURL)

  # Increment the menu counter
  mcnt = mcnt + 1

# Write SPDB for PIREP
write_spdb(SPDBHOST,SPDBPATH,"pirep",120,0,"off")
write_spdb(SPDBHOST,SPDBPATH,"metar",60,0,"latest")
write_spdb(SPDBHOST,SPDBPATH,"ltg",15,0,"off")
write_spdb(SPDBHOST,SPDBPATH,"AcTrack",60,60,"off")

# After the layer blocks comes the topo
write_topo(fout,TOPOURL,COLORURL)

# Next comes the map area definition
write_area(fout,LATMIN,LATMAX,LONMIN,LONMAX)

# Next comes the map layers
write_map_layers(fout)

# Next comes the time mode
write_time(fout,TMODE)

# Next comes the altitude scale
write_alt(fout,ZMODE)

# Finally, write the end of the file (map proj, window size, /jazz)
write_end(fout)

# Close output file
fout.close()

# Print success
print('\nSUCCESSFULLY WROTE FILE:')
print(OUTFILE)

