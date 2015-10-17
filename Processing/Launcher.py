#!/usr/bin/env python

import os
import sys
import argparse
import commands
import shutil
import tempfile
import time

from optparse import OptionParser
from optparse import OptionGroup

import nipype.interfaces.minc as minc
import nipype.pipeline.engine as pe
import nipype.interfaces.io as nio
import nipype.interfaces.utility as util
from nipype.interfaces.utility import Rename

from ScanConstructor import * 

version = "1.0"


sys.path.append('')
sys.path.append('/dagher/dagher1/klarcher/git/tka_nipype/Masking')


def printOptions(opts,args):
	uname = os.system('uname -s -n -r')

	print "\n* Pipeline started at "+time.strftime("%c")+"on "+uname
	print "\n* Command line is:\n  %prog"+str(sys.argv)+"\n"
	print "\n* The source directory is:"+opts.sourceDir+"\n"
	print "\n* Data-set Subject ID(s) is/are:"+args+"\n";
	print "\n* PET conditions :"+opts.condiList+"\n";
	print "\n* ROI labels :"+opts.ROILabels+"\n";

def initPipeline(opts,args):
	if args:
		id_subjs = args
	else:
		print "\n\n*******ERROR********: \n     The subject IDs are not listed in the command-line \n********************\n\n"
		sys.exit(1)

	for id in id_subjs:
		scan.set_filenames(opts,id)

def runPipeline(scan,opts):	
	node1 = pe.Node(interface=minc.AverageCommand(), name="pet_volume")
	node1.inputs.input_file='/dagher/dagher4/klarcher/nipype_test/data/gluta_015_0_fwhm4_real.mnc'
	node1.inputs.out_file='/dagher/dagher4/klarcher/nipype_test/data/gluta_015_0_fwhm4_real_sum.mnc'
	node1.inputs.avgdim='time'
	node1.inputs.width_weighted=True


	node2 = pe.Node(interface=reg.PETtoT1LinRegRunning(), name="node2")
	node2.inputs.input_source_file = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_0_real_resh_sum.mnc';
	node2.inputs.input_target_file = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_t1_nuc.mnc';
	node2.inputs.input_source_mask = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_0_headmask.mnc';
	node2.inputs.input_target_mask = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_head_mask_native.mnc';
	node2.inputs.out_file_xfm = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_0_petmri.xfm';
	node2.inputs.out_file_img = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_0_petmri.mnc';
	node2.inputs.clobber = True;
	node2.inputs.verbose = True;
	node2.inputs.run = True;


	node3 = pe.Node(interface=masking.T1maskingRunning(), name="node3")
	node3.inputs.nativeT1 = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/native/gluta_015_t1_nuc.mnc';
	node3.inputs.LinT1TalXfm = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_t1_tal.xfm';
	node3.inputs.brainmaskTal = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/mask/gluta_015_skull_mask.mnc';
	node3.inputs.modelDir = '/data/movement/movement7/klarcher/share/icbm';
	node3.inputs.T1headmask = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_t1_headmask.mnc';
	node3.inputs.T1brainmask = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_t1_brainmask.mnc';
	node3.inputs.clobber = True;
	node3.inputs.run = False;
	node3.inputs.verbose = True;

	node4 = pe.Node(interface=masking.RefmaskingRunning(), name="node4")
	node4.inputs.nativeT1 = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/native/gluta_015_t1_nuc.mnc';
	node4.inputs.T1Tal = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/final/gluta_015_t1_final.mnc';
	node4.inputs.LinT1TalXfm = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_t1_tal.xfm';
	node4.inputs.brainmaskTal  = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/mask/gluta_015_skull_mask.mnc';
	node4.inputs.clsmaskTal  = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/classify/gluta_015_pve_classify.mnc';
	node4.inputs.segMaskTal  = '/dagher/dagher4/klarcher/nipype_test/data/civet/gluta/015/segment/gluta_015_stx_labels_masked.mnc'
	node4.inputs.segLabels = [67, 76];
	node4.inputs.MaskingType = "no-transform"
	node4.inputs.modelDir = '/dagher/dagher4/klarcher/atlases/icbm152/';
	node4.inputs.RefmaskTemplate  = '/dagher/dagher5/klarcher/tvincent/neuroecon/apROI/template/minc/Hammers_mith_atlas_n30r83_SPM5_icbm152_asym_vmPFC.mnc';
	node4.inputs.close = True;
	node4.inputs.refGM = True;
	node4.inputs.refWM = False;
	node4.inputs.RefmaskTal  = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_tal_refmask.mnc';
	node4.inputs.RefmaskT1  = '/dagher/dagher4/klarcher/nipype_test/data/gluta_015_t1_refmask.mnc';
	node4.inputs.clobber = True;
	node4.inputs.run = False;
	node4.inputs.verbose = True;




	workflow = pe.Workflow(name='preproc')






