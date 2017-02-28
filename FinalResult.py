# 3D HUMAN BRAIN GENE VISUALIZATION 

# Importing the following libraries.

from vtk import *
# NUMPY - useful for large multi-dimensional arrays and mathematical functions
import numpy as np
# NIBABEL - useful for reading, writing and manipulating neuroimaging file formats
import nibabel as nib


# Reading the 3D Human Brain NIFTI image downloaded from Allen Human Brain Atlas website
image = nib.load("T2.nii") # extracted from T2.nii.gz of donor H0351.2001 - 'http://human.brain-map.org/mri_viewers/data'
image_array_data = image.get_data()
MRI_data = np.array (image_array_data,dtype=np.uint16)
print ("The MRI_data array :" , MRI_data)
print ('MRI_data size :' , MRI_data.size)
print ("Number of elements in MRI_data array :", len(MRI_data))
print ("Dimension of MRI_data array: ", MRI_data.shape)


# Random array values created for gene expression visualization which will later be manipulated with actual data
# Dummy array values set to 0 throughout with the same dimension as MRI data (185,180,192)
dummy = np.zeros ((185,180,192), dtype=np.uint16)
print ("dummy array (0s) size:" , dummy.size)

# Dummy array values set to 145 throughout with the same dimension as MRI data (185,180,192)
dummy_array = np.full((185,180,192), 145, dtype = np.uint16)
print ("The dummy array :" , dummy_array)
print ('dummy_array size :' , dummy_array.size)
print ("Number of elements in dummy_array :", len(dummy_array))
print ("Dimension of dummy_array: ", dummy_array.shape)


# Now that both arrays have same dimension and size we can combine both volumes using Numpy
Volume_of_arrays = MRI_data + dummy_array # or dummy
print ("Volume of both arrays combined: ", Volume_of_arrays)
print ("Whole volume size: ", Volume_of_arrays.size)
print ("Number of elements in the volume: ", len (Volume_of_arrays))
print ("Dimension of the whole volume: ", Volume_of_arrays.shape)

# Rendering the volume in an interactive renderer that rotates upon user interaction with mouse drag

# First, the combined array information that has both MRI and dummy gene data are imported for volume rendering through a function called 'VtkImageImport'
dataImporter = vtk.vtkImageImport()
data_string = Volume_of_arrays.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
dataImporter.SetNumberOfScalarComponents(1)

# Data extent has to be set when using VtkImageImport function
# Since both the volumes have same dimensions, one of them can be used to set the extents
w, d, h = MRI_data.shape
# Setting the limits from 0 to H,D,W values -1 (which are 0 to 184,179,191)
dataImporter.SetDataExtent(0, h-1, 0, d-1, 0, w-1)
dataImporter.SetWholeExtent(0, h-1, 0, d-1, 0, w-1)

# Setting the mapper function for the volume 
# VtkFixedPointVolumeRayCastMapper - it is a replacement for VolumeRayCastMapper due to VTK version 7
mapperVolume = vtk.vtkFixedPointVolumeRayCastMapper()
mapperVolume.SetBlendModeToMaximumIntensity()
mapperVolume.SetSampleDistance(0.1)
mapperVolume.SetAutoAdjustSampleDistances(0)

# Initializing the renderers VtkRenderer, VtkRenderWindow, and VtkRenderWindowInteractor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()

# Setting connections between the mapper and input array data
mapperVolume.SetInputConnection(dataImporter.GetOutputPort())

# Initializing VtkVolume object 
vol = vtk.vtkVolume()
vol.SetMapper(mapperVolume)
ren.AddViewProp(vol)

# Calling the rendering functions 
renWin.AddRenderer(ren)
iren.SetRenderWindow(renWin)

# Now, set the color transfer functions for both MRI volume and dummy Gene expression volume 
# Set a criteria to color the volume based on the values in every voxel 
# The values less than 256 in the array will be set to greyscale
# The values more than 256 in the array will be set to colors


