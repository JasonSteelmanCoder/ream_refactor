# Summary
This repository contains scripts used to improve the numbers in a scholarly paper. The steps taken are below.

# Steps and Details
    fit curves to data
        trim the first 360 entries from the data (this is a noisy period during which the tape itself is still heating up)
        data comes from 7.27.22/ondrive/LAB/StemConduction/newraw
        learn to fit a curve and find its intersection with y = 20 degrees using fit_first_curves.py
        find all of the regressed 20 degree marks and durations using fit_curves.py
            use it to make durations.csv
            and fill in ream_notes_regressed.xlsx