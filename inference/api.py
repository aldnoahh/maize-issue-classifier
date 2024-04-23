from fastapi import FastAPI, UploadFile, File, HTTPException
#from typing import List
#from typing import Union, Optional
from pydantic import BaseModel
from predict import onnx_inference as inf
import uvicorn
import json

app = FastAPI()
WORKERS = 4

class INFER(BaseModel):
	image: str


@app.post("/infer")
async def inference(infer: INFER):
	try:
		ret = inf(infer.image)
		if ret:
			return json.dumps({"success": True,"status_code": 200,"message": f"{ret}"})
		else:
			return json.dumps({"success": False,"status_code": 400,"message": "Unable to Recognize"})
		
	except Exception as e:
		return json.dumps({"success": False, "status_code": 404, "message": f"Error in inference: {e}"})


if __name__ == "__main__":
	uvicorn.run("api:app", port=8000, host="0.0.0.0", workers=1)