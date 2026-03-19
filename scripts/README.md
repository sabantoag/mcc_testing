# SWAG Test Software Setup Instructions

## Shortcut Configuration

**Target field:**

```
%WINDIR%\System32\cmd.exe "/C" C:\Users\<user>\AppData\Local\miniconda3\Scripts\activate.bat C:\Users\<user>\AppData\Local\miniconda3 && "<FILE_PATH>\mcc_testing-0.1\scripts\execute_test.bat"
```

**Open In field:**

```
"<FILE_PATH>"
```

## Batch File
Completes the following operations
- Enters mcc_testing directory (where test code is located)
- Loads virtual environment
- Executes tests with pytest and debugging logging enabled
- Deactivates environment after test completion

---
