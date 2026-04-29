@echo off
title HIRO SOVEREIGN AGENT - FULL ACTIVATION
echo ====================================================
echo      HIRO SOVEREIGN OS (V9.2) - ONE-CLICK LAUNCH
echo ====================================================

:: 1. Start the C# Perception Engine (The Eyes)
echo [1/4] Launching Nerve Engine (C# DXGI)...
cd /d "e:\Hiro_Master\PROJECTS\HS_Gravity_Framework\SOVEREIGN_CORE_CS\SovereignPerception\bin\Release\net8.0"
start "Hiro_Eyes" SovereignPerception.exe

:: 2. Wait for MMF Sync
echo [2/4] Waiting for Synapse stabilization (2s)...
timeout /t 2 /nobreak > nul

:: 3. Ignite Telegram Bot (The Messenger)
echo [3/4] Igniting Telegram Reflex Bot...
cd /d "e:\Hiro_Master"
start "Hiro_Telegram" cmd /c "python ignite_hiro.py"

:: 4. Launch the Python Decision Engine (The Brain)
echo [4/4] Awakening the Cognitive Stack (Python)...
cd /d "e:\Hiro_Master\PROJECTS\HS_Gravity_Framework"
python hiro_main.py

echo ====================================================
echo  HIRO SOVEREIGN OS IS NOW FULLY ONLINE (V9.2)
echo ====================================================
pause
