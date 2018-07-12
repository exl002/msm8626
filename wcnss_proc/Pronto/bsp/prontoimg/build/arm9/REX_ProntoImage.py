#===============================================================================
#
# CoreBSP Modem CPU build script
#
# GENERAL DESCRIPTION
#    build script
#
# Copyright (c) 2009-2009 by Qualcomm Technologies, Incorporated.
# All Rights Reserved.
# QUALCOMM Proprietary/GTDR
#
#-------------------------------------------------------------------------------
#
#  $Header: //source/qcom/qct/core/pkg/wcnss/pr/rel/2.1/Pronto/bsp/prontoimg/build/arm9/REX_ProntoImage.py#3 $
#  $DateTime: 2013/07/03 18:30:20 $
#  $Author: coresvc $
#  $Change: 4043138 $
#                      EDIT HISTORY FOR FILE
#
#  This section contains comments describing changes made to the module.
#  Notice that changes are listed in reverse chronological order.
#
# when       who     what, where, why
# --------   ---     ---------------------------------------------------------
#
#===============================================================================
from SCons.Script import *

import subprocess

def mapscan (target = None, source = None, env = None):
    image_limit = ""
    for cppdef in env['CPPDEFINES']:
        defname = cppdef.split('=')
        if defname[0] == 'WCNSS_CODE_SIZE' :
            image_limit = '-L'+defname[1]

    target_name=str(target[0])
#    return subprocess.call([env['PYTHONCMD'], env.subst('${BUILD_SCRIPTS_ROOT}/rvct_mapscan.py'),
    return subprocess.call([env['PYTHONCMD'], 'rvct_mapscan.py',
                     os.path.dirname(target_name), '-s', image_limit ])


#------------------------------------------------------------------------------
# Hooks for Scons
#------------------------------------------------------------------------------
def exists(env):
   return env.Detect('Pronto Image')

