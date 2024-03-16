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
#imageSize = [3840, 2160]                            # 4K

# Value that will change the text and colorbar size based on the image resolution
coeff = 1
if imageSize[1] == 1440:
    coeff = 1
if imageSize[1] == 2160:
    coeff = 2

# Name of the .foam file
Foam_name = 'results.foam'
# Field that will be loaded
Fields = ['UMean', 'pMean']
# Formula used to calculate Unorm
Formula = 'UMean / 40'
# Number of elements in the colorbar
discretization = 256
# Mirror plane, useful in half-vehicle simulations
mirroringPlane = 'Y Min'
# Clip box size to reduce domain size
boxPosition = [-1.5, -1.5, 0.0]
boxLength = [7.0, 3.0, 2.0]
# First slice that will be saved and list of all other slices
firstSlice = 10
zz_slices = list(range(25, 1801, 25))

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
resultsfoam.MeshRegions = ['internalMesh']
resultsfoam.CellArrays = Fields

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on resultsfoam
resultsfoam.CaseType = 'Reconstructed Case'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# show data in view
resultsfoamDisplay = Show(resultsfoam, renderView1, 'UnstructuredGridRepresentation')


#######################################################################################
# Domain mirroring
# create a new 'Reflect'
reflect1 = Reflect(registrationName='Reflect1', Input=resultsfoam)

# Properties modified on reflect1
reflect1.Plane = mirroringPlane

# hide data in view
Hide(resultsfoam, renderView1)


#######################################################################################
# Create the box to have a smaller domain
# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=reflect1)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['POINTS', 'pMean']
clip1.Value = -1336.6304321289062

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [7.75, -3.5, 3.5]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [7.75, -3.5, 3.5]

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1.ClipType)

# Properties modified on clip1
clip1.ClipType = 'Box'

# Properties modified on clip1.ClipType
clip1.ClipType.Position = boxPosition
clip1.ClipType.Length = boxLength

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# hide data in view
Hide(reflect1, renderView1)


