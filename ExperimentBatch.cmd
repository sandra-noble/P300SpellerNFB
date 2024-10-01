@echo off
setlocal enabledelayedexpansion

:: get the subject number
if "%~1"=="" (
  set /p subject_num=Please enter a subject number or name: 
) else (
  set subject_num=%1
)

:: get the group number
if "%~2"=="" (
  set /p group=Please enter a group number; 1-Control1, 2-Control2, 3-Experimental:
) else (
  set group=%2
)

:: get start time of experiment
set "start_time=%time%"

:: need to run all the scenarios with the same random seed for replicability
set rand_seed=0

:: create directory for subject where all recorded files are saved to
set subj_dir=%SUBJECT_PATH%\Subject-%subject_num%
if not exist "%subj_dir%" (
  mkdir "%subj_dir%"
) else (
  echo This subject already exists. Please enter a new subject number or name.
  goto eof
)

:: create path with / instead of \ for config files
set subj_dir_config=%SUBJECT_PATH_CONFIG%/Subject-%subject_num%

:: create logfile to save RT and accuracies to
set log_file=%subj_dir%\log.txt
set log_file_config=%subj_dir_config%/log.txt

:: write to logfile
echo Subject %subject_num% > "%log_file%"
if %group%==1 echo Control group 1 >> "%log_file%"
if %group%==2 echo Control group 2 >> "%log_file%"
if %group%==3 echo Experimental group >> "%log_file%"
echo Start Time: %start_time% >> "%log_file%"
echo Pre-training: >> "%log_file%"

:: start openvibe acquisition server
cd "%OV_ROOT%"
call openvibe-acquisition-server --run-bg

pause

:rdmtrain
set "rdm_start=%time%"
echo RDM Training: >> "%log_file%"
echo RDM train start: %rdm_start% >> "%log_file%"
cd "%RDM_PATH%"

:: run first block
call RDMcont_training.py %subject_num% train-01 "%log_file%" "%subj_dir%" 1

:: run second block
call RDMcont_training.py %subject_num% train-02 "%log_file%" "%subj_dir%" 2

:: run third block
call RDMcont_training.py %subject_num% train-03 "%log_file%" "%subj_dir%" 3

:rdmpre
set "rdm_start=%time%"
echo RDM Task: >> "%log_file%"
echo RDM start: %rdm_start% >> "%log_file%"

:: run RDM task
call RDMcont.py %subject_num% 01 "%log_file%" "%subj_dir%"

set "rdm_stop=%time%"
echo RDM stop: %rdm_stop% >> "%log_file%"

:acq
:: start openvibe acquisition server
cd "%OV_ROOT%"
call openvibe-acquisition-server --run-bg

pause

:: need to test the signal acquisition quality (eye-blinks, jaw clenching, alpha waves)
call openvibe-designer --no-pause --no-gui --random-seed %rand_seed% --play "%OV_PATH_CUM%\0-signal-monitoring.xml"

pause

:cal
:: set where to save the recorded file in calibration run 1
set scenario1_record_file1=%subj_dir_config%/calibration-signal1.ov

:: set what word to play in calibration run 1 and the number of flashes
set word=the
set num_letters=3
set num_flash=12

:: run the first scenario (acquisition)
call openvibe-designer --no-pause --no-gui --random-seed %rand_seed% --define word %word% ^
--define num_letters %num_letters% --define num_flash %num_flash% ^
--define save_file "%scenario1_record_file1%" --play "%OV_PATH_CUM%\1-acquisition.xml"

:: set where to save the recorded file in calibration run 2
set scenario1_record_file2=%subj_dir_config%/calibration-signal2.ov

:: set what word to play in calibration run 2 and the number of flashes
set word=quick
set num_letters=5
set num_flash=12

pause

:: run the first scenario (acquisition)
call openvibe-designer --no-pause --no-gui --random-seed %rand_seed% --define word %word% ^
--define num_letters %num_letters% --define num_flash %num_flash% ^
--define save_file "%scenario1_record_file2%" --play "%OV_PATH_CUM%\1-acquisition.xml"

:: concatenate the signals from both calibration runs
set scenario1_record_files=%subj_dir_config%/calibration-signals.ov

