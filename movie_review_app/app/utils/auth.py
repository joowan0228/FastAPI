from fastapi import Depends

async def get_current_user():
    # 더미 사용자 객체 (실제 구현에서는 JWT 등 사용)
    class DummyUser:
        id = 1
    return DummyUser()
