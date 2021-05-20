#!/usr/bin/env python

# Import ConfigMaster
from ConfigMaster import ConfigMaster

# Create a params class
class Params(ConfigMaster):
  defaultParams = """

#!/usr/bin/env python

# DEFAULT PARAMS

###### debug #######
#
# NAME: debug
# OPTIONS:
# TYPE: bool
# FORMAT:
# DEFAULT: False
# DESCRIPTION: Control verbosity of info statements
#
debug = False

####### tmode #######
#
# NAME: tmode
# OPTIONS: realtime, archive
# TYPE: string
# FORMAT:
# DEFAULT: archive
# DESCRIPTION: Set the mode entry in the <Time> tag in the Jazz config file
#
tmode = "archive"

####### start #######
#
# NAME: start
# OPTIONS:
# TYPE: string
# FORMAT: YYYY-MM-DDTHH:MM
# DEFAULT:
# DESCRIPTION: Set the start entry in the <Time> tag in the Jazz config file
#              Only used for tmode = "archive"
#
start = "2019-02-01T00:00"

####### end #######
#
# NAME: end
# OPTIONS: 
# TYPE: string
# FORMAT: YYYY-MM-DDTHH:MM
# DEFAULT:
# DESCRIPTION: Set the end entry in the <Time> tag in the Jazz config file
#              Only used for dmode = "archive"
#
end = "2019-02-02T00:00"

####### interval #######
#
# NAME: interval
# OPTIONS: 
# TYPE: string
# FORMAT: MMmins
# DEFAULT: 60mins
# DESCRIPTION: Set the interval entry in the <Time> tag in the Jazz config file
#
interval = "60mins"

####### zmode #######
#
# NAME: zmode
# OPTIONS: pressure, flvl, feet, data
# TYPE: string
# FORMAT:
# DEFAULT: data
# DESCRIPTION: specify the vertical coordinate of your data, used to
#              control the <Altitude> tag in the Jazz config file
#
zmode = "data"

####### wwidth #######
#
# NAME: wwidth
# OPTIONS: 
# TYPE: integer
# FORMAT:
# DEFAULT: 1200
# DESCRIPTION: Width of the Jazz window when it opens
#              Used to set the width entry in the <Window> tag in the Jazz config file
#
wwidth = 1200

####### whgt #######
#
# NAME: whgt
# OPTIONS:
# TYPE: integer
# FORMAT:
# DEFAULT: 800
# DESCRIPTION: Height of the Jazz window when it opens
#              Used to set the height entry in the <Window> tag in the Jazz config file
#
whgt = 800

####### outfile #######
#
# NAME: outfile
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: 
# DESCRIPTION: output filename for your Jazz XML config file
#
outfile = ""

####### inurl #######
#
# NAME: inurl
# OPTIONS: 
# TYPE: string
# FORMAT:
# DEFAULT: ''
# DESCRIPTION: Provide a single absolute or relative path to generate a quick param file
#              If providing a URL, it must be a fully qualified MDV URL
#              following the mdvp:://hostname.rap.ucar.edu::/path/to/data syntax
#
inurl = ''

####### inlist #######
#
# NAME: inlist
# OPTIONS:
# TYPE: list
# FORMAT:
# DEFAULT: []
# DESCRIPTION: Explicit list of input MDV data files to process.
#              If providing URL's to remote hosts, the URL must be a fully qualified MDV URL
#              following the mdvp:://hostname.rap.ucar.edu::/path/to/data syntax
#              If the URL is relative, the "latest" file info will be obtained
#              If the URL is absolute, information from the specific file will be obtained 
#
inlist = []

####### rap_data_dir #######
#
# NAME: rap_data_dir
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: ''
# DESCRIPTION: If all of your MDV files are organized under a "data_dir", then provide the
#              top level of that path (e.g. /d1/user/data/mdv) and this script will attempt
#              to navigate all limbs of that tree that contain MDV files and include them
#              in the resulting config file
#
rap_data_dir = ''

####### rap_data_dir_host #######
#
# NAME: rap_data_dir_host
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: ''
# DESCRIPTION: Provide the hostname where the data in rap_data_dir exist. If it's remote, the
#              script will perform finding data in rap_data_dir remotely.
#
rap_data_dir_host = ''

####### remote #######
#
# NAME: remote
# OPTIONS: True, False
# TYPE: boolean
# FORMAT:
# DEFAULT: False
# DESCRIPTION: Indicate whether you want to access file information remotely using SSH or not. This requires
#              that SSH keys be set up between your localhost and remotehost, and is only really needed if you
#              want to automatically create a config file without setting the INLIST variable.
#              In other words, this is only used when rap_data_dir is set and rap_data_dir_host is not localhost.
#
remote = False

####### remuser #######
#
# NAME: remuser
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT:
# DESCRIPTION: Username of account on remote host. Only used if remote is True.
#
remuser = ""

####### topo_url #######
#
# NAME: topo_url
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: "mdvp:://localhost::/tmp/topo.mdv"
# DESCRIPTION: URL/path to topography file if you wish to view topography in Jazz.
#              This is not a required file, and so often times a dummy file can be used.
#              Must be a fully qualified MDV URL, with the form:
#              mdvp:://hostname.rap.ucar.edu::/path/to/topo.mdv
#
topo_url = "mdvp:://localhost::/tmp/topo.mdv"

####### latmax #######
#
# NAME: latmax
# OPTIONS:
# TYPE: float
# FORMAT:
# DEFAULT: 52.0
# DESCRIPTION: Maximum (northern) latitude of the full domain/default area that you want to view.
#
latmax = 52.0

####### latmin #######
#
# NAME: latmin
# OPTIONS:
# TYPE: float
# FORMAT:
# DEFAULT: 16.5
# DESCRIPTION: Minimum (southern) latitude of the full domain/default area that you want to view.
#
latmin = 16.5

####### lonmax #######
#
# NAME: lonmax
# OPTIONS:
# TYPE: float
# FORMAT:
# DEFAULT: -70.0
# DESCRIPTION: Maximum longitude (eastern) of the full domain/default area that you want to view.
#
lonmax = -70.0

####### lonmin #######
#
# NAME: lonmin
# OPTIONS:
# TYPE: float
# FORMAT:
# DEFAULT: -122.0
# DESCRIPTION: Minimum longitude (western) of the full domain/default area that you want to view.
#
lonmin = -122.0

####### viewproj #######
#
# NAME: viewproj
# OPTIONS: PolarStereographic, LambertConformal
# TYPE: string
# FORMAT:
# DEFAULT: "LambertConformal"
# DESCRIPTION: Projection Jazz will use to display data (will re-project if not equal to this)
#
viewproj = "LambertConformal"

####### mnames #######
#
# NAME: mnames
# OPTIONS: 
# TYPE: list
# FORMAT:
# DEFAULT: []
# DESCRIPTION: Provide an optional list of menu names. Only applies when "inlist" is used,
#              and items should be 1-1 with items in "inlist". If this is not set,
#              the file path string will be used for the menu names.
#
mnames = []

####### mmethod #######
#
# NAME: mmethod
# OPTIONS: strict, lazy
# TYPE: string
# FORMAT: 
# DEFAULT: lazy
# DESCRIPTION: Tell the program whether to provide lazy menu names or strict menu names.
#              If set to strict, it will use pre-defined menu strings based on the file URL
#              being processed. If set to lazy, it will use a portion of the actual file URL
#              as the menu name. Lazy is better for if you don't know all the datasets, strict
#              is only if the datasets you're processing are supported in the set_mname() function.
#              Only used if mnames == [].
#
mmethod = 'lazy'

####### colorurl #######
#
# NAME: colorurl
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: https://www.ral.ucar.edu/staff/dadriaan/jazz/colorscales
# DESCRIPTION: Local or remote URL for colorscale files
#
colorurl = "https://www.ral.ucar.edu/staff/dadriaan/jazz/colorscales"

####### exclude #######
#
# NAME: exclude
# OPTIONS:
# TYPE: list
# FORMAT:
# DEFAULT: []
# DESCRIPTION: List of strings to exclude
#
exclude = ['tile']

####### spdbpath #######
#
# NAME: spdbpath
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: ""
# DESCRIPTION: Path to SPDB data
#
spdbpath = ""

####### spdbhost #######
#
# NAME: spdbhost
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: ""
# DESCRIPTION: Which host serves SPDB data
#
spdbhost = ""

####### drawlatlon #######
#
# NAME: drawlatlon
# OPTIONS:
# TYPE: boolean
# FORMAT:
# DEFAULT: False
# DESCRIPTION: Include lat/lon labels
#
drawlatlon = False

####### addskewt #######
#
# NAME: addskewt
# OPTIONS:
# TYPE: boolean
# FORMAT:
# DEFAULT:
# DESCRIPTION:
#
addskewt = False

####### skewtURL #######
#
# NAME: skewtURL
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: ""
# DESCRIPTION: Path to files containing required variables for SKEW-T tool
#
skewtURL = ""

####### skewthost #######
#
# NAME: skewthost
# OPTIONS:
# TYPE: string
# FORMAT:
# DEFAULT: ""
# DESCRIPTION: Host where SKEW-T data reside
#
skewthost = ""

####### must_include #######
#
# NAME: must_include
# OPTIONS:
# TYPE: list
# FORMAT:
# DEFAULT: []
# DESCRIPTION: Provide a list of strings that the user wants included in the files processed and allowed in the param file.
#
must_include = []

"""

