import dotenv

dotenv.load_dotenv()

from src.sdk.latex_publisher_sdk import LatexPublisherSDK  # noqa: E402

if __name__ == "__main__":
    sdk = LatexPublisherSDK()
    result = sdk.run()
    print(result)
