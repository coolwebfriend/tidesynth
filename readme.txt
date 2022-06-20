TideSynth v0.1
A Python script for prediction and sonification of tidal data. 

BACKGROUND

Tidal data can be visualized as a complex waveform, much like an audio signal. 
If you run historical water height measurements through a Fourier transform 
function, you can visualize the frequencies and amplitudes of each harmonic 
which constitutes the original wave. 

Each harmonic represents the influence of a real-world phenomenon on the tide,
like the positions of the sun and moon in the sky relative to your position on 
the rotating Earth. There are actually more than 400 tidal harmonic constituents, 
but reasonably accurate predictions can be achieved using just 37. 

This Python script is based on Tide Predicting Machine No. 2, aka “Old Brass Brains,” 
an analog computer constructed by Rollin A. Harris and E.G. Fisher in 1910. 
This machine was used by the US National Geodetic Survey (then called the US 
Coast and Geodetic Survey) for official tide predictions for over fifty years. 
Using mechanical principles, it modeled the frequencies, amplitudes, and phases 
of known tidal harmonics. Think of it like a Fourier transform in reverse— it 
summed the known harmonics to reconstitute the complex waveform. 


How To Use

1. ACQUIRE TIDAL DATA

The National Oceanic and Atmosphere Administration (NOAA) publishes snapshots of 
tidal harmonic data here: https://tidesandcurrents.noaa.gov/harcon.html?&id=9410660 
The seven-digit code at the end of the URL represents a NOAA station code. In this 
case, 9410660 represents the Los Angeles station. You can search for another station
at the URL provided. If that doesn’t work look for a station at 
https://tidesandcurrents.noaa.gov and replace 9410660 with your chosen station code.
Copy/paste the full contents of the harmonic constituent table into Numbers or Excel,
and export the data as a CSV suing the same column order and headers as the example 
CSV provided. 


2. RUN THE SCRIPT

TideSynth is designed to be run from Terminal. Type Python3 followed by the local 
file path of TideSynth.py. You will be prompted to enter four pieces of information:

  Input File Path: the file path of the CSV you created in step 2.
  
  Fundamental frequency in Hertz. For musical results, remember that typical human 
  hearing range is 20-20000Hz.
  
  Audio Duration in Seconds: The length of the file that will be created. 
  
  Output Filepath: where you’d like to save the audio file, including the name of 
  the file and .wav extension.

After the output filepath is entered, TideSynth will generate a .wav file based 
on the data provided. If the script returns errors, try removing spaces from 
folder names in the input and output file paths and try again.



Extras

TideSynth is designed to accept CSV based on data from the NOAA tidal harmonic
constituent page. But other data can be used, so long as it’s formatted to match
the format of the NOAA data. 

For a challenge, try building a dataset based on the moons of Jupiter. You will
need to find the period and current phase of each moon’s revolution. Since there 
are no historical water level data from the Jovian surface, you’ll need to use 
some other number for the “amplitude” value. The amplitudes of major tidal 
constituents are proportional to their gravitational force. We’re not so concerned
with absolute values; it’s more about the ratio between a given moon’s amplitude 
and the largest constituent represented by the fundamental. 


For more information on tides and tide prediction, check out these NOAA publications:

  NOAA Special Publication NOS CO-OPS 3 - Tidal Analysis and Predictions 
  https://tidesandcurrents.noaa.gov/publications/Tidal_Analysis_and_Predictions.pdf

  Special Publication No. 98: Manual of Harmonic Analysis and Prediction of Tides
  https://tidesandcurrents.noaa.gov/publications/SpecialPubNo98.pdf
