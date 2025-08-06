"""
CLI Test Runner for LifeCoachAgent.
This script is for local, interactive testing only.
The production service runs via FastAPI in server.py.
"""
from app.agent.life_coach_agent import LifeCoachAgent
from app.models.openai_model import OpenAIModel

model = OpenAIModel()

def run():
	coach = LifeCoachAgent(model)
	print("Ask your life coach anything. Type 'quit' to exit.")
	while True:
		q = input("You: ")
		if q.lower() in ["quit", "exit"]:
			break
		print("\nCoach:", coach.chat(q), "\n")

if __name__ == "__main__":
	run()