def generate(env):
   #-------------------------------------------------------------------------
   # Libs/Objs
   #-------------------------------------------------------------------------
   prontoimg_libs_path = env.get('INSTALL_LIBPATH')
   prontoimg_libs = env.get('PRONTOIMG_LIBS')
   prontoimg_objs = env.get('PRONTOIMG_OBJS')      

   prontoimg_units = [prontoimg_libs, prontoimg_objs]
   
   # filter is not define or filter is current target files only, ok to build misc files
   if 'IMAGE_BUILD_LOCAL_FILES' in env:   
      #=========================================================================
      # Pronto Image section
      #=========================================================================
   
      # make our clone so we won't mess the lib rules, it shoun't because they 
      # should of clone, but just to be on the safe side.
      env = env.Clone()
      
      #-------------------------------------------------------------------------
      # Source PATH
      #-------------------------------------------------------------------------
      #ProntoIMG_SRC = "${COREBSP_ROOT}/bsp/coreimg/src"

      #env.VariantDir("${BUILDPATH}", ProntoIMG_SRC, duplicate=0)

      #-------------------------------------------------------------------------
      # External depends within CoreBSP
      #-------------------------------------------------------------------------
      env.RequireExternalApi([
         'DSM',
         'MODEM_API',
      ])

      #-------------------------------------------------------------------------
      # Internal depends within CoreBSP
      #-------------------------------------------------------------------------
      CBSP_API = [
         'BOOT',
         'BUSES',
         'DAL',
         'DEBUGTOOLS',
         'HAL',      
         'HWENGINES',
         'IODEVICES',
         'MPROC',
         'POWER',
         'SECUREMSM',
         'SERVICES',
         'STORAGE',
         'SYSTEMDRIVERS',
         'WIREDCONNECTIVITY',
         
         # needs to be last also contains wrong comdef.h
         'KERNEL',
      ]

      env.RequirePublicApi(CBSP_API)
      env.RequireRestrictedApi(CBSP_API)
      
      #=========================================================================
      # Beging building QCOREIMG
      #
      #----------------------------------------------------------------------------
      # Build env scatter load
      #----------------------------------------------------------------------------
      target_scl = env.SclBuilder('${SHORT_BUILDPATH}/${TARGET_NAME}_pre_reloc_changes', [
		 '${BUILD_MS_ROOT}/wcnss_pronto_image',
      ])
      
      prontoimg_units += target_scl
      
      #----------------------------------------------------------------------------
      # Sources, libraries
      #----------------------------------------------------------------------------

      # stubs and other qcore app files
      #PRONTOIMG_STUBS_SOURCES = [
      #   '${BUILDPATH}/other_stubs.c',    
      #]
      
      #prontoimg_objs.extend(env.Object(PRONTOIMG_STUBS_SOURCES))      

   # the following steps can only be performed if there is no filters in effect
   if 'IMAGE_BUILD_LINK' in env:   
		#-------------------------------------------------------------------------
		# Build env for Pronto image
		#-------------------------------------------------------------------------
		prontoimg_elf_pre_reloc_changes = env.AddProgram("${SHORT_BUILDPATH}/${TARGET_NAME}_pre_reloc_changes", prontoimg_objs, LIBS=prontoimg_libs)

		if 'USES_RELOC_ENABLE_AND_ALIGN' in env:
			prontoimg_elf = env.ModifyRelocatableFlagsBuilder( '${SHORT_BUILDPATH}/M${TARGET_FAMILY}${BUILD_ID}${BUILD_VER}.elf', prontoimg_elf_pre_reloc_changes )
		else:
			prontoimg_elf = prontoimg_elf_pre_reloc_changes
			 
		env.Depends(prontoimg_elf, target_scl)

		map_action = Action(mapscan,'=== Gathering image size statistics')
		env.AddPostAction(prontoimg_elf, map_action)
		

		# copy elf and reloc to needed locations for AMSS tools to load on target
		if 'USES_PRONTO_MEMORY_REDUCED' in env:
			install_target_elf = env.InstallAs(
			 #'${BUILD_MS_ROOT}/${CHIPSET}_${IMAGE_NAME}.elf', rivaimg_elf)
			'${BUILD_MS_ROOT}/${MSM_ID}_PRONTO_NODEVCFG_MR.elf', prontoimg_elf)
		else:
			install_target_elf = env.InstallAs(
			 #'${BUILD_MS_ROOT}/${CHIPSET}_${IMAGE_NAME}.elf', rivaimg_elf)
			'${BUILD_MS_ROOT}/${MSM_ID}_PRONTO_NODEVCFG.elf', prontoimg_elf)
      
		# #-------------------------------------------------------------------------
		# # Build env mbn files
		# #-------------------------------------------------------------------------
		# target_mbn = env.MbnBuilder('${TARGET_NAME}', prontoimg_elf, IMAGE_TYPE="wcnss",
		 # FLASH_TYPE=env['TARGET_FLASH_TYPE'], ENABLE_ENCRYPT=True)

		# target_mbn_copy = env.Install("${BUILD_ROOT}/build/ms/bin/${MSM_ID}/", target_mbn)

		# #-------------------------------------------------------------------------
		# # Run PIL Splitter Tool
		# #-------------------------------------------------------------------------
		# split_files = env.PilSplitterBuilder('${BUILD_ROOT}/build/ms/bin/${MSM_ID}/PIL_IMAGES/${MSM_ID}_SPLITBINS_${QC_SHORT_BUILDPATH}/wcnss.mdt', target_mbn)
		 
		#============================================================================
		# Define targets needed RIVA QCOREIMG
		prontoimg_units = env.Alias ('pronto_img_units', [
		 install_target_elf
		 #target_mbn,
		 #target_mbn_copy,
		 #split_files
      ])

   #print env.Dump()

   #=========================================================================
   # Finish up...
   env.BindAliasesToTargets(prontoimg_units)
