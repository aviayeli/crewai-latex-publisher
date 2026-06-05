import dotenv

dotenv.load_dotenv()

from src.sdk.latex_publisher_sdk import LatexPublisherSDK  # noqa: E402
from src.topics import select_topic  # noqa: E402

if __name__ == "__main__":
    selected = select_topic()
    sdk = LatexPublisherSDK()
    result = sdk.run(topic=selected.title, research_focus=selected.research_focus)
    print(result)
