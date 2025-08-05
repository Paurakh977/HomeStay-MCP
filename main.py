
import contextlib
from fastapi import FastAPI
import os
from src.officer import officer_mcp

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(officer_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/officer", officer_mcp.streamable_http_app())



PORT = os.environ.get("PORT", 8080)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
