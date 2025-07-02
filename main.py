import requests
import json

url = 'https://api.dify.ai/v1'

headers = {
'Authorization': 'Bearer app-wybS2n6y2Oi4G8yz8bmlRPCH',
'Content-Type': 'application/json',
}


query = input("ask anything! \n")

data = {
    "inputs": {"text": "is this apple?"}, # the context
    "query": query, # the actual question
    "response_mode": "streaming",
    "conversation_id": "", # left blank so server can generate new ones
    "user": "test_user"
}

response = requests.post(
    url + '/chat-messages',
    headers=headers,
    json=data,           # a bit cleaner than data=json.dumps(...)
    stream=True          # <-- crucial! makes chunck responce in realtime
)


if response.status_code != 200:
    print("Error:", response.text)

else:
    full_answer = ""
    # chunk_size=1 will yield each byte/line ASAP
    for line in response.iter_lines(chunk_size=1, decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue

        chunk = json.loads(line[len("data:"):].strip())
        if chunk.get("event") == "message":
            piece = chunk["answer"]
            print(piece, end="", flush=True)
            full_answer += piece

    print()  # newline after stream ends

    # req = response.request

    # print("=== REQUEST ===")
    # print(f"{req.method} {req.url} HTTP/1.1")
    # for k, v in req.headers.items():
    #     print(f"{k}: {v}")
    # print()
    # # body comes through as bytes (or a str); decode if you like
    # body = req.body
    # if isinstance(body, (bytes, bytearray)):
    #     body = body.decode('utf-8')
    # print(body)
    # print("=== END REQUEST ===")