@echo off
title Neural Synergy Mastery Dashboard
:main_menu
cls
echo ==================================================
echo      NEURAL SYNERGY - STRATEGIC MASTERY HUB
echo ==================================================
echo  [1] RUN HUD (Live Camera)        [2] EVALUATE (Metrics)
echo   11. YOLOv8                     21. YOLOv8
echo   12. ResNet50                   22. ResNet50
echo   13. EfficientNet-B0            23. EfficientNet-B0
echo   14. MobileNetV2                24. MobileNetV2
echo --------------------------------------------------
echo  [3] INTEGRITY TEST (Sanity)      [4] TRAINING (Master Evolution)
echo   31. YOLOv8                     41. YOLOv8
echo   32. ResNet50                   42. ResNet50
echo   33. EfficientNet-B0            43. EfficientNet-B0
echo   34. MobileNetV2                44. MobileNetV2
echo
echo  [5] HYPER-TUNING (Search)      [6] XAI ^& ABLATION (Insight)
echo   51. ALL MODELS                 61. ResNet50
echo   52. SPECIFIC MODEL             62. MobileNetV2
echo                                  63. EfficientNet-B0
echo                                  64. YOLOv8
echo --------------------------------------------------
echo  [7] FINAL REPORT (Mastery)       [8] AUTO-EVOLUTION (Loop)
echo --------------------------------------------------
echo  T. TEST ALL MODELS               E. EXIT MISSION
echo ==================================================
set /p choice="Selection ID: "

:: --- Evolution Loop ---
if "%choice%"=="8" (python models\MASTER_EVOLUTION.py & pause & goto main_menu)

:: --- Hyper-Tuning ---
if "%choice%"=="51" (goto run_tuning_all)
if "%choice%"=="52" (set /p m_id="Model ID (resnet/mobile/efficient/yolo): " & goto run_tuning_specific)

:: --- XAI & Ablation ---
if "%choice%"=="61" (set "target_dir=DL - imagenet" & set "model_id=resnet" & goto run_xai)
if "%choice%"=="62" (set "target_dir=DL - mobilenet" & set "model_id=mobile" & goto run_xai)
if "%choice%"=="63" (set "target_dir=DL - efficientnet b0" & set "model_id=efficient" & goto run_xai)
if "%choice%"=="64" (set "target_dir=DL -YOLO" & set "model_id=yolo" & goto run_xai)

:: --- Reporting ---
if "%choice%"=="7" (goto run_report)

:: --- HUD Launchers ---
if "%choice%"=="11" (set target_dir=DL -YOLO& goto run_hud)
if "%choice%"=="12" (set target_dir=DL - imagenet& goto run_hud)
if "%choice%"=="13" (set target_dir=DL - efficientnet b0& goto run_hud)
if "%choice%"=="14" (set target_dir=DL - mobilenet& goto run_hud)

:: --- Evaluation (Benchmarking) ---
if "%choice%"=="21" (set target_dir=DL -YOLO& set model_id=1& goto evaluate_model)
if "%choice%"=="22" (set target_dir=DL - imagenet& set model_id=2& goto evaluate_model)
if "%choice%"=="23" (set target_dir=DL - efficientnet b0& set model_id=3& goto evaluate_model)
if "%choice%"=="24" (set target_dir=DL - mobilenet& set model_id=4& goto evaluate_model)

:: --- Individual Integrity Tests ---
if "%choice%"=="31" (set target_dir=DL -YOLO& set model_id=1& goto test_model)
if "%choice%"=="32" (set target_dir=DL - imagenet& set model_id=2& goto test_model)
if "%choice%"=="33" (set target_dir=DL - efficientnet b0& set model_id=3& goto test_model)
if "%choice%"=="34" (set target_dir=DL - mobilenet& set model_id=4& goto test_model)

