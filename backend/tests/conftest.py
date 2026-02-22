import pytest
import os
import asyncio

os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_locks.db"

import sys
if "app.core.config" in sys.modules:
    del sys.modules["app.core.config"]

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    from app.db.database import init_db
    from app.db.seed import seed_database
    
    async def setup():
        await init_db()
        await seed_database()
    
    asyncio.run(setup())
    yield
    
    if os.path.exists("./test_locks.db"):
        os.remove("./test_locks.db")
