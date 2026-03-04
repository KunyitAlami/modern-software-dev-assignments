def success(data):
    return {"ok": True, "data": data}


def error(code: str, message: str):
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
