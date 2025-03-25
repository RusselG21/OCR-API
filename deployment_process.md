# Deploying FastAPI as a Windows Service with NSSM

## **1. Download and Extract NSSM**

1. Download NSSM from [https://nssm.cc/download](https://nssm.cc/download).
2. Extract the downloaded ZIP file.
3. Navigate to the correct subfolder:
   - **For 64-bit Windows**: Open `win64\`
   - **For 32-bit Windows**: Open `win32\`
4. Locate `nssm.exe` inside the folder.

## **2. Move NSSM to a Permanent Location (Optional, but Recommended)**

To make NSSM accessible from anywhere in PowerShell:

1. Copy `nssm.exe` from the extracted folder.
2. Paste it into `C:\Windows\System32\`.

## **3. Install Python and Set Up a Virtual Environment**

Ensure Python is installed on your system. If not, download it from [Python's official site](https://www.python.org/downloads/).

Then, set up a virtual environment in your project directory:

```powershell
cd C:\path\to\your\project
python -m venv venv
venv\Scripts\activate
```

## **4. Install Dependencies**

```powershell
pip install -r requirements.txt
```

## **5. Run FastAPI Manually for Testing**

Before setting up NSSM, test your application:

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Replace `app.main` with the actual import path of your FastAPI instance.

### **Test the API**

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

If the Swagger UI loads, FastAPI is working!

## **6. Install FastAPI as a Windows Service using NSSM**

Open **PowerShell as Administrator** and run:

```powershell
nssm install FastAPIService
```

A GUI window will appear. Fill in the details:

- **Path**: `C:\path\to\your\project\venv\Scripts\python.exe`
- **Arguments**: `-m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Startup directory**: `C:\path\to\your\project`

Click **"Install service"**.

## **7. Start the FastAPI Service**

Run the following command:

```powershell
nssm start FastAPIService
```

To check if it is running:

```powershell
nssm status FastAPIService
```

## **8. Test the FastAPI Service**

Try accessing FastAPI again:

```
http://127.0.0.1:8000/docs
```

If it loads, the service is running successfully.

## **9. Stop or Remove the Service (If Needed)**

- **Stop the service**:
  ```powershell
  nssm stop FastAPIService
  ```
- **Remove the service**:
  ```powershell
  nssm remove FastAPIService confirm
  ```

## **10. Next Steps**

Once tested on your PC, repeat the same steps on your **Windows Server** for deployment.

---

This guide ensures FastAPI runs as a Windows service, starts automatically, and remains running reliably. 🚀
