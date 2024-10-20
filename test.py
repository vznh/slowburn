from utils.utils import detect_framework_or_language

framework = detect_framework_or_language("python3 ./test/main.py")
print(framework)
