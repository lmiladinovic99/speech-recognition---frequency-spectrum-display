# Task description

Implement a tool that displays the frequency spectrum of a pre-recorded word. It is allowed to use a ready-made implementation of the DFT algorithm, as well as reading .wav headers.

# Entrance
The tool must provide the following items at the input:
- Using a raw .wav file as input sound. There is one word spoken on the recording, but it is possible that there is silence of arbitrary length before and after the word. This silence should be cut before processing begins. The system should report an error message if it considers that there are no spoken words in the recording.
- Choice of Triangle, Hamming, Hanning, Blackman, or any window function.
- DFT window width selection.

Provide at least five .wav files for testing, each a few seconds long:
- Speech signal - male voice.
- Speech signal - female voice.
- One tone on a musical instrument.
- Random noise (to check for an error message).
- Generated signal containing several selected harmonics (write a simple program to generate this signal).

# Exit
The tool must be able to display the frequency spectrum in two ways:
- Display the entire signal from the .wav file and the marked location of the beginning and end of the word.
- Display of the frequency spectrum for one window, where the spectrum is displayed as a histogram.
- Display of the frequency spectrum of the entire signal, where the spectrum is displayed as a sonogram.

The display of the location of the cut word should have time on the horizontal axis, and the values read from the .wav file on the vertical axis. It is necessary to show two vertical lines that represent the beginning and end of the found word. If no word is found in the input signal, show only the whole signal, without lines that would indicate the beginning and end of the word.

![alt text](https://github.com/lmiladinovic99/speech-recognition-frequency-spectrum-display/blob/main/1.PNG)

When displaying the frequency spectrum for a single window, the diagram has a frequency on the horizontal axis and a magnitude on the vertical axis. Display the frequency in Hz and the magnitude scaled to the range 0-100. It is necessary to provide zoom along the horizontal axis so that individual values can be seen at maximum zoom, and the entire diagram can be seen at minimum zoom.

![alt text](https://github.com/lmiladinovic99/speech-recognition-frequency-spectrum-display/blob/main/2.PNG)

The second diagram to be supported is used to show the entire frequency spectrum, with a time axis (sonogram). There is time on the horizontal axis, frequency on the vertical axis, and the intensity of the point on the diagram represents the magnitude. Both the horizontal and vertical axes must be numbered, with a fixed number of evenly spaced auxiliary horizontal lines (see example). Show two vertical lines that would mark the beginning and end of the found word as in the first diagram. If the word is not found, omit the lines. It is necessary to provide zoom functionality along the time axis to the extent that individual milliseconds can be seen at the highest zoom, and the entire signal can be seen at the lowest zoom.

![alt text](https://github.com/lmiladinovic99/speech-recognition-frequency-spectrum-display/blob/main/3.PNG)

