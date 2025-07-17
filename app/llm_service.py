from fastapi import FastAPI
from pydantic import BaseModel
from app.llm.backend.llm_strategy import analyze_strategy_llm

app = FastAPI()

class AnalyzeStrategyRequest(BaseModel):
    move_history: str

class AnalyzeStrategyResponse(BaseModel):
    analysis: str

@app.post("/analyze-strategy", response_model=AnalyzeStrategyResponse)
def analyze_strategy(req: AnalyzeStrategyRequest):
    result = analyze_strategy_llm(req.move_history)
    return AnalyzeStrategyResponse(analysis=result)
