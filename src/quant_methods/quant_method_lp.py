from quantification_template import *

in_file_format="NIFTI"
out_file_format="NIFTI"
reference=True
voxelwise=True


class quantOutput(TraitedSpec):
    out_file = File(argstr="%s",  desc="Parametric image")

class quantInput( CommandLineInputSpec):
    out_file = File(argstr="%s",  position=-1, desc="image to operate on")
    in_file= File(exists=True, mandatory=True, position=-3, argstr="%s", desc="PET file")
    reference = File(exists=True, mandatory=True,  position=-4, argstr="%s", desc="Reference file")
    sif = File(desc="Sif file for Nifti PET input")
    start_time=traits.Float(argstr="%s",default_value=0, usedefault=True,  position=-2, desc="Start time for regression in mtga.")
    k2=  traits.Float(argstr="-k2=%f", desc="With reference region input it may be necessary to specify also the population src for regerence region k2")
    thr=traits.Float(argstr="-thr=%f", desc="Pixels with AUC less than (threshold/100 x max AUC) are set to zero. Default is 0%")
    Max=traits.Float(argstr="-max=%f",default=10000, use_default=True, desc="Upper limit for Vt or DVR values; by default max is set pixel-wise to 10 times the AUC ratio.")
    Min=traits.Float(argstr="-min=%f", desc="Lower limit for Vt or DVR values, 0 by default")
    Filter=traits.Bool(argstr="-filter",  desc="Remove parametric pixel values that over 4x higher than their closest neighbours.")
    end=traits.Float(argstr="-end %f", desc="By default line is fit to the end of data. Use this option to enter the fit end time.")
    v=traits.Str(argstr="-v %s", desc="Y-axis intercepts time -1 are written as an image to specified file.")
    n=traits.Str(argstr="-n %s", desc="Numbers of selected plot data points are written as an image.")
    
    
class quantCommand(quantificationCommand):
    input_spec =  quantInput
    output_spec = quantOutput
    _cmd = "imgdv"  
    _suffix = "_lp" 


class QuantCommandWrapper(srcCommandWrapper):
    input_spec =  quantInput
    output_spec = quantOutput
    _quantCommand=quantCommand


def check_options(tkaNode, opts):
    #Define node for logan plot analysis 
    if opts.quant_k2 != None: tkaNode.inputs.k2=opts.quant_k2
    if opts.quant_thr != None: tkaNode.inputs.thr=opts.quant_thr
    if opts.quant_max != None: tkaNode.inputs.Max=opts.quant_max
    if opts.quant_filter != None: tkaNode.inputs.Filter=opts.quant_filter
    if opts.quant_end != None: tkaNode.inputs.end=opts.quant_end
    if opts.quant_v != None: tkaNode.inputs.v=opts.quant_v
    if opts.quant_start_time != None: tkaNode.inputs.start_time=opts.quant_start_time

    return tkaNode


