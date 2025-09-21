from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="Password Manager")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return HTMLResponse("""
                        <html>
                            <head>
                                <title>Password Manager</title>
                            </head>
                            <body>
                                <h1>Password Manager</h1>
                                <p>Server is running!</p>
                            </body>
                        </html>
                        """)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
