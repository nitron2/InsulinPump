# Hayden Baldwin | NitroStudios | Feb 1 2023
Total Hours: 14.5
7 testing
5 UI issues
2.5 Logicd

## Goals:
1. Simulates blood glucose of a diabetic person with insulin injection. 
2. If velocity of blood glucose is positive but acceleration is zero, inject a standard amount of insulin x units, unless blood glucose is in the safe range. 
3. Blood has insulin capacity. Min and max. Insulin is metabolized (removed from) [in] the blood at a of x units/10 minutes. 
4. The more insulin in the blood, the more likely blood glucose is to reduce. 
5. There is a probability of an anomaly in insulin (i.e., jumping randomly). 
6. Blood glucose is not completely random, but a **trend**, influenced by insulin injection. 
7. Object-oriented. 
8. UI with line graph of blood glucose over time. 
9. Ability to turn on and off pump to show insulin pump's effectiveness.
10. Max blood glucose in 200 mg/dL.
11. Toggleable alarm.
12. Battery simulated.
13. If blood glucose is increasing and is in high range, and has positive acceleration, inject a computed amount.

## Non-goals:
1. [ ] Perfectly staying between the low and high boundaries for blood glucose.
2. [ ] OOP elements simulate environment with the highest level of fidelity. 
3. (In real life, the injector would compute blood glucose acceleration, instead of the patient's blood reporting it to the sensors).