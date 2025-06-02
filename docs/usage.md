# Usage Examples

## 1. Command-line Runner  
```sh
python -m Engine.Launcher.LauncherMain
```
Outputs JSON with combined results.

## 2. Streamlit Dashboard  
```sh
streamlit run Engine/Launcher/StreamLitLauncher.py
```
- Upload or process a folder.  
- Click **Start Analysis**.  
- View LLM, Vector, Combined bar charts and progress bars.

## 3. Inspect Storage CSV  
```csv
serial_id,filename,sexually_explicit_material,…,type,time
1234.1,500041100578_227978.jpg,34.59,33.85,…,VectorScoring,0.835173
```
