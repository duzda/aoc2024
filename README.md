# AoC 2024

This repo contains my solutions for [Aoc 2024](https://adventofcode.com/).

You can automate grabbing the input by providing *.cookie* file with the **session** cookie, that can be grabbed from the website while logged in.

`generate-day.sh` creates a new folder for specified date with `template.py` file.  
`curl-input.sh` downloads input data using provided *.cookie* file.  
`run.sh` runs the solution for specific day using `curl-input.sh`, you can provide `-a` flag, to run the second exercise of the day.  

All provided solutions are self-contained, meaning, everything is always in a single file and uses nothing outside of the standard Python library.  
Developed for **Python 3.12**.  
