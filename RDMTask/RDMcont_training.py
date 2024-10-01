#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'RDMcont'  # from the Builder filename that created this script
expInfo = {'participant': sys.argv[1], 'session': sys.argv[2]}
#dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName, show=False)
#if dlg.OK == False:
#    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = sys.argv[4] + os.sep + u'RDM%s_%s' % (expInfo['participant'], expInfo['session'])

# log file to save response time and accuracy to
performance_file = open(sys.argv[3],'a')

# define which coherence levels to use using the fourth input argument
if(sys.argv[5] == '1'):
    conditions = 'train_conditions1.xlsx' # 80-60
elif(sys.argv[5] == '2'):
    conditions = 'train_conditions2.xlsx' # 40-30
else:
    conditions = 'train_conditions3.xlsx' # 25-20

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='RDMcont_training.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.DATA)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=1, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='LaptopMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=False, 
    units='height')
win.mouseVisible = False

# store frame rate of monitor if we can measure it
# expInfo['frameRate'] = win.getActualFrameRate()
expInfo['frameRate'] = 60.0
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='Press the left arrow key with your left hand to indicate leftward motion.\nPress the right arrow key with your right hand to indicate rightward motion.\nPress space to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=0.0);
key_respIns = keyboard.Keyboard()

# Initialize components for Routine "coherent"
coherentClock = core.Clock()
cross = visual.ShapeStim(
    win=win, name='cross', vertices='cross',
    size=(0.05, 0.05),
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=0.0, interpolate=True)
dots = visual.DotStim(
    win=win, name='dots', units='deg',
    nDots=118, dotSize=6.0,
    # speed should be 3.33 deg/sec, i.e. 3.33/60.0, 
    # however, there is an issue with psychopy where the speed is relative to 
    # the aperture size, so 5/3.33 = 1.5 
    # (https://github.com/psychopy/psychopy/issues/781)
    speed=1.5/60.0, dir=1.0, coherence=1.0,
    fieldPos=(0.0, 0.0), fieldSize=5,fieldShape='circle',
    signalDots='same', noiseDots='direction',dotLife=-1.0,
    color=[-1.0,-1.0,-1.0], colorSpace='rgb', opacity=None,
    depth=-1.0)
key_resp = keyboard.Keyboard()

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
feedbackTxt = visual.TextStim(win=win, name='feedbackTxt',
    text='This is the end of the task.',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
coherentTrials = data.TrialHandler(nReps=1.0, method='fullRandom', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(conditions),
    seed=None, name='coherentTrials')
thisCoherentTrial = coherentTrials.next()  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisCoherentTrial != None:
    for paramName in thisCoherentTrial:
        exec('{} = thisCoherentTrial[paramName]'.format(paramName))
        
incoherentTrials = data.TrialHandler(nReps=20.0, method='fullRandom',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('incoherent_conditions.xlsx'),
    seed=None, name='incoherentTrials')
thisIncoherentTrial = incoherentTrials.next()
if thisIncoherentTrial != None:
    for paramName in thisIncoherentTrial:
        exec('{} = thisIncoherentTrial[paramName]'.format(paramName))

# save the number of correct responses and RT for each trial
correct_counter = 0
wrong_counter = 0
RT = [0] * len(coherentTrials.trialList) * coherentTrials.nReps

# ------Prepare to start Routine "instructions"-------
continueRoutine = True
# update component parameters for each repeat
key_respIns.keys = []
key_respIns.rt = []
_key_respIns_allKeys = []
# keep track of which components have finished
instructionsComponents = [text, key_respIns]
for thisComponent in instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instructionsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        text.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_respIns.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_respIns.frameNStart = frameN  # exact frame index
        key_respIns.tStart = t  # local t and not account for scr refresh
        key_respIns.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_respIns, 'tStartRefresh')  # time at next scr refresh
        key_respIns.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_respIns.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_respIns.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_respIns.status == STARTED and not waitOnFlip:
        theseKeys = key_respIns.getKeys(keyList=['space'], waitRelease=False)
        _key_respIns_allKeys.extend(theseKeys)
        if len(_key_respIns_allKeys):
            key_respIns.keys = _key_respIns_allKeys[-1].name  # just the last key pressed
            key_respIns.rt = _key_respIns_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
    
