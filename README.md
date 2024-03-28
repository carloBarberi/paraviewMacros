# paraviewMacros

# Description
The repository relies on `server_allScript.py` and `server_singleScript.py` within the 0_Script folder. These two scripts allow all, or part of the macros, to be launched in order to automate as much as possible the post-processing in paraView.


# Known issues
- In some cases the photos are not centered. This happens only with in 3D views


# Disclaimers
- Scripts and macros have been tested on Windows machines only
- Scripts and macros have been tested with simpleFoam solver only
- **The two folders must be placed in a specific location inside the simulation output folder (in particular, inside the postProcessing folder)**
- To do a quick comparison between photos of different simulations that have been saved with these macros, it is possible to use another script called [CFDfigureViewer](https://github.com/carloBarberi/CFDfigureViewer)


# Installation
In order to use the scripts, it is necessary to download this repository and copy the two folders (0_Figures and 0_Script) inside the postProcessing folder of the simulation.

All figures will be saved within 0_Figures in the corresponding folders, while 0_Script contains scripts and macros. Specifically, all macros are located within `0_Script/Macros`.


# Before Usage
1. Change the `paraView.exe` directory inside `server_allScript.py` and `server_singleScript.py` located inside 0_Script. 

    `pvbatch.exe` is located in the same directory of `paraView.exe`. It is very convenient for running macros because paraView is launched from the terminal and is not shown on the screen. This makes the process of saving images much faster. I recommend using paraView with graphical UI when you need to debug macros, in case there are any problems.

2. At the beginning of each macro there is a section where you can change the main parameters, such as: name of the .foam file, formula used, position of the slices to be saved,... . Each parameter is commented for user's convenience. These parameters must be changed according to your simulation. In addition, each macro is divided into subsections, also commented, so that it is easier to find any problems.


# How it works
1. Copy the 0_Figures and 0_Script folders to the postProcessing folder of the simulation
2. The macros are run from the two scripts in 0_Scripts:
    - `server_allScript.py` runs all the macros inside the Macros folder
    - `server_singleScript.py` asks the user which macro to run

    Both have prompts to guide the user.


# Description of the macros
A description of the different macros in the repository follows:
- `Cp.py`: pressure coefficient on the surface of the body. Surface LIC can be turned on or off.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\1.jpeg" width="384" height="216">
    </div>
- `CpT_Contour.py`: volume in which the total pressure coefficient is null
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\2.jpeg" width="384" height="216">
    </div>
- `CpT_X.py`: total pressure coefficient, slices along X
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\3.jpeg" width="384" height="216">
    </div>
- `CpT_Y.py`: total pressure coefficient, slices along Y
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\4.jpeg" width="384" height="216">
    </div>
- `CpT_Z.py`: total pressure coefficient, slices along Z
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\5.jpeg" width="384" height="216">
- `CpX.py`: red areas are related to drag, while blue areas are related to thrust.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\6.jpeg" width="384" height="216">
    </div>
- `CpY.py`: red areas are related to a force to positive y, while blue areas are related to a force to negative y.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\7.jpeg" width="384" height="216">
    </div>
- `CpZ.py`: red areas are related to lift, while blue areas are related to downforce.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\8.jpeg" width="384" height="216">
    </div>
- `Unorm_X.py`: normalized flow velocity, slices along X. Surface LIC can be turned on or off.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\9.jpeg" width="384" height="216">
    </div>
- `Unorm_Y.py`: normalized flow velocity, slices along Y. Surface LIC can be turned on or off.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\10.jpeg" width="384" height="216">
    </div>
- `Unorm_Z.py`: normalized flow velocity, slices along Z. Surface LIC can be turned on or off.
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\11.jpeg" width="384" height="216">
    </div>
- `Vehicle.py`: it shows only the geometry of the body
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\12.jpeg" width="384" height="216">
    </div>
- `Cf.py`: skin friction coefficient
    <div style="text-align: left;">
        <img src="0_Figures\ZZ_sampleImages\13.jpeg" width="384" height="216">
    </div>