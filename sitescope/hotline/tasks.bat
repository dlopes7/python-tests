D:\SiteScope\scripts\psexec\PsExec.exe \\Atac-prd02.dc.nova cmd /c "wevtutil qe Microsoft-Windows-TaskScheduler/Operational "/q:*[System[(Level=1 or Level=2 or Level=3)]]" -rd:true -f:text" > eventos.log