# ------Prepare to start Routine "coherent"-------
continueRoutine = True
isCoherent = False
buttonPressed = False
coherentCounter = 0
correctButton = None
lastTrial = False
# update component parameters for each repeat
dots.setDir(0)
dots.setFieldCoherence(0)
dots.refreshDots()
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []

# keep track of which components have finished
coherentComponents = [cross, dots, key_resp]
for thisComponent in coherentComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
coherentClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "coherent"-------
while continueRoutine:
    # get current time
    t = coherentClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=coherentClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
        
    # *cross* updates
    if cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        cross.frameNStart = frameN  # exact frame index
        cross.tStart = t  # local t and not account for scr refresh
        cross.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(cross, 'tStartRefresh')  # time at next scr refresh
        cross.setAutoDraw(True)
    if cross.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > cross.tStartRefresh + 2.9-frameTolerance:
            # keep track of stop time/frame for later
            cross.tStop = t  # not accounting for scr refresh
            cross.frameNStop = frameN  # exact frame index
            win.timeOnFlip(cross, 'tStopRefresh')  # time at next scr refresh
            cross.setAutoDraw(False)
        
    # *dots* updates
    if dots.status == NOT_STARTED and tThisFlip >= 3.0-frameTolerance:
        # keep track of start time/frame for later
        dots.frameNStart = frameN  # exact frame index
        dots.tStart = t  # local t and not account for scr refresh
        dots.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(dots, 'tStartRefresh')  # time at next scr refresh
        dots.setAutoDraw(True)
        lastIncoherent = tThisFlip
        lastCoherent = 0
        
    # change direction and coherence level once incoherent trial time is up
    if dots.status == STARTED and tThisFlip >= lastIncoherent+show_time-frameTolerance and not isCoherent:
        lastIncoherent = 0
        lastCoherent = tThisFlip
        isCoherent = True
        coherentCounter += 1
        correctButton = correct_button
        # change coherence level
        dots.setFieldCoherence(coherence_level)
        # change direction
        dots.setDir(direction)
        # move on to next coherent trial
        try:
            thisCoherentTrial = coherentTrials.next()
        except StopIteration:
            lastTrial = True
        if thisCoherentTrial != None:
            for paramName in thisCoherentTrial:
                exec('{} = thisCoherentTrial[paramName]'.format(paramName))
        
    # change to incoherent motion once coherent trial time is up
    if dots.status == STARTED and tThisFlip >= lastCoherent+1.9-frameTolerance and isCoherent:
        # check if no button was pressed during coherent motion
        if  not buttonPressed and not coherentCounter == 0 \
            and key_resp.status == STARTED and not waitOnFlip:
            logging.log(msg='Missed trial',level=logging.DATA)
            logging.flush()
            performance_file.write('Missed trial, no RT\n')
            thisExp.addData('correct button', correctButton)
            thisExp.addData('key_resp.keys', 'None')
            thisExp.addData('key_resp.corr', 3) # meaning missed motion
            thisExp.addData('key_resp.tStart', key_resp.tStart)
            thisExp.addData('key_resp.rt', 'None')
            thisExp.addData('lastCoherent', lastCoherent)
            thisExp.addData('RT', 0) 
            thisExp.nextEntry()
        buttonPressed = False
        lastIncoherent = tThisFlip
        lastCoherent = 0
        correctButton = None
        # change coherence level
        dots.setFieldCoherence(0)
        # change direction
        dots.setDir(0)
        isCoherent = False
        # move on to next incoherent trial
        try:
            thisIncoherentTrial = incoherentTrials.next()
        except StopIteration:
            continueRoutine = False
        if thisIncoherentTrial != None:
            for paramName in thisIncoherentTrial:
                exec('{} = thisIncoherentTrial[paramName]'.format(paramName))
                
        if lastTrial:
            continueRoutine = False
            break
        
    # *key_resp* updates
    waitOnFlip = False
    newKey = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 3.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    # only check for button presses if the dots are already displaying
    if key_resp.status == STARTED and not waitOnFlip and dots.status == STARTED:
        theseKeys = key_resp.getKeys(keyList=['left', 'right'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(theseKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # was this correct?
            if isCoherent:
                if (key_resp.keys == str(correctButton)) or (key_resp.keys == correctButton):
                        key_resp.corr = 1 # correct
                        correct_counter = correct_counter + 1
                        logging.log(msg='Correct',level=logging.DATA)
                        logging.flush()
                        performance_file.write('Correct, ')
                        RT[coherentCounter-1] = (key_resp.rt + key_resp.tStart) - lastCoherent
                        performance_file.write('RT: ' + str(round((key_resp.rt + key_resp.tStart) - lastCoherent,3)) + 's\n')
                        buttonPressed = True
                else:
                    if isCoherent:
                        key_resp.corr = 0 # wrong
                        wrong_counter = wrong_counter + 1
                        logging.log(msg='Wrong',level=logging.DATA)
                        logging.flush()
                        performance_file.write('Wrong, ')
                        performance_file.write('RT: ' + str(round((key_resp.rt + key_resp.tStart) - lastCoherent,3)) + 's\n')
                        buttonPressed = True
            else:
                key_resp.corr = 2 # false alarm or too late
                logging.log(msg='False alarm/too late',level=logging.DATA)
                logging.flush()
                performance_file.write('False alarm or too late, no RT\n')
            
            thisExp.addData('correct button', correctButton)
            thisExp.addData('key_resp.keys',key_resp.keys)
            thisExp.addData('key_resp.corr', key_resp.corr)
            thisExp.addData('key_resp.tStart', key_resp.tStart)
            thisExp.addData('key_resp.rt', key_resp.rt)
            thisExp.addData('lastCoherent', lastCoherent)
            thisExp.addData('RT', (key_resp.rt + key_resp.tStart) - lastCoherent) 
            thisExp.nextEntry()
        
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in coherentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
        
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    
# -------Ending Routine "coherent"-------
for thisComponent in coherentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "coherent" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "feedback"-------
continueRoutine = True
# keep track of which components have finished
feedbackComponents = [feedbackTxt]
for thisComponent in feedbackComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "feedback"-------
while continueRoutine:
    # get current time
    t = feedbackClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=feedbackClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *feedbackTxt* updates
    if feedbackTxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        feedbackTxt.frameNStart = frameN  # exact frame index
        feedbackTxt.tStart = t  # local t and not account for scr refresh
        feedbackTxt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(feedbackTxt, 'tStartRefresh')  # time at next scr refresh
        feedbackTxt.setAutoDraw(True)
    if feedbackTxt.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > feedbackTxt.tStartRefresh + 3.0-frameTolerance:
            # keep track of stop time/frame for later
            feedbackTxt.tStop = t  # not accounting for scr refresh
            feedbackTxt.frameNStop = frameN  # exact frame index
            win.timeOnFlip(feedbackTxt, 'tStopRefresh')  # time at next scr refresh
            feedbackTxt.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "feedback"-------
for thisComponent in feedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

routineTimer.reset()

# calculate accuracy and average RT and save to file
accuracy = correct_counter / (len(coherentTrials.trialList)*coherentTrials.nReps)
accuracy_wrong = wrong_counter / (len(coherentTrials.trialList)*coherentTrials.nReps)
avg_rt = np.sum(RT) / correct_counter

performance_file.write('Accuracy (correct): ' + str(accuracy) + \
    ', wrong replies: ' + str(accuracy_wrong) + \
    ', mean RT: ' + str(round(avg_rt,3)) + '\n')
performance_file.close()
  
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
