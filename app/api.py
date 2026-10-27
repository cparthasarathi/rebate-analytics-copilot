from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.security import detect_sensitive_markers, tokenize_identifier, validate_readonly_sql, validate_text

app = FastAPI(title=settings.app_name, version="0.1.0")
APPROVED_RELATIONS = {
    "GOLD.FACT_REBATE_TRANSACTION",
    "GOLD.DIM_PRODUCT",
    "GOLD.DIM_CONTRACT",
    "GOLD.DIM_CUSTOMER_PAYER",
    "GOLD.DIM_PERIOD",
}


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class TokenizeRequest(BaseModel):
    identifier: str = Field(min_length=1, max_length=256)


class SqlGuardRequest(BaseModel):
    sql: str = Field(min_length=1, max_length=10000)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.app_env}


@app.post("/demo/validate-question")
def validate_question(request: QuestionRequest):
    try:
        question = validate_text(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if detect_sensitive_markers(question):
        raise HTTPException(status_code=422, detail="Potential sensitive identifier detected; use approved aggregate commercial data only.")
    return {"accepted": True, "message": "Passed basic demo checks; this is not complete DLP."}


@app.post("/demo/tokenize")
def tokenize(request: TokenizeRequest):
    try:
        token = tokenize_identifier(request.identifier, settings.tokenization_hmac_key)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"token": token}


@app.post("/demo/validate-sql")
def validate_sql(request: SqlGuardRequest):
    try:
        sql = validate_readonly_sql(request.sql, APPROVED_RELATIONS)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"accepted": True, "normalized_sql": sql, "executed": False}
