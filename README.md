# crime_hotspots_simulation_analysis
This repo implements two papers related to crime hotspots simulation and spatial analysis.

## Crime hotspots simulation
paper: [A statistical model of criminal behavior (Short et al., 2008)](http://paleo.sscnet.ucla.edu/ShortEtAl2008-M3AS.pdf)

### Reproduce experiment

#### Fig.3 (a) - no signicant hotspots
https://user-images.githubusercontent.com/43054769/126831590-37efd0e8-5813-4d05-a210-e9c2050b5bec.mp4

#### Fig.3 (b) - dynamic hotspots
https://user-images.githubusercontent.com/43054769/126831603-66c534bb-5a64-4cb1-98e7-2bf00a0d3f1e.mp4

#### Fig.3 (c) - stable hotspots
https://user-images.githubusercontent.com/43054769/126831609-1ef801c2-d6d8-46af-8fb6-9e0fb1ac2704.mp4

#### Fig.3 (d) - dynamic hotspots with larger deformations
https://user-images.githubusercontent.com/43054769/126831621-5ad7cf6e-6c49-410b-8fef-6cde0fb83cee.mp4


## Quick start
```bash
# run experiment (a) in Fig.3 for 200 days; plot every 0.5 day
python main.py --expset a --T 200 --plot_rate 0.5
```
