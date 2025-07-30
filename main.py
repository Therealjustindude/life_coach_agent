from app.agent import LifeCoachAgent

def run():
	coach = LifeCoachAgent()
	print("Ask your life coach anything. Type 'quit' to exit.")
	while True:
		q = input("You: ")
		if q.lower() in ["quit", "exit"]:
			break
		print("\nCoach:", coach.get_advice(q), "\n")

if __name__ == "__main__":
	run()