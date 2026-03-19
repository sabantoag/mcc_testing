# SWAG Test Software Setup Instructions

## Shortcut Configuration

**Target field:**

```
%WINDIR%\System32\cmd.exe "/C" C:\Users\<user>\AppData\Local\miniconda3\Scripts\activate.bat C:\Users\<user>\AppData\Local\miniconda3 && "<FILE_PATH>\mcc_testing-<release>\scripts\execute_tests.bat"
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


## NOTES:

Need to update batch file to execute appropriate virtual environment and from release directory