# For values less than 256 in the combined array (MRI + GeneExpression)
for x in np.nditer (Volume_of_arrays < 256 , flags =['external_loop'], order ='C'):
	print ("Printing the number of elements in the combined array (<256) :", len(x)) # This is to make sure the nditer command is reading all the elements in the array
	
	# Transfer function, MRI
	# Setting RGBA values 
  
	ctfun1 = vtk.vtkColorTransferFunction()
	ctfun1.AddRGBPoint(0, 0, 0, 0)
	ctfun1.AddRGBPoint(50, 1.5, 1.5, 0)	

	volumeScalarOpacity1 = vtk.vtkPiecewiseFunction()
	volumeScalarOpacity1.AddPoint(0, 40)

	volumeGradientOpacity1 = vtk.vtkPiecewiseFunction()
	volumeGradientOpacity1.AddPoint(250, 1.0)

	propVolume = vtk.vtkVolumeProperty()
	propVolume.SetColor(ctfun1)
	propVolume.SetScalarOpacity(0, volumeScalarOpacity1)
	propVolume.SetGradientOpacity(0, volumeGradientOpacity1)
	propVolume.SetInterpolationTypeToLinear()


for x in np.nditer (Volume_of_arrays > 256, flags =['external_loop'], order ='C'):
	print ("Printing the number of elements in the combined array (>256):", len(x)) # This is to make sure the nditer command is reading all the elements in the array
	
	# Transfer functions, Gene
	# Setting RGBA values 
  
	tfun2= vtk.vtkPiecewiseFunction()
	tfun2.AddPoint(70.0, 0.0)
	tfun2.AddPoint(250.0, 0)
	tfun2.AddPoint(4195.0, 40)

	ctfun2 = vtk.vtkColorTransferFunction()
	ctfun2.AddRGBPoint(400, 1, 0, 0.3)

	volumeScalarOpacity2 = vtk.vtkPiecewiseFunction()
	volumeScalarOpacity2.AddPoint(100, 1.5)

	volumeGradientOpacity2 = vtk.vtkPiecewiseFunction()
	volumeGradientOpacity2.AddPoint(300, 1.0)

	# Volume property setting
	propVolume = vtk.vtkVolumeProperty()
	propVolume.SetColor(ctfun2)
	propVolume.SetScalarOpacity(tfun2)
	propVolume.SetScalarOpacity(1, volumeScalarOpacity2)
	propVolume.SetGradientOpacity(1, volumeGradientOpacity2)
	propVolume.ShadeOn()
	propVolume.SetAmbient(1.0)
	propVolume.SetDiffuse(0.7)
	propVolume.SetSpecular(0.5)
	propVolume.SetInterpolationTypeToLinear()

# Calling the volume property 
vol.SetProperty(propVolume)
print ("Rendering the Volume in 3D interactive window")

# Adding the actor
ren.AddActor(vol)
ren.AddVolume(vol)

# Setting a background for the interactive renderer and size 
ren.SetBackground(0,0,0)
renWin.SetSize(700, 700)

# When interaction starts, the requested frame rate is increased.
def StartInteraction(obj, event):
    global renWin
    renWin.SetDesiredUpdateRate(10)
  
# When interaction ends, the requested frame rate is decreased to
# normal levels. This causes a full resolution render to occur.
def EndInteraction(obj, event):
    global renWin
    renWin.SetDesiredUpdateRate(0.001)
  
# The implicit function vtkPlanes is used in conjunction with the
# volume ray cast mapper to limit which portion of the volume is rendered
planes = vtk.vtkPlanes()
def ClipVolumeRender(obj, event):
    global planes, mapperVolume
    obj.GetPlanes(planes)
    mapperVolume.SetClippingPlanes(planes)

# Start the 3D interactive renderer to show a humn brain
iren.Initialize()
renWin.Render()
iren.Start()
