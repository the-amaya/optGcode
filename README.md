# optGcode

<p align="center">
	<img alt="GitHub language count" src="https://img.shields.io/github/languages/count/the-amaya/optGcode?style=plastic">
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/the-amaya/optGcode?style=plastic">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/the-amaya/optGcode?style=plastic">
	<img alt="GitHub" src="https://img.shields.io/github/license/the-amaya/optGcode?style=plastic">
	<img alt="GitHub contributors" src="https://img.shields.io/github/contributors/the-amaya/optGcode?style=plastic">
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/the-amaya/optGcode?style=plastic">
	<img alt="Scrutinizer code quality (GitHub/Bitbucket)" src="https://img.shields.io/scrutinizer/quality/g/the-amaya/optGcode?style=plastic">
</p>


## new features!

### laser etching!

using CAM files and a bit of manual prep we can generate a gcode file to run a laser to etch the component side of the board.

![nested silkscreen](https://raw.githubusercontent.com/the-amaya/optGcode/main/demo/silkscreen.png)

### nesting!

You can now use this to nest g-code (non-rotationally) to fill out a PCB

input g-code with outlines at a random spot X,Y

![raw layout](https://raw.githubusercontent.com/the-amaya/optGcode/main/demo/nest0.png)

we then move the g-code to 0,0

![clean layout](https://raw.githubusercontent.com/the-amaya/optGcode/main/demo/nest1.png)

then we nest it as many times as possible

![nested layout](https://raw.githubusercontent.com/the-amaya/optGcode/main/demo/nest2.png)


## features
take gcode and do a poor job trying to optimize it

The gcode that we start with looks something like this

![start](https://raw.githubusercontent.com/the-amaya/optGcode/main/demo/start.png)

After running this crappy code it looks something like this

![finish](https://raw.githubusercontent.com/the-amaya/optGcode/main/demo/finish.png)



# usage instructions as of dec 8th
in eagle

	run ULP 'pcb-gcode-setup' to get bottom etch and drill files
	file > 'generate CAM data' (cam data is used in flamcam in next step)

in flatcam

	'open_gerber <top-silkscreen-file.cam> -follow 1 -outname GTO_follow'
	'follow GTO_follow -outname silk_geo'
	'cncjob silk_geo'
	'write_gcode silk_geo_cnc silk.gcode'

in notepad

	edit silk.gcode from flatcam
	remove headers/footers
	find and replace (include trailing/leading spaces as indicated):
	
		'Y' -> ' Y'
		'\n' -> '\nN0 '
		'G01 Z-0.0020' -> 'M03'
		'G00 Z0.1000' -> 'M05'

in gcodestuff

	run and select the 3 files we created above