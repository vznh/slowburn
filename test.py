from utils.utils import detect_framework_or_language

if __name__ == "__main__":
    framework = detect_framework_or_language("test/test-react-app")
    print(framework)
