import dotenv

dotenv.load_dotenv()

from src.crew import PublisherCrew  # noqa: E402

if __name__ == "__main__":
    crew = PublisherCrew()
    result = crew.kickoff()
    print(result)
