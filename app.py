from fastapi import FastAPI, UploadFile, Request
import uvicorn
from script import *
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload_image")
async def upload_image(file: UploadFile, request: Request):
    data = await file.read()
    nparr = np.frombuffer(data, np.uint8)
    colorize_image(nparr)

    file_path = "colorized_image.png"

    # move file to static folder
    os.rename("colorized_image.png", "static/colorized_image.png")

    download_link = "/static/colorized_image.png"
    return HTMLResponse(
        f"""
        <html>
            <body>
                <h1>Image uploaded and processed successfully!</h1>
                <p>Download the processed image: <a href="{download_link}" download>Download</a></p>
            </body>
        </html>
    """
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
