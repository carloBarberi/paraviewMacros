# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#######################################################################################

# Image resolution
imageSize = [1920, 1080]                            # 1080p
imageSize = [2560, 1440]                            # 2K
# imageSize = [3840, 2160]                            # 4K

# Value that will change the text and colorbar size based on the image resolution
coeff = 1
if imageSize[1] == 1440:
    coeff = 1
if imageSize[1] == 2160:
    coeff = 2

# Name of the .foam file
Foam_name = 'results.foam'
# Group containing all the patches that make up the vehicle.
# It is defined in the snappyhexMesh
surface_group = 'group/vehicleGroup'
# Field that will be loaded
Fields = ['UMean', 'pMean']
# Formula used to calculate CpZ
Formula = 'pMean * (Normals_Z) / (0.5*40^2)'
# Number of elements in the colorbar
discretization = 31
# Mirror plane, useful in half-vehicle simulations
mirroringPlane = 'Y Min'

#######################################################################################


#### import the simple module from the paraview
from paraview.simple import *
import os

# Get current directory
current_directory = os.getcwd()

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
resultsfoam = OpenFOAMReader(registrationName=Foam_name, FileName=os.path.join(current_directory, '..\..', Foam_name))
resultsfoam.MeshRegions = [surface_group, 'internalMesh']
resultsfoam.CellArrays = Fields

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on resultsfoam
resultsfoam.CaseType = 'Reconstructed Case'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
resultsfoamDisplay = Show(resultsfoam, renderView1, 'GeometryRepresentation')


#######################################################################################
# Extracting the block to isolate the car
# find source
resultsfoam = FindSource(Foam_name)

# create a new 'Extract Block'
extractBlock1 = ExtractBlock(registrationName='ExtractBlock1', Input=resultsfoam)

# Properties modified on extractBlock1
extractBlock1.Selectors = ['/Root/boundary']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
extractBlock1Display = Show(extractBlock1, renderView1, 'GeometryRepresentation')

# hide data in view
Hide(resultsfoam, renderView1)

# update the view to ensure updated data information
renderView1.Update()


#######################################################################################
# Calculation of the surface normals
# find source
extractBlock1 = FindSource('ExtractBlock1')

# create a new 'Generate Surface Normals'
generateSurfaceNormals1 = GenerateSurfaceNormals(registrationName='GenerateSurfaceNormals1', Input=extractBlock1)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
generateSurfaceNormals1Display = Show(generateSurfaceNormals1, renderView1, 'GeometryRepresentation')

# hide data in view
Hide(extractBlock1, renderView1)

# update the view to ensure updated data information
renderView1.Update()


#######################################################################################
# Domain mirroring
# create a new 'Reflect'
reflect1 = Reflect(registrationName='Reflect1', Input=generateSurfaceNormals1)

# Properties modified on reflect1
reflect1.Plane = mirroringPlane

# hide data in view
Hide(generateSurfaceNormals1, renderView1)


#######################################################################################
# Calculation of CpZ
# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=reflect1)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.Function = Formula

