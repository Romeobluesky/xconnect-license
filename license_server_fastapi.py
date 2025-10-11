from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import mysql.connector
from datetime import datetime

app = FastAPI(title="Recap Voice License API", version="1.0")

# MySQL 연결 설정
DB_CONFIG = {
    "host": "localhost",
    "user": "xconnect_admin",             # 실제 사용자 계정으로 변경
    "password": "$ujin1436",  # 실제 비밀번호로 변경
    "database": "xconnect_admin" # 실제 DB 이름으로 변경
}

def get_db_connection():
    """MySQL 연결"""
    return mysql.connector.connect(**DB_CONFIG)

@app.post("/check_license")
async def check_license(request: Request):
    """클라이언트 Recap Voice에서 라이선스 검증 요청"""
    try:
        data = await request.json()
        license_no = data.get("license_no")
        line_count = data.get("line_count", 1)

        if not license_no:
            return JSONResponse(content={
                "result": False,
                "message": "Missing parameter: license_no"
            })

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT license_no, contract_end_date, line_limit
            FROM companies
            WHERE license_no = %s
        """, (license_no,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return JSONResponse(content={"result": False, "message": "License not found"})

        today = datetime.now().date()
        expiry = row["contract_end_date"]

        if expiry < today:
            return JSONResponse(content={"result": False, "message": "License expired"})

        if line_count > row["line_limit"]:
            return JSONResponse(content={"result": False, "message": "Exceeded max lines"})

        return JSONResponse(content={
            "result": True,
            "message": "License valid",
            "contract_end_date": str(expiry),
            "line_limit": row["line_limit"]
        })

    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={
            "result": False,
            "message": f"Server error: {str(e)}"
        })

# 헬스체크용 엔드포인트
@app.get("/")
async def health_check():
    return {"status": "ok", "service": "RecapVoice License API"}
