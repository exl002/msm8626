#line 1 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/wcnss_pronto_image.scl"







 
#line 1 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/cust/customer.h"


















 















































 






 



 
#line 1 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/Pronto/bsp/prontoimg/inc/cust_pronto_img.h"

























 



 
#line 1 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/custscaqbazm.h"






 

#line 1 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/targscaqbazm.h"






 

#line 18 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/targscaqbazm.h"




#line 11 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/custscaqbazm.h"


#line 102 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/custscaqbazm.h"



#line 132 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/custscaqbazm.h"

#line 32 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/Pronto/bsp/prontoimg/inc/cust_pronto_img.h"



 






































 






 



 
 
 
 
 
 
 



#line 135 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/Pronto/bsp/prontoimg/inc/cust_pronto_img.h"

#line 198 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/Pronto/bsp/prontoimg/inc/cust_pronto_img.h"


#line 236 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/Pronto/bsp/prontoimg/inc/cust_pronto_img.h"



 
 
 
 
#line 310 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/Pronto/bsp/prontoimg/inc/cust_pronto_img.h"


#line 81 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/cust/customer.h"







 




























































































 
 




 




 





 




 
#line 247 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/cust/customer.h"

#line 10 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/wcnss_pronto_image.scl"


WCNSS_BOOT 0x0D200000
{
  BOOT_RO_REGION +0x0
  {
    boot_vectors.o (Int_Vect, +FIRST)
    boot_reset_handler.o (RST_Handler)
    bootapp.o (BOOTAPP_IVECT)
    boot_vectors.o (Boot_Block_Info)	
    boot* (+RO)
    crc.o (+RO)
    armmmu.o (+RO)
    
    
    rexarm.o (+RO)           
  }
  BOOT_RW_REGION +0x0
  {
    boot* (+RW)
    
    
   
    
  }
  BOOT_ZI_REGION +0x0
  {
    boot* (+ZI)
    
    
    
  }
}

 

PAGE_TABLE +0x0 ALIGN 0x00004000
{
   PAGE_TABLE +0x0
   {
     * (PAGE_TABLES)
   }
}


DEVCFG_DATA_SEG ImageLimit(PAGE_TABLE)
{
  DEVCFG_DATA +0x0
  {
   devcfg_pad.o(+RW)
  }
}


CMEM_DATA_SEG +0x0 0xE000
{
  CMEM_DATA_RW_REGION +0x0 EMPTY 0xE000
  {
  }  
}

WCNSS_NON_BOOT +0xE000
{
  RO_REGION +0x0
  {
    .ANY (+RO)
  }
  RW_REGION +0x0
  {
    .ANY(+RW)
    vmm.o (+ZI)
  }
  ZI_REGION +0x0
  {
    bootmem.o (+ZI)
    .ANY(+ZI)
  }
  UNINIT_RAM +0x0
  {
    *_nzi.o (+ZI)
	boot_stacks.o (Stacks, +LAST)
  }
}

#line 104 "/local/mnt/workspace/CRMBuilds/M8626AAAAANAZW12053645.1_20150311_075122/M8626AAAAANAZW12053645/wcnss_proc/build/ms/wcnss_pronto_image.scl"
DEBUG_DATA_SEG_MINI AlignExpr(ImageLimit(WCNSS_NON_BOOT),0x00010000)
{
  DEBUG_DATA_MINI_RW +0x0
  {
    * (DEBUG_REGION_MINI)
	rcinit_internal.o(+ZI)
  }  
}


 
AMSS_HEAP_SEG +0x0 ALIGN 0x1000
{
  HEAP_ZI +0x0
  {
    bootmem.o (AMSS_HEAP)
  }
}



UBSP_IMAGE +0x0 ALIGN 0x1000
{
  
  UBSP_RO_REGION 0xFB280000
  {
    ubsp_vectors.o (CMEM_VECT_TABLE, +FIRST)
    ubsp_vectors.o (UBSP_VECT_TABLE)	
	ubsp_reset_handler.o (RST_Handler)
    stack_protect.o (+RO)
    ubsp* (+RO)	
    lpwr* (+RO)
    etm.o (+RO)
    strlcpy.o
    llmul.o
    lludiv5.o
    memcmp.o
    rt_memclr.o	  
    rt_memclr_w.o 
    rt_memcpy.o   
    rt_memcpy_w.o 
    * (i.__ARM_common_ll_muluu)

    strlen.o
    aeabi_sdivfast.o
    __2snprintf.o
    aeabi_ldiv0_sigfpe.o
	aeabi_idiv0_sigfpe.o
    _printf_char_common.o
    _sputc.o
    rt_div0.o	
    defsig_fpe_formal.o	
    * (i.__ARM_common_udiv_6)
    * (i.__ARM_common_udiv_20)
    * (i.__ARM_common_sdiv_20)	

  }
  UBSP_RW_REGION +0x0 ALIGN 0x1000
  {
    ubsp* (+RW)	
    lpwr* (+RW)	
    stack_protect.o (+RW)
    etm.o (+RW)
    * (CMEM_SHARED_CFG_REGION)	
    ubsp_vectors.o (INDIRECT_VECT_TABLE)	
  }  
  UBSP_ZI_REGION +0x0
  {
    ubsp* (+ZI)	
    lpwr* (+ZI)	
    etm.o (+ZI)
  }  
  UBSP_UNINIT_RAM +0x0
  {
    ubsp_stacks.o (Stacks, +LAST)
  }
}




ScatterAssert((ImageLength(WCNSS_BOOT)+ImageLength(PAGE_TABLE)+ImageLength(DEVCFG_DATA_SEG)+ImageLength(UBSP_IMAGE)+ImageLength(CMEM_DATA_SEG)+ImageLength(WCNSS_NON_BOOT)+ImageLength(AMSS_HEAP_SEG))<0x0700000);
