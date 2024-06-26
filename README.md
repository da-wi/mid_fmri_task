# Monetary incentive delay task 

![Overview](https://raw.githubusercontent.com/da-wi/mid_fmri_task/master/instruction/mid_fmri_task.png)

## Installation

Requirements
- Installation of python 2.7 or higher
- Installation of pygame
- Setting the paths correctly on your system

Here is a step by step tutorial on how to install pygame:
https://www.pygame.org/wiki/GettingStarted

## Quick start

After installation of the requirements, you should be able to launch the task via the commandline:

1. Change to the correct folder (e.g. "cd /this/is/the/correct/path")
2. Call the mid_task_v5.py3 script

```
python mid_task_v5.py3 SUBJECTID -s single -o -t 1
```

"SUBJECTID" is mandatory for the logfile
"-s single" enforces window mode - in the script this must be manually adjusted according to the local setup - right now this is adjusted for the MR centre in Zurich.
"-o" omits color in the symbols
"-t 1" sets the shape type balancing to balancing "1" (out of 6 possible balancings, see instructions)

3. Start the task by pressing "t"
4. Press the button "b" whenever you see the target (star symbol)

## Arguments

```
usage: mid_task_v5.py3 [-h] [-s SCREENMODE] [-bg BGCOLOR] [-r RUN] [-e] [-o] [-c COLORTYPE] [-t SHAPETYPE] [-S] [-l]
                       subjectid

Monetary incentive delay task

positional arguments:
  subjectid             mandatory subject id

options:
  -h, --help            show this help message and exit
  -s SCREENMODE, --screenmode SCREENMODE
                        dual or single screenmode [single,dual]
  -bg BGCOLOR, --bgcolor BGCOLOR
                        colortype 1 = black, colortype 2 = grey [1,2]
  -r RUN, --run RUN     determines the run number for the subject [1,2]
  -e, --emulation       Sets emulation mode for use outside the scanner
  -o, --omitcolor       Do not use any color
  -c COLORTYPE, --colortype COLORTYPE
                        colortype blue/orange (LOSS,GAIN,NEUTRAL) - 1=(Blu,Ora,Gray),2=(Ora,Blu,Gray),3=(Ora,Gray,Blu)
                        ,4=(Gray,Ora,Blu),5=(Gray,Blu,Ora),6=(Blu,Gray,Ora) [1-6]
  -t SHAPETYPE, --shapetype SHAPETYPE
                        determines the randomization of cues [1,2,3,4,5,6]
  -S, --shortversion    Starts a shortversion of the task
  -l, --forcelogdir     Force Logdir creation
```

## References

If you use this task, please cite one of the following publications:

- Willinger, D., Karipidis, I. I., Dimanova, P., Walitza, S., & Brem, S. (2021). Neurodevelopment of the incentive network facilitates motivated behaviour from adolescence to adulthood. _NeuroImage_, 237, 118186.

- Willinger, D., Karipidis, I. I., Neuer, S., Emery, S., Rauch, C., Häberling, I., ... & Brem, S. (2022). Maladaptive avoidance learning in the orbitofrontal cortex in adolescents with major depression. _Biological Psychiatry: Cognitive Neuroscience and Neuroimaging, 7_ (3), 293-301.

and  the original idea:

- Knutson, B., Westdorp, A., Kaiser, E., & Hommer, D. (2000). FMRI visualization of brain activity during a monetary incentive delay task. Neuroimage, 12(1), 20-27.