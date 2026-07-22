from webpagesummarize import *
from brochuregenerator import *


def main():
    #print(summarize_website_ollama("https://openai.com"))
    brochure_generator("Hugging Face", "https://huggingface.co/", True)


if __name__ == "__main__":
    main()

