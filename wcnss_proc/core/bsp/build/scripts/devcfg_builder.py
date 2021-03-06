#===============================================================================
#
# Device Config Builder
#
# GENERAL DESCRIPTION
#    Contains builder(s) defenitions
#
# Copyright (c) 2011 by Qualcomm Technologies, Incorporated.
# All Rights Reserved.
# QUALCOMM Proprietary/GTDR
#
#-------------------------------------------------------------------------------
#
#  $Header: //components/rel/core.wcnss/2.1.c16/core/bsp/build/scripts/devcfg_builder.py#1 $
#  $DateTime: 2014/06/10 11:46:41 $
#  $Author: coresvc $
#  $Change: 6057513 $
#                      EDIT HISTORY FOR FILE
#                      
#  This section contains comments describing changes made to the module.
#  Notice that changes are listed in reverse chronological order.
#  
# when       who     what, where, why
# --------   ---     ---------------------------------------------------------
# 11/14/11   jay     Device Configuration builder implementation
#===============================================================================

import os
import subprocess
import string
from SCons.Script import *

#------------------------------------------------------------------------------
# Globals
#------------------------------------------------------------------------------
DEVCFG_ENV_DESCRIPTOR = 'DEVCFG_INFO_COLLECTOR'
DEVCFG_XML = 'devcfg_xml'
DALCFG_DEV_ID = 'dalcfg_id'
PP_XML = 'pp_xml'

#------------------ path2hash
AU_MASK = 4
MACRO_MASK = 18
# ----------|------------------|--------
#   AU (4)  | Driver ID (10) |  Macro (18)   

#------------------------------------------------------------------------------
# Hooks for Scons
#------------------------------------------------------------------------------
def exists(env):
    return True

def generate(env):
    """
    Generate function for devcfg builder. 
    Sets up the action, scanner and builder function to be called by clients to
    pass xml, devId details to the builder.
    """

    rootenv = env.get('IMAGE_ENV')

    rootenv[DEVCFG_ENV_DESCRIPTOR] = []
    
    # Add method to enviroment. 
    # AddDevCfgInfo is the function that needs to be called by the clients to pass
    # dev cfg xml file name with location, devID is needed to be added, APIs needed
    # to compile any .h files included in the xml file.
    rootenv.AddMethod(add_devcfg_info, "AddDevCfgInfo")
    
    # load builder into enviroment
    devcfg_act = env.GetBuilderAction(devcfg_xml_builder,action_source=None)
    devcfg_target_scan = env.Scanner(devcfg_target_scan_func, name='DevCfgSrcScanner')
    devcfg_bld = env.Builder(action = devcfg_act,
                             target_scanner = devcfg_target_scan,
                             suffix = '.xml')
    rootenv.Append(BUILDERS = {'DevcfgBuilder' : devcfg_bld})
    
    return
    
def devcfg_target_scan_func(node, env, path):
    """
    Scanner adds the include paths to dal config environment which will 
    be used to compile autogenerated c files while rebuilding. This gets
    called from the dal config scons environment.
    """
    rootenv = env.get('IMAGE_ENV')    
   
    
    #Instead of returning any nodes just add the PP XMLs as deps
    [env.Depends(node, sub_dict.get(PP_XML, [])) for sub_dict in  rootenv.get('DEVCFG_INFO_COLLECTOR', [])]

    return []
    