#######################################################################################
# Calculation of Unorm
# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=clip1)
calculator1.Function = ''

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on calculator1
calculator1.Function = Formula

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('pMean')

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('pMean')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = ['POINTS', 'pMean']
calculator1Display.LookupTable = pLUT
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'None'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleArray = 'pMean'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'Result'
calculator1Display.ScaleFactor = 0.7000000000000001
calculator1Display.SelectScaleArray = 'pMean'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'pMean'
calculator1Display.GaussianRadius = 0.035
calculator1Display.SetScaleArray = ['POINTS', 'pMean']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'pMean']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityFunction = pPWF
calculator1Display.ScalarOpacityUnitDistance = 0.058548045984597445
calculator1Display.OpacityArrayName = ['POINTS', 'pMean']
calculator1Display.SelectInputVectors = ['POINTS', 'Result']
calculator1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [-3482.765869140625, 0.0, 0.5, 0.0, 809.5050048828125, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [-3482.765869140625, 0.0, 0.5, 0.0, 809.5050048828125, 1.0, 0.5, 0.0]

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# find source
resultsfoam = FindSource(Foam_name)

# update the view to ensure updated data information
renderView1.Update()


#######################################################################################
# First slice
# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=calculator1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [1.0, -1.25, 1.25]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [1.0, -1.25, 1.25]

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [-2.0, 0.0, firstSlice/1000]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'pMean']
slice1Display.LookupTable = pLUT
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'pMean'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'Result'
slice1Display.ScaleFactor = 0.25
slice1Display.SelectScaleArray = 'pMean'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'pMean'
slice1Display.GaussianRadius = 0.0125
slice1Display.SetScaleArray = ['POINTS', 'pMean']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'pMean']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.SelectInputVectors = ['POINTS', 'Result']
slice1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [4.859202861785889, 0.0, 0.5, 0.0, 165.7403106689453, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [4.859202861785889, 0.0, 0.5, 0.0, 165.7403106689453, 1.0, 0.5, 0.0]

# hide data in view
Hide(calculator1, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()


#######################################################################################
# SurfaceLIC setup
# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'Result', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

if sLIC == True:
    # change representation type
    slice1Display.SetRepresentationType('Surface LIC')

    # Properties modified on slice1Display
    slice1Display.ColorMode = 'Multiply'

    # Properties modified on slice1Display
    slice1Display.EnhanceContrast = 'Color Only'


#######################################################################################
# Colorbar setup
# Rescale transfer function
resultLUT.RescaleTransferFunction(0.0, 1.2)

# Rescale transfer function
resultPWF.RescaleTransferFunction(0.0, 1.2)

# Rescale 2D transfer function
resultTF2D.RescaleTransferFunction(0.0, 1.2, 0.0, 1.0)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Rainbow Uniform', True)

# Properties modified on resultLUT
resultLUT.NumberOfTableValues = discretization

# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)

# Properties modified on resultLUTColorBar
resultLUTColorBar.Title = 'Mean normalized velocity'
resultLUTColorBar.ComponentTitle = ''
resultLUTColorBar.RangeLabelFormat = '%-#6.1f'

renderView1.ResetActiveCameraToPositiveX()

# reset view to fit data
renderView1.ResetCamera(False)

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# get the material library
materialLibrary1 = GetMaterialLibrary()

# reset view to fit data bounds
renderView1.ResetCamera(-2.5, 4.5, 0.0, 0.0, -1.862639926672926e-18, 2.5, True)

# Properties modified on resultLUTColorBar
resultLUTColorBar.AutoOrient = 0
resultLUTColorBar.Orientation = 'Horizontal'
resultLUTColorBar.WindowLocation = 'Lower Center'
resultLUTColorBar.TitleFontSize = 20*coeff
resultLUTColorBar.LabelFontSize = 20*coeff
resultLUTColorBar.ScalarBarThickness = 20*coeff
resultLUTColorBar.ScalarBarLength = 0.4
resultLUTColorBar.UseCustomLabels = 1
resultLUTColorBar.CustomLabels = [round(x / 10, 1) for x in range(int(1.2 * 10), int(0 * 10), int(-0.2 * 10))]


#######################################################################################
# Set the camera perpendicular to Z
# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

renderView1.ResetActiveCameraToNegativeZ()

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data bounds
renderView1.ResetCamera(-1.5, 6.5, -2.5, 0.0, 1.0, 1.0, True)


#######################################################################################
# Definizione del testo da inserire
# create a new 'Text'
text1 = Text(registrationName='Text1')

# Properties modified on text1
text1.Text = 'Z = '+str(firstSlice)+'mm'

# show data in view
text1Display = Show(text1, renderView1, 'TextSourceRepresentation')

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on text1Display
text1Display.FontSize = 45*coeff

# get layout
layout1 = GetLayout()


#######################################################################################
# Definizione della grandezza della foto
#Enter preview mode
layout1.PreviewMode = [imageSize[0], imageSize[1]]

# layout/tab size in pixels
layout1.SetSize(imageSize[0], imageSize[1])

# set active source
SetActiveSource(slice1)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/Unorm_Z_slices/Z_'+str(firstSlice)+'.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Loop to automatically save the slices
ii = 1

for zz in zz_slices:
    # set active source
    SetActiveSource(slice1)

    # Properties modified on slice1.SliceType
    slice1.SliceType.Origin = [1.5, 1.5, zz/1000]

    # update the view to ensure updated data information
    renderView1.Update()

    # set active source
    SetActiveSource(text1)

    # toggle interactive widget visibility (only when running from the GUI)
    ShowInteractiveWidgets(proxy=text1Display)

    # toggle interactive widget visibility (only when running from the GUI)
    HideInteractiveWidgets(proxy=text1Display)

    # Properties modified on text1
    text1.Text = 'Z = '+str(zz)+'mm'

    # update the view to ensure updated data information
    renderView1.Update()

    # layout/tab size in pixels
    layout1.SetSize(imageSize[0], imageSize[1])

    # set active source
    SetActiveSource(slice1)

    # reset view to fit data
    renderView1.ResetCamera(True)

    # save screenshot
    SaveScreenshot(current_directory + '/../0_Figures/Unorm_Z_slices/Z_'+str(zz)+'.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')
    
    ii = ii + 1
    

exit(0)