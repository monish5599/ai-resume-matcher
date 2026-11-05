
import ollama

print("Testing Ollama Python connection...")

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly Hello"
        }
    ],
    stream=False
)

print("\nComplete response:")
print(response)

print("\nGenerated text:")
print(repr(response.message.content))
