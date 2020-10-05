SET logfile="C:\Users\Tsipis\Documents\data\run.log"
@echo off
@echo Starting Script at %date% %time% >> %logfile%
%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -Command "& 'C:\Users\Tsipis\anaconda3\shell\condabin\conda-hook.ps1' ; conda activate 'C:\Users\Tsipis\anaconda3\envs\phaetons_37' ; python C:\Users\Tsipis\phaetons\data\demokritos\data_demokritos.py -t 24h; python C:\Users\Tsipis\phaetons\data\demokritos\data_weather_predictions.py ; conda deactivate"
@echo finished at %date% %time% >> %logfile%
