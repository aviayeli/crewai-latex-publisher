import dotenv

dotenv.load_dotenv()

from src.sdk.latex_publisher_sdk import LatexPublisherSDK  # noqa: E402

if __name__ == "__main__":
    topic = input(
        "Enter the topic for the agents to research and write about: "
    ).strip()
    sdk = LatexPublisherSDK()
    result = sdk.run(topic=topic)
    print(result)