call openvibe-designer --no-pause --no-gui --random-seed %rand_seed% --define first_file "%scenario1_record_file1%" ^
--define second_file "%scenario1_record_file2%" --define concat_file "%scenario1_record_files%" ^
--play-fast "%OV_PATH_CUM%\signal-concatenation.xml"

:: define the number of virtual channels to use and save files for config files
set num_channels=3
set xdawn_config_file=%subj_dir_config%/spatial-filter.cfg
set class_config_file=%subj_dir_config%/classifier.cfg

:: run the second and third scenarios (filter and classifier training) in fast forward
call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define load_file "%scenario1_record_files%" --define num_channels %num_channels% ^
--define config_file "%xdawn_config_file%" --play-fast "%OV_PATH_CUM%\2-train-xDAWN.xml"

call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define load_file "%scenario1_record_files%" --define xdawn_config_file "%xdawn_config_file%" ^
--define config_file "%class_config_file%" --play-fast "%OV_PATH_CUM%\3-train-classifier.xml"

pause

:eval
:: evaluate the speller quality
set word=dog
set num_letters=3
set num_flash=12
set save_file_raw=%subj_dir_config%/eval-raw.ov
set save_file_processed=%subj_dir_config%/eval-processed.ov

:: write to logfile
echo Evaluation spelling accuracy: >> "%log_file%"

call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define word %word% --define num_letters %num_letters% --define num_flash %num_flash% ^
--define save_file_raw "%save_file_raw%" --define save_file_processed "%save_file_processed%" ^
--define xdawn_config_file "%xdawn_config_file%" --define class_config_file "%class_config_file%" ^
--define accuracy_file "%log_file_config%" --play "%OV_PATH_CUM%\4-online.xml"

:: re-train filter and classifier if less than 2 letters were correct
:ask
set /p next=Enter 1 for training, 2 for re-calibration: 

if %next%==1 goto train
if %next%==2 goto recal
goto ask

:recal
:: re-training with the dog file
set retrain_file=%subj_dir_config%/retrain-signal.ov

:: add evaluation file to calibration signals
call openvibe-designer --no-pause --no-gui --random-seed %rand_seed% --define first_file "%scenario1_record_files%" ^
--define second_file "%save_file_raw%" --define concat_file "%retrain_file%" ^
--play-fast "%OV_PATH_CUM%\signal-concatenation.xml"

:: define the number of virtual channels to use and save files for config files
set num_channels=3

:: run the second and third scenarios (filter and classifier training) in fast forward
call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define load_file "%retrain_file%" --define num_channels %num_channels% ^
--define config_file "%xdawn_config_file%" --play-fast "%OV_PATH_CUM%\2-train-xDAWN.xml"

call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define load_file "%retrain_file%" --define xdawn_config_file "%xdawn_config_file%" ^
--define config_file "%class_config_file%" --play-fast "%OV_PATH_CUM%\3-train-classifier.xml"

:: do another evaluation
set word=fox
set num_letters=3
set num_flash=12
set save_file_raw=%subj_dir_config%/eval2-raw.ov
set save_file_processed=%subj_dir_config%/eval2-processed.ov

:: write to logfile
echo Evaluation 2 spelling accuracy: >> "%log_file%"

pause 

call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define word %word% --define num_letters %num_letters% --define num_flash %num_flash% ^
--define save_file_raw "%save_file_raw%" --define save_file_processed "%save_file_processed%" ^
--define xdawn_config_file "%xdawn_config_file%" --define class_config_file "%class_config_file%" ^
--define accuracy_file "%log_file_config%" --play "%OV_PATH_CUM%\4-online.xml"

:: stop experiment if still not 2 letters correct
:ask2
set /p "continue=Enter 1 to continue experiment, 2 to stop: "
if %continue%==1 goto train
if %continue%==2 goto eof

goto ask2


:train
:: loop for online p300 speller

set "train_start=%time%"
:: write to logfile
echo =================================== >> "%log_file%"
echo P300 speller training: >> "%log_file%"
echo Train start: %train_start% >> "%log_file%"

:: first run with 10 flashes
set word=beautiful
set num_letters=9
set num_flash=10

:: set save files to reflect the run number
set save_file_raw=%subj_dir_config%/training-run-1-raw.ov
set save_file_processed=%subj_dir_config%/training-run-1-processed.ov