def add_devcfg_info(env, targets, thread_input_dict):
    """
    When AddDevCfgInfo is called by the client, this add_devcfg_xml gets invoked in the
    devcfg builder env & the details passed by the clients are stored in a dictionary here.
    """
    #import pdb;pdb.set_trace()
    rootenv = env.get('IMAGE_ENV')
    if rootenv.GetUsesFlag('USES_DEVCFG') is False:
        return
        
    # Dictionary to hold dal device id and device config xml locations
    newDict = {}
    
    # DEVCFG_XML needs to be passed whenever AddDevCfgInfo is called from the client scons file.
    if DEVCFG_XML not in thread_input_dict:
        devcfg_error(env, DEVCFG_XML + 'required')

    # Devcfg xml filename along with the path is stored in the dictionary
    newDict[DEVCFG_XML] = thread_input_dict[DEVCFG_XML]
    # Check to see if the xml file passed through scons exists
    if env.PathExists(newDict[DEVCFG_XML]) is False:
        errStr = 'File not found: ' + str(newDict[DEVCFG_XML])
        devcfg_error(env, errStr)
    
    # Check for duplicates in the xml files passed in
    for grpList in rootenv[DEVCFG_ENV_DESCRIPTOR]:
        if newDict[DEVCFG_XML] == grpList.get(DEVCFG_XML, "BADXMLFILE"):
           # If its a duplicate, do not process
           env.PrintWarning("Duplicate Device Configuration Input File Specified " + str(newDict[DEVCFG_XML]))
           return           
    
    #Full path to the XML file
    xml_fullpath = env.RealPath(newDict.get(DEVCFG_XML))
    #Obtain just the file name + ext
    xml_fname = os.path.basename(xml_fullpath)
    #Preprocess the XML
    pp_xml = env.PreProcess('${BUILDPATH}/' + xml_fname + '.pp', newDict.get(DEVCFG_XML))
    #Cleanup the Preprocessed XML
    pp_xml_cl = env.PreProcessClean('${BUILDPATH}/' + xml_fname + '.i', pp_xml)
    newDict[PP_XML] = pp_xml_cl

    # Add the user supplied info to the rootenv dictionary
    rootenv[DEVCFG_ENV_DESCRIPTOR].append(newDict)
    #print 'rootenv[DEVCFG_ENV_DESCRIPTOR]: ', rootenv[DEVCFG_ENV_DESCRIPTOR]
        
    return
    
def path2Hash(env, dic):
    # Setting up the Masks
    M1 = (0xFFFFFFFF << (32 - AU_MASK))& 0xFFFFFFFF # need to and it with 0xFFFFFFFF to keep it 32bits.
    M3 = 0xFFFFFFFF>>(32-MACRO_MASK)
    M2 = (~(M1 | M3))&0xFFFFFFFF
    # AU dictionary to prevent recalculating Hash number for each AU.
    AU_lookUp={}
    # Hash_list make sure there are NO duplicates in hash list. 
    # 0 is reserved for backwards compatibility
    hash_list = [0]
    for macro, path in dic.iteritems():
        # Filtering AU         
        Current_path = path[0].split('/', 2 );
        AU = Current_path[0]+"/"+Current_path[1];
        ID = path[1]
        # If the Hash was generated before?
        if not AU_lookUp.has_key(AU):
            AU_lookUp[AU] = hash(AU) & M1
        # Removing the item since the new value has different type (from list to int)
        del dic[macro]
        dic[macro]= AU_lookUp[AU] |(hash(macro.replace("DALDEVICEID_","")) & M2)|(ID&M3) # if macro may have DALDEVICEID_ prefix, will be removed.
        hash_list.append(dic[macro])
    if(len(hash_list)==len(set(hash_list))):
        return dic
    else:
        devcfg_error(env,"Error ... Could not generate unique IDs")

    return

def devcfg_xml_builder(target, source, env):
    """
    devcfg_xml_builder gets invoked as its a rule in dal\config\SConscript to create the master xml file
    and DALDeviceId_autogen.h.
    The master xml file will be the #includes of all the xml files passed by the clients.
    DALDeviceId_autogen.h will have #define for all the dal device ids passed thro' the drivers' scons file.
    target[0] will have the master xml location & name.
    target[1] will have the location & name for DALDeviceId_autogen.h.
    """
    rootenv = env.get('IMAGE_ENV')
    
    # Save the caller environment as the APIs for the include files need to be added to
    # the dal config build environment
    caller_env = env
    
    if rootenv.GetUsesFlag('USES_DEVCFG') is False:
        return None
    
    # Check for duplicate dal dev id macros
    dictHashIn = check_daldevid_macro_dups(rootenv)
    dalDevIdHashDict = {}
    
    # Creation of master dal xml file
    target_full = env.RealPath(str(target[0]))
    master_xml = devcfg_create_master_xml_file(rootenv, target_full)
    
    return
    
