# trace generated using paraview version 5.11.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#######################################################################################

# Image resolution
imageSize = [1920, 1080]                            # 1080p
imageSize = [2560, 1440]                            # 2K
imageSize = [3840, 2160]                            # 4K

# Name of the .foam file
Foam_name = 'results.foam'
# Group containing all the patches that make up the vehicle.
# It is defined in the snappyhexMesh
surface_group = 'group/vehicleGroup'
# Field that will be loaded
Fields = ['UMean', 'pMean']
# Formula used to calculate CpT
Formula = ' ( pMean + 0.5*mag(UMean)^2) / (0.5*40^2) '
# Threshold for the contour function
contourThreshold = 0
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

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0


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

# show data in view
reflect1Display = Show(reflect1, renderView1, 'UnstructuredGridRepresentation')


#######################################################################################
# Calculation of CpT
# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=resultsfoam)
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

# find source
resultsfoam = FindSource(Foam_name)

# update the view to ensure updated data information
renderView1.Update()


#######################################################################################
# Contour of the CpT
# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=calculator1)
contour1.ContourBy = ['POINTS', 'Result']
contour1.Isosurfaces = [3.0879120510003504]
contour1.PointMergeMethod = 'Uniform Binning'

# find source
resultsfoam = FindSource(Foam_name)

# Properties modified on contour1
contour1.Isosurfaces = [contourThreshold]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

# hide data in view
Hide(calculator1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# turn off scalar coloring
ColorBy(contour1Display, None)

# change solid color
contour1Display.AmbientColor = [1.0, 0.0, 0.0]
contour1Display.DiffuseColor = [1.0, 0.0, 0.0]


#######################################################################################
# Contour mirror
# create a new 'Reflect'
reflect2 = Reflect(registrationName='Reflect2', Input=contour1)

# Properties modified on reflect1
reflect2.Plane = mirroringPlane

# hide data in view
Hide(contour1, renderView1)

# show data in view
reflect2Display = Show(reflect2, renderView1, 'UnstructuredGridRepresentation')

# turn off scalar coloring
ColorBy(reflect2Display, None)

# change solid color
reflect2Display.AmbientColor = [1.0, 0.0, 0.0]
reflect2Display.DiffuseColor = [1.0, 0.0, 0.0]


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
SetActiveSource(reflect2)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/0_Top.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SetActiveSource(reflect2)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/0_Bottom.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SetActiveSource(reflect2)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/0_Left.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SetActiveSource(reflect2)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/0_Right.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SetActiveSource(reflect2)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/0_Front.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
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
SetActiveSource(reflect2)

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/0_Rear.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# Transform function to setup the 3D views (for the car)
# create a new 'Transform'
transform1 = Transform(registrationName='Transform1', Input=reflect1)
transform1.Transform = 'Transform'

# find source
reflect1 = FindSource('Reflect1')

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [0.0, 90.0, 90.0]

# hide data in view
Hide(reflect1, renderView1)

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


#######################################################################################
# Transform function to setup the 3D views (for the CpT)
# create a new 'Transform'
transform2 = Transform(registrationName='Transform2', Input=reflect2)
transform2.Transform = 'Transform'

# find source
reflect1 = FindSource('Reflect2')

# Properties modified on transform1.Transform
transform2.Transform.Rotate = [0.0, 90.0, 90.0]

# hide data in view
Hide(reflect1, renderView1)

# set active source
SetActiveSource(transform2)

# show data in view
transform2Display = Show(transform2, renderView1, 'UnstructuredGridRepresentation')

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=transform2.Transform)

#changing interaction mode based on data extents
renderView1.InteractionMode = '3D'

# update the view to ensure updated data information
renderView1.Update()

renderView1.ApplyIsometricView()

# reset view to fit data
renderView1.ResetCamera(True)

# turn off scalar coloring
ColorBy(transform2Display, None)

# change solid color
transform2Display.AmbientColor = [1.0, 0.0, 0.0]
transform2Display.DiffuseColor = [1.0, 0.0, 0.0]


#######################################################################################
# 3D view 1
# set active source
SetActiveSource(transform1)

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [0.0, 90.0, 90.0]

# set active source
SetActiveSource(transform2)

# Properties modified on transform2.Transform
transform2.Transform.Rotate = [0.0, 90.0, 90.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/3D_1.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# 3D view 2
# set active source
SetActiveSource(transform1)

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [180.0, 90.0, 90.0]

# set active source
SetActiveSource(transform2)

# Properties modified on transform2.Transform
transform2.Transform.Rotate = [180.0, 90.0, 90.0]

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/3D_2.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# 3D view 3
# set active source
SetActiveSource(transform1)

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [0.0, -90.0, 90.0]

# set active source
SetActiveSource(transform2)

# Properties modified on transform2.Transform
transform2.Transform.Rotate = [0.0, -90.0, 90.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/3D_3.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


#######################################################################################
# 3D view 4
# set active source
SetActiveSource(transform1)

# Properties modified on transform1.Transform
transform1.Transform.Rotate = [180.0, -90.0, 90.0]

# set active source
SetActiveSource(transform2)

# Properties modified on transform2.Transform
transform2.Transform.Rotate = [180.0, -90.0, 90.0]

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(True)

# save screenshot
SaveScreenshot(current_directory + '/../0_Figures/CpT_Contour/3D_4.jpeg', layout1, ImageResolution=[imageSize[0], imageSize[1]],
    OverrideColorPalette='WhiteBackground')


exit(0)