echo save_file_raw %save_file_raw%
echo save_file_processed %save_file_processed%

:: write to logfile
echo Run 1: number of flashes = %num_flash%, word = %word% >> "%log_file%"
echo Spelling accuracy: >> "%log_file%"

pause

:: run the 4th scenario with the new settings
cd "%OV_ROOT%"
call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define word %word% --define num_letters %num_letters% --define num_flash %num_flash% ^
--define save_file_raw "%save_file_raw%" --define save_file_processed "%save_file_processed%" ^
--define xdawn_config_file "%xdawn_config_file%" --define class_config_file "%class_config_file%" ^
--define accuracy_file "%log_file_config%" --play "%OV_PATH_CUM%\4-online.xml"
  
:: runs 2 to 5 with adaptive number of flashes
set num_runs=5

set flash_file=%subj_dir%\num_flash_file.txt

::set /a "end=%num_runs%-1"

echo for loop

for /l %%i in (2,1,%num_runs%) do (
  echo run %%i
 
  :: call the matlab script to calculate the new number of flashes
  cd "%MATLAB_PATH%"
  if %group%==1 start matlab -wait -minimize -nosplash -nodesktop -r "control1('%flash_file%','%log_file%'); exit"
  if %group%==2 start matlab -wait -minimize -nosplash -nodesktop -r "control2('%flash_file%'); exit"
  if %group%==3 start matlab -wait -minimize -nosplash -nodesktop -r "experimental('%flash_file%','%log_file%'); exit"

  :: wait for matlab to overwrite the file --> when black window closes again
  pause
  
  :: get the new number of flashes from the file
  set /p num_flash=<"%flash_file%"
  
  echo !num_flash! flashes

  :: write to logfile
  echo Run %%i: number of flashes = !num_flash!, word = !word! >> "%log_file%"
  echo Spelling accuracy: >> "%log_file%"

  :: set save files to reflect the run number
  set save_file_raw=%subj_dir_config%/training-run-%%i-raw.ov
  set save_file_processed=%subj_dir_config%/training-run-%%i-processed.ov

  echo save_file_raw !save_file_raw!
  echo save_file_processed !save_file_processed!

  pause

  :: run the 4th scenario with the new settings
  cd "%OV_ROOT%"
  call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
  --define word !word! --define num_letters %num_letters% --define num_flash !num_flash! ^
  --define save_file_raw "!save_file_raw!" --define save_file_processed "!save_file_processed!" ^
  --define xdawn_config_file "%xdawn_config_file%" --define class_config_file "%class_config_file%" ^
  --define accuracy_file "%log_file_config%" --play "%OV_PATH_CUM%\4-online.xml"
)

set "train_stop=%time%"
echo Training stop: %train_stop% >> "%log_file%"

:post
:: run the 4th scenario with the same settings as before training
set word=dance
set num_letters=5
set num_flash=12
set save_file_raw=%subj_dir_config%/post-training-raw.ov
set save_file_processed=%subj_dir_config%/post-training-processed.ov

:: write to logfile
echo =================================== >> "%log_file%"
echo Post-training: >> "%log_file%"
echo P300 speller: number of flashes = %num_flash%, word = %word% >> "%log_file%"
echo Spelling accuracy: >> "%log_file%"

echo save_file_raw %save_file_raw%
echo save_file_processed %save_file_processed%

pause 

call openvibe-designer --no-pause --no-gui --no-session-management --random-seed %rand_seed% ^
--define word %word% --define num_letters %num_letters% --define num_flash %num_flash% ^
--define save_file_raw "%save_file_raw%" --define save_file_processed "%save_file_processed%" ^
--define xdawn_config_file "%xdawn_config_file%" --define class_config_file "%class_config_file%" ^
--define accuracy_file "%log_file_config%" --play "%OV_PATH_CUM%\4-online.xml"

pause

:rdmpost
set "rdm_start=%time%"
echo RDM task: >> "%log_file%"
echo RDM start: %rdm_start% >> "%log_file%"
:: run RDM task
cd "%RDM_PATH%"
call RDMcont.py %subject_num% 02 "%log_file%" "%subj_dir%"

:: get end time of experiment
set "end_time=%time%"

echo End Time: %end_time% >> "%log_file%"

:eof
pause
