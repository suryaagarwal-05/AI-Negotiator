# main.py
from src.app import run_negotiator

async def main(csv_file_path):
    print("Hello from ai-negotiator!")
    return await run_negotiator(csv_file_path)
