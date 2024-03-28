# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#######################################################################################

# If true, the surface LIC will be shown
sLIC = True

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
Fields = ['wallShearStressMean']
# Formula used to calculate CpY
Formula = 'mag(wallShearStressMean) / (0.5*1.225*40^2)'
# Number of elements in the colorbar
discretization = 256
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
# Domain mirroring
# create a new 'Reflect'
reflect1 = Reflect(registrationName='Reflect1', Input=extractBlock1)

# Properties modified on reflect1
reflect1.Plane = mirroringPlane

# hide data in view
Hide(extractBlock1, renderView1)


#######################################################################################
# Calculation of Cp
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
# Surface LIC
# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

if sLIC:
    # change representation type
    calculator1Display.SetRepresentationType('Surface LIC')

    # set scalar coloring
    ColorBy(calculator1Display, ('POINTS', 'wallShearStressMean', 'Magnitude'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(resultLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    calculator1Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    calculator1Display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'wallShearStressMean'
    wallShearStressMeanLUT = GetColorTransferFunction('wallShearStressMean')

    # get opacity transfer function/opacity map for 'wallShearStressMean'
    wallShearStressMeanPWF = GetOpacityTransferFunction('wallShearStressMean')

    # get 2D transfer function for 'wallShearStressMean'
    wallShearStressMeanTF2D = GetTransferFunction2D('wallShearStressMean')

    # set scalar coloring
    ColorBy(calculator1Display, ('POINTS', 'Result'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(wallShearStressMeanLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    calculator1Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    calculator1Display.SetScalarBarVisibility(renderView1, True)

    # Properties modified on calculator1Display
    calculator1Display.SelectInputVectors = ['POINTS', 'wallShearStressMean']

    # Properties modified on calculator1Display
    calculator1Display.ColorMode = 'Multiply'

    # Properties modified on calculator1Display
    calculator1Display.EnhanceContrast = 'Color Only'


#######################################################################################
# Colorbar setup
# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Rainbow Uniform', True)

# Properties modified on resultLUT
resultLUT.NumberOfTableValues = discretization

# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)

# Properties modified on resultLUTColorBar
resultLUTColorBar.Title = 'Mean skin friction coefficient             '
resultLUTColorBar.RangeLabelFormat = '%-#6.1f'

# Rescale transfer function
resultLUT.RescaleTransferFunction(0, 0.005)

# Rescale transfer function
resultPWF.RescaleTransferFunction(0, 0.005)

# Rescale 2D transfer function
resultTF2D.RescaleTransferFunction(0, 0.005, 0.0, 1.0)

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
SaveScreenshot(current_directory + '/../0_Figures/Cf/01_Top.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/01_Bottom.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/01_Left.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/01_Right.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/01_Front.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/01_Rear.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
# Surface LIC for 3D views
# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

if sLIC:
    # change representation type
    transform1Display.SetRepresentationType('Surface LIC')

    # set scalar coloring
    ColorBy(transform1Display, ('POINTS', 'wallShearStressMean', 'Magnitude'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(resultLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    transform1Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    transform1Display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'wallShearStressMean'
    wallShearStressMeanLUT = GetColorTransferFunction('wallShearStressMean')

    # get opacity transfer function/opacity map for 'wallShearStressMean'
    wallShearStressMeanPWF = GetOpacityTransferFunction('wallShearStressMean')

    # get 2D transfer function for 'wallShearStressMean'
    wallShearStressMeanTF2D = GetTransferFunction2D('wallShearStressMean')

    # set scalar coloring
    ColorBy(transform1Display, ('POINTS', 'Result'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(wallShearStressMeanLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    transform1Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    transform1Display.SetScalarBarVisibility(renderView1, True)

    # Properties modified on calculator1Display
    transform1Display.SelectInputVectors = ['POINTS', 'wallShearStressMean']

    # Properties modified on calculator1Display
    transform1Display.ColorMode = 'Multiply'

    # Properties modified on calculator1Display
    transform1Display.EnhanceContrast = 'Color Only'


#######################################################################################
# Colorbar
# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Rainbow Uniform', True)

# Properties modified on resultLUT
resultLUT.NumberOfTableValues = 35

# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)

# Properties modified on resultLUTColorBar
resultLUTColorBar.Title = 'Mean skin friction coefficient'
resultLUTColorBar.RangeLabelFormat = '%-#6.1f'

# Rescale transfer function
resultLUT.RescaleTransferFunction(0, 0.005)

# Rescale transfer function
resultPWF.RescaleTransferFunction(0, 0.005)

# Rescale 2D transfer function
resultTF2D.RescaleTransferFunction(0, 0.005, 0.0, 1.0)

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
SaveScreenshot(current_directory + '/../0_Figures/Cf/02_3D_1.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/02_3D_2.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/02_3D_3.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SaveScreenshot(current_directory + '/../0_Figures/Cf/02_3D_4.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')

exit(0)