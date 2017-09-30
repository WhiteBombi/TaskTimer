# Script Name        : TaskTimer.py
# Author             : WhiteBombo
# Created            : October 1st 2017
# Last modified      :
# Version            : 0.1
# Description        : Create, control and write several tasks and their running duration.

import os
import csv
from datetime import datetime


class Timer:
    '''Create a timer for multiple separately trackable tasks.'''

    def __init__(self, name):
        self.name = name  # Timer name, duh
        self.jobs = {}    # Task accrued duration
        self.state = {}   # Is a task running?

    def start(self, task):
        '''Sets a timestamp for start of the object counter. [E.g. self.start("task1")]'''
        if task in self.jobs:              # If exists
            if self.state[task] is False:  # If not running
                self.start_time = datetime.now()
            self.state[task] = True
        else:  # Create duration and state and try again
            self.jobs[task] = 0
            self.state[task] = False
            self.start(task)

    def stop(self, task):
        '''Calculates elapsed time and saves to dictionary. [E.g. self.stop("task1")]'''
        if self.state[task]:  # If running, calc secs
            elapsed = datetime.now() - self.start_time
            self.jobs[task] += elapsed.seconds
        self.state[task] = False

    def tally(self):
        '''Print time ran for each task. [E.g. self.tally()]'''
        for key, value in self.jobs.items():  # Calc and add up secs if running
            if self.state[key]:
                elapsed = datetime.now() - self.start_time
                self.jobs[key] += elapsed.seconds
            # Print the things
                state = '(Running)'
            else:
                state = '(Stopped)'
            print(f'Task "{key}" has run {self.jobs[key]} seconds.', state)
        print('Number of tasks:', len(self.jobs.keys()))

    def write(self, filename):
        '''Writes tasks to a .csv file. [E.g. self.write("file") or self.write("directory/file")]'''
        '''Tries to write to a directory if one is given.'''
        '''If directory doesn't exist, creates one and tries again.'''
        self.tally()
        try:
            with open(filename + '.csv', 'w') as csvfile:
                spreadsheet = csv.writer(csvfile, delimiter=',')
                spreadsheet.writerow(["Task name", "Total Duration"])
                for key, value in self.jobs.items():
                    spreadsheet.writerow([key, value])
        except FileNotFoundError:
            directory = filename.split('/')
            os.makedirs(directory[0])
            self.write(filename)