# show data in view
calculator1Display = Show(calculator1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = ['POINTS', 'Result']
calculator1Display.LookupTable = resultLUT
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'None'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleArray = 'Result'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'UMean'
calculator1Display.ScaleFactor = 0.4613143026828766
calculator1Display.SelectScaleArray = 'Result'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'Result'
calculator1Display.GaussianRadius = 0.02306571513414383
calculator1Display.SetScaleArray = ['POINTS', 'Result']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'Result']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.SelectInputVectors = ['POINTS', 'UMean']
calculator1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [-4.920267333984375, 0.0, 0.5, 0.0, 1.0846156311035156, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [-4.920267333984375, 0.0, 0.5, 0.0, 1.0846156311035156, 1.0, 0.5, 0.0]

# hide data in view
Hide(reflect1, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()


#######################################################################################
# Colorbar
# Properties modified on resultLUT
resultLUT.NumberOfTableValues = discretization

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Cool to Warm (Extended)', True)

# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)

# Properties modified on resultLUTColorBar
resultLUTColorBar.Title = 'CpZ mean                        '
resultLUTColorBar.RangeLabelFormat = '%-#6.1f'

# Rescale transfer function
resultLUT.RescaleTransferFunction(-1, 1)

# Rescale transfer function
resultPWF.RescaleTransferFunction(-1, 1)

# Rescale 2D transfer function
resultTF2D.RescaleTransferFunction(-1, 1, 0.0, 1.0)

# Properties modified on resultLUT
resultLUT.RGBPoints = [-1.0, 0.0, 0.0, 0.34902, -0.9375, 0.039216, 0.062745, 0.380392, -0.875, 0.062745, 0.117647, 0.411765, -0.8125, 0.090196, 0.184314, 0.45098, -0.75, 0.12549, 0.262745, 0.501961, -0.6875, 0.160784, 0.337255, 0.541176, -0.625, 0.2, 0.396078, 0.568627, -0.5625, 0.239216, 0.454902, 0.6, -0.5, 0.286275, 0.521569, 0.65098, -0.4374999999999999, 0.337255, 0.592157, 0.701961, -0.375, 0.388235, 0.654902, 0.74902, -0.3125000000000001, 0.466667, 0.737255, 0.819608, -0.25, 0.572549, 0.819608, 0.878431, -0.1874999999999999, 0.654902, 0.866667, 0.909804, -0.125, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.12500000000000022, 1.0, 1.0, 1.0, 0.1875, 0.94902, 0.733333, 0.588235, 0.25, 0.929412, 0.65098, 0.509804, 0.3125, 0.909804, 0.564706, 0.435294, 0.3749999999999998, 0.878431, 0.458824, 0.352941, 0.4375, 0.839216, 0.388235, 0.286275, 0.5, 0.760784, 0.294118, 0.211765, 0.5625, 0.701961, 0.211765, 0.168627, 0.6250000000000002, 0.65098, 0.156863, 0.129412, 0.6875, 0.6, 0.094118, 0.094118, 0.75, 0.54902, 0.066667, 0.098039, 0.8125, 0.501961, 0.05098, 0.12549, 0.8749999999999998, 0.45098, 0.054902, 0.172549, 0.9375, 0.4, 0.054902, 0.192157, 1.0, 0.34902, 0.070588, 0.211765]

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# get the material library
materialLibrary1 = GetMaterialLibrary()

# change scalar bar placement
resultLUTColorBar.Orientation = 'Horizontal'
resultLUTColorBar.WindowLocation = 'Lower Right Corner'
resultLUTColorBar.TitleJustification = 'Right'
resultLUTColorBar.TitleFontSize = 20*coeff
resultLUTColorBar.LabelFontSize = 15*coeff
resultLUTColorBar.ScalarBarThickness = 15*coeff
resultLUTColorBar.ScalarBarLength = 0.4


#######################################################################################
# Top picture
#change interaction mode for render view
renderView1.InteractionMode = '2D'

renderView1.ResetActiveCameraToNegativeZ()

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# get layout
layout1 = GetLayout()

#Enter preview mode
layout1.PreviewMode = [imageSize[0], imageSize[1]]

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(calculator1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/07_Top.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Bottom picture
renderView1.ResetActiveCameraToNegativeZ()

# reset view to fit data
renderView1.ResetCamera(False)

renderView1.ResetActiveCameraToPositiveZ()

# reset view to fit data
renderView1.ResetCamera(False)

renderView1.AdjustRoll(-90.0)

renderView1.AdjustRoll(-90.0)

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(calculator1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/07_Bottom.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Left picture
renderView1.ResetActiveCameraToPositiveY()

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(calculator1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/07_Left.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Right picture
renderView1.ResetActiveCameraToNegativeY()

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(calculator1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/07_Right.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Front picture
renderView1.ResetActiveCameraToPositiveX()

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(calculator1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/07_Front.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Rear picture
renderView1.ResetActiveCameraToNegativeX()

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data bounds
renderView1.ResetCamera(-0.8083210587501526, 3.8048219680786133, -1.0141137838363647, 0.0, 0.0, 1.4164721965789795, True)

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(calculator1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/07_Rear.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Transform function to setup the 3D views
# create a new 'Transform'
transform1 = Transform(registrationName='Transform1', Input=calculator1)
transform1.Transform = 'Transform'

# find source
reflect1 = FindSource('Reflect1')

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [0.0, 90.0, 90.0]

# hide data in view
Hide(calculator1, renderView1)

# get active source.
transform1 = GetActiveSource()

# set active source
SetActiveSource(transform1)

# show data in view
transform1Display = Show(transform1, renderView1, 'UnstructuredGridRepresentation')

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=transform1.Transform)

#changing interaction mode based on data extents
renderView1.InteractionMode = '3D'

# update the view to ensure updated data information
renderView1.Update()

renderView1.ApplyIsometricView()

# reset view to fit data
renderView1.ResetCamera(True)

# show color bar/color legend
transform1Display.SetScalarBarVisibility(renderView1, True)


#######################################################################################
# Colorbar
# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Cool to Warm (Extended)', True)

# Properties modified on resultLUT
resultLUT.Discretize = discretization

# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)

# Properties modified on resultLUTColorBar
resultLUTColorBar.Title = 'CpZ mean'
resultLUTColorBar.RangeLabelFormat = '%-#6.1f'

# Rescale transfer function
resultLUT.RescaleTransferFunction(-1, 1)

# Rescale transfer function
resultPWF.RescaleTransferFunction(-1, 1)

# Rescale 2D transfer function
resultTF2D.RescaleTransferFunction(-1, 1, 0.0, 1.0)

# Properties modified on resultLUT
resultLUT.RGBPoints = [-1.0, 0.0, 0.0, 0.34902, -0.9375, 0.039216, 0.062745, 0.380392, -0.875, 0.062745, 0.117647, 0.411765, -0.8125, 0.090196, 0.184314, 0.45098, -0.75, 0.12549, 0.262745, 0.501961, -0.6875, 0.160784, 0.337255, 0.541176, -0.625, 0.2, 0.396078, 0.568627, -0.5625, 0.239216, 0.454902, 0.6, -0.5, 0.286275, 0.521569, 0.65098, -0.4374999999999999, 0.337255, 0.592157, 0.701961, -0.375, 0.388235, 0.654902, 0.74902, -0.3125000000000001, 0.466667, 0.737255, 0.819608, -0.25, 0.572549, 0.819608, 0.878431, -0.1874999999999999, 0.654902, 0.866667, 0.909804, -0.125, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.12500000000000022, 1.0, 1.0, 1.0, 0.1875, 0.94902, 0.733333, 0.588235, 0.25, 0.929412, 0.65098, 0.509804, 0.3125, 0.909804, 0.564706, 0.435294, 0.3749999999999998, 0.878431, 0.458824, 0.352941, 0.4375, 0.839216, 0.388235, 0.286275, 0.5, 0.760784, 0.294118, 0.211765, 0.5625, 0.701961, 0.211765, 0.168627, 0.6250000000000002, 0.65098, 0.156863, 0.129412, 0.6875, 0.6, 0.094118, 0.094118, 0.75, 0.54902, 0.066667, 0.098039, 0.8125, 0.501961, 0.05098, 0.12549, 0.8749999999999998, 0.45098, 0.054902, 0.172549, 0.9375, 0.4, 0.054902, 0.192157, 1.0, 0.34902, 0.070588, 0.211765]

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# get the material library
materialLibrary1 = GetMaterialLibrary()

# change scalar bar placement
resultLUTColorBar.Orientation = 'Horizontal'
resultLUTColorBar.WindowLocation = 'Lower Right Corner'
resultLUTColorBar.TitleJustification = 'Centered'
resultLUTColorBar.TitleFontSize = 20*coeff
resultLUTColorBar.LabelFontSize = 15*coeff
resultLUTColorBar.ScalarBarThickness = 15*coeff
resultLUTColorBar.ScalarBarLength = 0.4


#######################################################################################
# 3D view 1
# get active source.
transform1 = GetActiveSource()

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [0.0, 90.0, 90.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/08_3D_1.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# 3D view 2
# get active source.
transform1 = GetActiveSource()

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [180.0, 90.0, 90.0]

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/08_3D_2.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# 3D view 3
# get active source.
transform1 = GetActiveSource()

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [0.0, -90.0, 90.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/08_3D_3.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# 3D view 4
# get active source.
transform1 = GetActiveSource()

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [180.0, -90.0, 90.0]

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Cp/08_3D_4.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')

exit(0)