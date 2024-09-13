#!/bin/bash
echo "Setting run variables"

# where images will be saved
imgFolder=/mnt/1ABAA95DBAA93663/Users/Public/DATA/LTA/test_soft/ironman@LSC/
runname=test_run
lockfile=lockfile
# OUTPUT FOLDER
DAYFOLDER=$(date +"%Y%m%d")

# Sequencers that we will use
seqFolder=/home/centos/Documentos/LTA/ltadaemon-v2-main/lta-scripts/sequencers
#imageSeq=$seqFolder/clock1L/expose_binned_L1_ZFE.xml
#imageSeq=$seqFolder/sequencer_clean_binned_L1L2.xml
imageSeq=$seqFolder/sequencer_clean_binned.xml
#imageSeq=$seqFolder/sequencer_microchip_binned_brenda.xml
idleSeq=$seqFolder/clock1L/idle.xml
cleanSeq=$seqFolder/clock1L/clean.xml

name=$imgFolder/lta_img_${DAYFOLDER}_seqc4Amp_cleanSeparate_noA_3x3_testmix_VHM_120K_vsub50_150sg_
# voltage variables
# voltage_setup=voltage_skp_lta_v2.sh
volFolder=/home/centos/Documentos/LTA/ltadaemon-v2-main/lta-scripts/voltages
#voltage_setup=$volFolder/voltage_setup_Maria.sh
voltage_setup=$volFolder/voltage_setup_mix.sh

# cds variables

# Integration width = (cdsSAMP+cdsSINIT+seqSIGEXTRA)/15 in untits of micro seconds
cdsSAMP=225 #ssamp and psamp for signal and pedestal samples
cdsSINIT=40 #unit is number of clock cycles (15 Mhz)
cdsPINIT=30
seqPEDEXTRA=10
seqSIGEXTRA=10
cdsout=3 # 3 for differential-Amp, 2 for Op-Amp only

# Number of skips
skpNSAMP=1

skpNROW=270
skpNCOL=1183

# Number of columns and rows
#skpNROW=1650
#skpNCOL=6250

# Binning
skpNBINROW=3
skpNBINCOL=3

# Exposition time
skpEXP=150

# Substrae voltage
VSUB=50