def devcfg_create_master_xml_file(env, filepathname):
    """
    devcfg_create_master_xml_file creates the master dal xml file that includes all the 
    xml files passed in by various scons files
    """
    # Determine the module name that needs to be added to the module tag in the xml file
    moduleName = ''
    proc_name = env.get('PROC_CONFIG')
    
    if proc_name == 'wcn':
        moduleName = 'wcn'
    elif proc_name == 'modem':
        moduleName = 'modem'
    elif env.has_key('CORE_SPS'):
        moduleName = 'dsps'
    elif env.has_key('CORE_RPM') or env.has_key('RPM_IMAGE'):
        moduleName = 'rpm'
    elif env.has_key('TZOS_IMAGE'):
        moduleName = 'tz'
    elif env.has_key('BUILD_BOOT_CHAIN') or env.has_key('BUILD_TOOL_CHAIN'):
        moduleName = 'boot'
    elif env.has_key('APPS_PROC'):
        moduleName = 'apps'
    else:
        # If none of the above are applicable, then throw an error to indicate 
        # that a proper build env needs to be present for module name
        devcfg_error(env, 'Need image definition for determining module name for dal master cfg file')
    moduleNameStr = '<module name="' + moduleName + '">\n'
    
    # Create the master xml file and open for writing
    try:
        devcfg_xml_file = open(filepathname, 'w')
    except IOError:
        errStr = 'Could not create dal master XML file' + filepathname
        devcfg_error(env, errStr)

    # Add the include files and the xml header tags
    devcfg_xml_file.write('#include "DALPropDef.h"\n')
    devcfg_xml_file.write('#include "DALDeviceId.h"\n')
    devcfg_xml_file.write('#include "dalconfig.h"\n\n')
    devcfg_xml_file.write('<?xml version="1.0"?>\n')
    devcfg_xml_file.write('<dal>\n')
    devcfg_xml_file.write(moduleNameStr)
    
    # Write all the xml files as #includes in the xml file
    for xml_loc in env[DEVCFG_ENV_DESCRIPTOR]:
        #devcfg_xml_file.write('#include "' + os.path.normpath(xml_loc[DEVCFG_XML]) + '"\n')
        devcfg_xml_file.write(xml_loc[PP_XML][0].get_contents())
        devcfg_xml_file.write('\n')
    
    # Write the closing tags
    devcfg_xml_file.write('</module>' + '\n')
    devcfg_xml_file.write('</dal>\n')        
        
    # Close the file
    devcfg_xml_file.close()
    
    return
    

                        
def check_daldevid_macro_dups(env):
    """
    Function to check if the dal device id macros passed by the drivers' scons 
    files have duplicates. Dal device ID macros have to be unique through out
    the system. This function also creates dictionary to be passed to the 
    function that will generate the hash values for the IDs.
    """

    # dalDevIdMacroList will hold all the dal device ids passed in by the drivers
    dalDevIdMacroList = []
    # Dictionary to be passed to the hash fn - dictHashIn = {'DALDeviceId_MACRO' : [xml_file, devId_val]}
    dictHashIn = {}
    # eachSconsInput is a dictionary of all the info extracted from user scons file
    for eachSconsInput in env[DEVCFG_ENV_DESCRIPTOR]:
        if eachSconsInput.has_key(DALCFG_DEV_ID) is True and eachSconsInput.has_key(DEVCFG_XML) is True:
            for devIdMacro, devIdVal in eachSconsInput[DALCFG_DEV_ID].iteritems():
                # Strip the leading ${TARGET_ROOT} as this is not used for hashing
                xml_stripped_path = eachSconsInput[DEVCFG_XML].lstrip(str(env.get('TARGET_ROOT', None)))
                # Eg: {'DALDEVICEID_GPIOINT1': ['wcnss_proc\core\systemdrivers\GPIOInt\config\GPIOInt.xml', 1}
                dictHashIn[str(devIdMacro)] = [xml_stripped_path, devIdVal]
                dalDevIdMacroList.append(str(devIdMacro))
                # Set of a list will remove duplicates. Hence, if the length of the list before and creating
                # a set has to be same if there are no duplicates in the list.
                if len(dalDevIdMacroList) != len(set(dalDevIdMacroList)):
                    devcfg_error(env, 'Duplicate Dal Macro names', dalDevIdMacroList)
                    
    return dictHashIn


def devcfg_error(env, Info, Info1=None):
    """
    Error handler for devcfg framework. Info can be a string that describes the error and
    Info1 can be any data that needs to be printed along with the error message.
    """
    env.PrintError("DevCfg error found: " + Info)
    env.PrintError(Info1)
    raise Exception(Info)