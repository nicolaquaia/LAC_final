# Final Report of LAC Course
In this report, a new version of the DTU 10 MW blade is proposed, building on the experience from the redesign completed within Group 1. The new design has the same goal: to change the wind class from 1A to 3B while adhering to the same design criteria—specifically, increasing the Annual Energy Production (AEP) while maintaining similar or lower design loads.

### Blades Analyzed:
1. **Original DTU 10 MW blade**: Referred to as 'DTU.'
2. **Group 1 Redesign**: Referred to as 'redesign.'
3. **Final New Version**: Referred to as 'remodel,' addressing the issues identified in Group 1's redesign.

### Issues with Group 1 Redesign:
- The redesigned blade had a reasonable shape but an inefficient control strategy, resulting in:
  - **Lower AEP**: -1.19%
  - **Resonance Phenomenon**: Occurring around 7 m/s, increasing design loads.

### Proposed Changes for the Remodel:
1. **Shorter Blade**: -1% to reduce the inertial moment and design loads, with minimal compromise on power production
2. **Larger Chord**: +0.5% to increase production while limiting load increases
3. **Reduced Safety Margin in Lift Coefficient Design**: A more aggressive aerodynamic design to enhance production
4. **Increased Rotor Speed**: To reduce torque after the rated speed
5. **Minimum Rotor Speed**: To avoid resonance problems
6. **Peak Shaving**: To reduce loads near the rated speed
7. **Lower Cut-in Speed**: Adjusted to align with the new wind class, shifting wind probability toward smaller wind speeds, thereby improving AEP.

### Methodology:
A complete redesign of the blade was undertaken:
1. **Shape Definition**: Developed using a Python script and tested with the HAWC2S program
2. **Operational Data Optimization**: Computed for both rigid and flex blades using HAWC2S to evaluate optimal TSR and expected CP
3. **Modal Analysis**: Conducted using HAWCStab2
4. **Control Tuning**: Performed with HAWC2S and HAWC2
5. **Design Load Evaluation**: Conducted with HAWC2.

---

## Group 1 Members:
&nbsp;&nbsp;&nbsp;Nicola Quaia&nbsp;&nbsp;s232439  
&nbsp;&nbsp;&nbsp;Mathéo Chala&nbsp;&nbsp;s233011
&nbsp;&nbsp;&nbsp;Bogusz Adam Glaza&nbsp;&nbsp;s233186  
