#==============================================================================
# Target Build ID Config Script.
#
# Copyright (c) 2010 Qualcomm Technologies Inc.  All Rights Reserved
#==============================================================================

def exists(env):
   return env.Detect('tcfg_SCAQBAZM_data')

def generate(env):
   # Save the tcfg_bid_data in the env
   env['TCFG_BID_IMAGE'] = 'WCNSS_PROC'

   env.AddUsesFlags('USES_HAL', from_builds_file = True)
   env.AddUsesFlags('USES_SPLIT_CODE_DATA', from_builds_file = True)
   env.AddUsesFlags('USES_SMEM_LOG', from_builds_file = True)
   env.AddUsesFlags('USES_UBSP', from_builds_file = True)
   env.AddUsesFlags('USES_DIAG_SMD_SUPPORT', from_builds_file = True)
   env.AddUsesFlags('USES_SMI_CFG_DATA', from_builds_file = True)
   env.AddUsesFlags('USES_TIMER_STUBS', from_builds_file = True)
   env.AddUsesFlags('USES_DAL', from_builds_file = True)
   env.AddUsesFlags('USES_ERR', from_builds_file = True)
   env.AddUsesFlags('USES_RCINIT', from_builds_file = True)
   env.AddUsesFlags('USES_SMEM', from_builds_file = True)
   env.AddUsesFlags('USES_ARM_ASM_SPINLOCK', from_builds_file = True)
   env.AddUsesFlags('USES_MBNTOOLS', from_builds_file = True)
   env.AddUsesFlags('USES_EFS2', from_builds_file = True)
   env.AddUsesFlags('USES_STACK_PROTECTOR', from_builds_file = True)
   env.AddUsesFlags('USES_STRIP_NO_ODM', from_builds_file = True)
   env.AddUsesFlags('USES_ERR_INJECT_CRASH', from_builds_file = True)
   env.AddUsesFlags('USES_REX', from_builds_file = True)
