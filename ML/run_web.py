"""
AgriFertilizer AI - Web Application Launcher
Runs FastAPI backend with Uvicorn and launches the web interface.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import uvicorn

def main():
    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}"
    
    print("=" * 65)
    print(">> AGRIFERTILIZER AI - WEB SERVER STARTING")
    print("=" * 65)
    print(f"Local URL:      {url}")
    print(f"API Docs:       {url}/docs")
    print("Model Bundle:   fertilizer_requirement_model_bundle.joblib")
    print("Authors:        Sai Snehith (2520090149) & Harshith Reddy (2520090114)")
    print("=" * 65)
    
    uvicorn.run("app:app", host=host, port=port, log_level="info", reload=False)

if __name__ == "__main__":
    main()