def get_opt_list(option,opt,value,parser):
	setattr(parser.values,option.dest,value.split(','))

# def printStages(scan,opts):


# def printScan(scan,opts):



if __name__ == "__main__":

	usage = "usage: %prog "

	parser = OptionParser(usage=usage,version=version)

	# group= OptionGroup(parser,"File options","Mandatory")
	group= OptionGroup(parser,"File options (mandatory)")
	group.add_option("-s","--sourcedir",dest="sourceDir",help="Native pet and mri directory")
	group.add_option("-t","--targetdir",dest="targetDir",help="Directory where output data will be saved in")
	group.add_option("-p","--prefix",dest="prefix",help="Study name")
	group.add_option("-c","--civetdir",dest="civetDir",help="Civet directory")
	parser.add_option_group(group)		

	group= OptionGroup(parser,"Scan options","***if not, only baseline condition***")
	group.add_option("","--condition",dest="condiList",help="comma-separated list of conditions or scans",type='string',action='callback',callback=get_opt_list,default='baseline')
	parser.add_option_group(group)		

	group= OptionGroup(parser,"Registration options")
	# PERL :
	# ["-template", "string", 1, \$template, "Template to resample the subject MR image in strereostatix space."],
	# ["-fr-range-reg", "integer", 2, \@rangeFramesReg, "Frames range for MRI/PET registration."],
	# ["-manual-mripet", "const", "manual-reg", \$manual_reg, "Use manual MRI/PET registration."], 
	# ["-no-manual-mripet", "const", "no-manual-reg", \$manual_reg, "Compute manual MRI/PET registration. [default]"], 
	parser.add_option_group(group)		

	group= OptionGroup(parser,"PET acquisition options")
	# PERL :
	# ["-motions-corr", "const", "motions", \$motions_corr, "Correct for the head motions. [default]"], 
	# ["-no-motions-corr", "const", "no-motions", \$motions_corr, "Don't correct for the head motions. The dynamic PET image need to be provided."], 
	# ["-target-fr", "integer", 2, \@targetFr, "Frames range used for creating target volume that will be used for realigning each frame."],
	# ["-target-all-fr", "integer", 1, \$targetFrAll, "Use all frames for creating target volume. [default]"],
	# ["-remove-fr", "const", "remove-fr", \$remove_fr, "Run the frame removing."], 
	# ["-no-remove-fr", "const", "no-remove-fr", \$remove_fr, "Don't run the frame removing."], 
	# ["-exclude-fr", "call", [\@excludeFr], \&ParseOption, "Frames to exclude."],
	# ["-exclude-fr-time", "call", [\@excludeFrTime], \&ParseOption, "Width-Time of frames to exclude."],
	# ["-smooth", "integer", 1, \$smooth, "FWHM value to blur the dynamic pet image."], 
	parser.add_option_group(group)
		
	group= OptionGroup(parser,"Masking options","Reference region")
	group.add_option("","--ref-animal",dest="refValueAnimal",help="Label value(s) from ANIMAL segmentation. By default, the values correspond to the cerebellum",type='string',action='callback',callback=get_opt_list,default=['67','76'])
	group.add_option("","--ref-gm",dest="refMatter",help="Gray matter of reference region (if -ref-animal is used)",action='store_const',const='gm',default='gm')
	group.add_option("","--ref-wm",dest="refMatter",help="White matter of reference region (if -ref-animal is used)",action='store_const',const='wm',default='gm')
	group.add_option("","--ref-template",dest="templateRef",help="Template to segment the reference region.",default='/home/klarcher/bic/models/icbm152/mni_icbm152_t1_tal_nlin_sym_09a.mnc')
	group.add_option("","--ref-linreg",dest="refRegister",help="Non-linear registration based segmentation",action='store_true',default=False)
	group.add_option("","--ref-no-linreg",dest="refRegister",help="Don't run any non-linear registration",action='store_false',default=False)
	group.add_option("","--ref-close",dest="refClose",help="Close - erosion(dialtion(X))",action='store_true',default=False)
	group.add_option("","--ref-mask",dest="refOnTemplate",help="Reference mask on the template",default=None)	
	parser.add_option_group(group)
	group= OptionGroup(parser,"Masking options","Region Of Interest")
	group.add_option("","--roi-animal",dest="roiValueAnimal",help="Label value(s) from ANIMAL segmentation.",type='string',action='callback',callback=get_opt_list)
	group.add_option("","--roi-linreg",dest="roiRegister",help="Non-linear registration based segmentation",action='store_true',default=False)
	group.add_option("","--roi-no-linreg",dest="roiRegister",help="Don't run any non-linear registration",action='store_false',default=False)
	group.add_option("","--roi-template",dest="templateROI",help="Template to segment the ROI.",default='/home/klarcher/bic/models/icbm152/mni_icbm152_t1_tal_nlin_sym_09a.mnc')
	group.add_option("","--roi-template-suffix",dest="templateROIsuffix",help="Suffix for the ROI template.",default='icbm152')
	group.add_option("","--roi-mask",dest="ROIOnTemplate",help="ROI mask on the template",default='/home/klarcher/bic/models/icbm152/mni_icbm152_t1_tal_nlin_BG_mask_6lbl.mnc')	
	group.add_option("","--roi-suffix",dest="ROIsuffix",help="ROI suffix",default='striatal_6lbl')	
	group.add_option("","--roi-labels",dest="ROILabels",help="ROI labels",type='string',action='callback',callback=get_opt_list,default=['4','5','6','9','10','11'])
	group.add_option("","--roi-erosion",dest="roiErosion",help="Erode the ROI mask",action='store_true',default=False)
	parser.add_option_group(group)

	group= OptionGroup(parser,"Tracer Kinetic analysis options")
	# PERL :
	# ["-param", "const", "parametric", \$param, "Compute modelling parameters. [default]"], 
	# ["-no-param", "const", "no-parametric", \$param, "Don't compute modelling parameters. Stop just after the registration MRI/PET."], 
	# ["-vox-wise", "const", "vox", \$analysis, "Run voxel-wise analysis."],
	# ["-regional", "const", "regional", \$analysis, "Run regional analysis." ], 
	# ["-regional-stx", "const", "regional-stx", \$analysis, "Run regional analysis, using the mask in the stereotaxic space." ], 
	# ["-srtm-gunn", "const", "gunn", \$mapping, "Create the Receptors Parametric Maps, from the matlab script written by Roger GUNN (some matlab librairies are necessary)."],
	# ["-srtm-turku", "const", "turku", \$mapping, "Create the Receptors Parametric Maps, using Turku tools." ], 
	# ["-theta3", "float", 2, \@theta3val, "Minimal and maximal values of theta3 (min max)."],
	# ["-ligand", "integer", 1, \$ligand, "Ligand."],
	parser.add_option_group(group)

	group= OptionGroup(parser,"Pipeline control")
	group.add_option("","--run",dest="prun",help="Run the pipeline.",action='store_true',default=False)
	group.add_option("","--fake",dest="pfake",help="do a dry run, (echo cmds only).",action='store_true',default=True)
	group.add_option("","--print-scan",dest="pscan",help="Print the pipeline parameters for the scan.",action='store_true',default=False)
	group.add_option("","--print-stages",dest="pstages",help="Print the pipeline stages.",action='store_true',default=False)
	# PERL :
	# ["-run", "const", "run", \$command, "Run the pipeline."],
	# ["-status-from-files", "const", "statusFromFiles", \$command, "Compute pipeline status from files"],
	# ["-print-stages", "const", "printStages", \$command, "Print the pipeline stages."],
	# ["-print-status", "const", "printStatus", \$command, "Print the status of each pipeline."],
	# ["-make-graph", "const", "makeGraph", \$command, "Create dot graph file."],
	# ["-make-filename-graph", "const", "makeFilenameGraph", \$command, "Create dot graph of filenames."],
	# ["-print-status-report", "const", "printStatusReport", \$command, "Writes a CSV status report to file in cwd."],
	parser.add_option_group(group)

	(opts, args) = parser.parse_args()

	opts.extension='mnc.gz'

	if not opts.sourceDir or not opts.targetDir or not opts.civetDir or not opts.prefix:
		print "\n\n*******ERROR******** \n     You must specify -sourcedir, -targetdir, -civetdir  and -prefix \n********************\n"
		parser.print_help()
		sys.exit(1)
	
	if opts.refRegister and opts.templateRef:
		print "\n\n*******ERROR******** \n     You can't use the options -ref-no-transf and -ref-template together \n********************\n"
		parser.print_help()
		sys.exit(1)
	
	opts.targetDir = os.path.normpath(opts.targetDir)
	opts.sourceDir = os.path.normpath(opts.sourceDir)
	opts.civetDir = os.path.normpath(opts.civetDir)
	# PERL :
	# if (@targetFr) {$targetFrAll = 0;}

	scan = PipelineFiles()
	initPipeline(opts,args)

	if opts.prun or opts.pfake:
		runPipeline(scan,opts)
	elif opts.pscan:
		printScan(scan,opts)
	elif opts.pstages:
		printStages(scan,opts)
	else:
		print "\n\n*******ERROR********: \n    The options -run, -print-scan or print-stages need to be chosen \n********************\n\n"
		parser.print_help()
