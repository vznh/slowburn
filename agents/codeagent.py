from uagents import Agent, Context, Protocol, Model
import random
from uagents import Field
from ai_engine import UAgentResponse, UAgentResponseType
import sys
from dotenv import load_dotenv
import os

load_dotenv()

codeagent = Agent(name="Baka", seed=os.getenv("SEED_ADDRESS"))

@codeagent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Agent {codeagent.name} starting and i am at {codeagent.address}")

if __name__ == "__main__":
    codeagent.run()
