# Architecture Overview

```plaintext
Runner
 └─ Monitor.PubSub → collects & writes scores to storage.csv
Engine
 ├─ DataObjects ── Base & EventData
 ├─ Spare        ── Corruption checks, helpers
 ├─ PreProcessors ── AudioPre & VideoPre
 ├─ Processors    ── Audio, Image, Video → fetch analysis & set context
 ├─ LLMHandler    ── MultiSetLLMScoring (Single & Bulk prompts)
 ├─ VectorHandler ── load CategoryBags + VectorScoring
 └─ Launcher      ── TaskPerformer + LauncherMain + StreamLitLauncher
```

- **Data Flow** 
  1. `Engine/Launcher/LauncherMain.main()` builds `EventData` via `FileSegregator` & `TaskPerformer`.  
  2. `TaskPerformer._process_data()` calls processors & corruption checks.  
  3. `_get_scores()` invokes LLM & vector scoring → publishes to `Runner/Monitor/PubSub`.  
  4. `process_datasets()` in [`LauncherMain`](Engine/Launcher/LauncherMain.py) merges results.  
  5. Streamlit UI displays bar charts & progress bars.

- **Storage**  
  - `storage.csv` tracks per‐serial and overall scores (LLM vs Vector).