:: --- Training (Retrain) ---
if "%choice%"=="41" (set target_dir=DL -YOLO& goto run_train)
if "%choice%"=="42" (set target_dir=DL - imagenet& goto run_train)
if "%choice%"=="43" (set target_dir=DL - efficientnet b0& goto run_train)
if "%choice%"=="44" (set target_dir=DL - mobilenet& goto run_train)

:: --- Global Commands ---
if /i "%choice%"=="T" goto test_all
if /i "%choice%"=="E" goto end
goto main_menu

:test_all
echo [INFO] Running Global Integrity Audit across all modules...
for %%d in ("DL -YOLO" "DL - imagenet" "DL - efficientnet b0" "DL - mobilenet") do (
    if exist "%%d\AUTO_TEST_MODELS.py" (
        echo.
        echo >>> Testing %%d...
        cd "%%~d"
        python AUTO_TEST_MODELS.py
        cd ..
    )
)
pause
goto main_menu

:run_hud
echo [INFO] Initializing Live HUD in %target_dir%...
cd "%target_dir%"
python inference_hud.py
cd ..
pause
goto main_menu

:evaluate_model
echo [INFO] Benchmarking Model %model_id% in %target_dir%...
cd "%target_dir%"
python AUTO_TEST_MODELS.py --model %model_id% --evaluate
cd ..
pause
goto main_menu

:test_model
echo [INFO] Testing Integrity of Model %model_id% in %target_dir%...
cd "%target_dir%"
python AUTO_TEST_MODELS.py --model %model_id%
cd ..
pause
goto main_menu

:run_tuning_all
echo [INFO] Starting Global Hyper-Tuning Search...
echo [INFO] Tuning YOLOv8...
if exist "DL -YOLO\hyper_tuner.py" (cd "DL -YOLO" && python hyper_tuner.py yolo && cd ..)
echo [INFO] Tuning ResNet50...
if exist "DL - imagenet\hyper_tuner.py" (cd "DL - imagenet" && python hyper_tuner.py resnet && cd ..)
echo [INFO] Tuning EfficientNet-B0...
if exist "DL - efficientnet b0\hyper_tuner.py" (cd "DL - efficientnet b0" && python hyper_tuner.py efficient && cd ..)
echo [INFO] Tuning MobileNetV2...
if exist "DL - mobilenet\hyper_tuner.py" (cd "DL - mobilenet" && python hyper_tuner.py mobile && cd ..)
pause
goto main_menu

:run_tuning_specific
echo [INFO] Running Specific Tuning on %m_id%...
:: Try to find which folder contains the target
if /i "%m_id%"=="resnet" set target_dir=DL - imagenet
if /i "%m_id%"=="mobile" set target_dir=DL - mobilenet
if /i "%m_id%"=="efficient" set target_dir=DL - efficientnet b0
if /i "%m_id%"=="yolo" set target_dir=DL -YOLO

if defined target_dir (
    cd "%target_dir%"
    python hyper_tuner.py %m_id%
    cd ..
) else (
    echo [ERROR] Unknown Model ID: %m_id%
)
pause
goto main_menu

:run_train
echo [WARNING] Initiating Local Training Pipeline in %target_dir%...
echo Ensure dataset is correctly structured in %target_dir%/dataset
pause
cd "%target_dir%"
python train_local.py
cd ..
pause
goto main_menu

:run_xai
echo [INFO] Running XAI Mastery Analysis on %model_id% in %target_dir%...
cd "%target_dir%"
if exist xai_ablation.py (
    python xai_ablation.py %model_id%
) else (
    echo [ERROR] XAI script missing in %target_dir%
)
cd ..
pause
goto main_menu

:run_report
for %%d in ("DL -YOLO" "DL - imagenet" "DL - efficientnet b0" "DL - mobilenet") do (
    if exist "%%d\FINAL_REPORT.md" (
        echo.
        echo ==================================================
        echo   REPORT: %%d
        echo ==================================================
        cd "%%~d"
        type FINAL_REPORT.md
        cd ..
    )
)
pause
goto main_menu

:end
echo Mission Terminated.
timeout /t 2 >nul
exit
