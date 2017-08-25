# Pianopad
Pianopad is a python solution to enable the usage of Launchpad controllers as keyboards. Keyboard as in music, not as in typing. Well, _keyboards as in type as well_, but mainly as in music. :P

Right now this is far from its final state and usage is recomended only for developers or curious people, end-user usage is not recommended due to bugs and poor usability.

## Main usage
Right now (and maybe forever) pianopad won't create a custom midi device for you, so you need to create one. The suggested way is to download [loopMIDI](http://www.tobias-erichsen.de/software/loopmidi.html) that at the same time works great and simple to use.
That done, create a custom midi device as in the picture below:

_(just click the + button and rename as you desire)_
That done, it is time to setup pianopad. Run main.py in a terminal session, ou might see a list of input and output devices listed. There is a file named **devices.txt** at the root directory where you should put the devices name as follows:
- input: the launchpad input device that has been listed
- launchpad output: the launchpad output device that has been listed
- piano output: the output device that has been listed with the same name of the device you have created at loopMIDI

Example:
```
input: Launchpad MK2 6
launchpad output: Launchpad MK2 8
piano output: pianopad 3
```
After that, you can run the main.py again and it will hopefully run.
In you daw, set the loopMIDI device as yor input device, and things should work:

## Dependencies
Only [mido](https://github.com/olemb/mido/) so far:
```
pip install mido
```

# Contributing
There are some issues created in the tracker about some of the things we may want to have in there. We have 12 function buttons in launchpad, so we gotta fill them all. :D
Aside from that, all help is welcome, including:
- Documentation
-- Code Documentation and User Guides
- UI design
- Testing in different OSs and with different hardware (I only have access to one Launchpad MK2, I don't have the Pro, MK1 and mini)
