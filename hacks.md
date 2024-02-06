curl -X POST "127.0.0.1:11434/api/chat" \
     -H "Content-Type: text/event-stream" \
     -H "Accept: */*" \
     -H "Connection: keep-alive" \
     -H "Accept-Encoding: gzip, deflate" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15" \
     -H "Accept-Language: en-GB,en;q=0.9" \
     -H "Sec-Fetch-Site: same-origin" \
     -H "Sec-Fetch-Mode: cors" \
     -H "Sec-Fetch-Dest: empty" \
     -d '{"model":"mixtral:latest","messages":[{"role":"user","content":"Tell me a random fun fact about the Roman Empire"},{"role":"user","content":"hi"},{"role":"assistant","content":""}],"options":{}}'


curl -v -X POST "127.0.0.1:11434/api/chat" \
     -H "Content-Type: text/event-stream" \
     -H "Accept: */*" \
     -H "Connection: keep-alive" \
     -H "Accept-Encoding: gzip, deflate" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15" \
     -H "Accept-Language: en-GB,en;q=0.9" \
     -H "Sec-Fetch-Site: same-origin" \
     -H "Sec-Fetch-Mode: cors" \
     -H "Sec-Fetch-Dest: empty" \
     -d '{"model":"mixtral:latest","messages":[{"role":"user","content":"Tell me a random fun fact about the Roman Empire"},{"role":"user","content":"hi"},{"role":"assistant","content":""}],"options":{}}'


launch 
fake_ollama % uvicorn fast_app:app --reload --port 11434 

output fast api

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:47.594749Z", "message": {"role": "assistant", "content": "I"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:47.694498Z", "message": {"role": "assistant", "content": "need"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:47.794312Z", "message": {"role": "assistant", "content": "information"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:47.895279Z", "message": {"role": "assistant", "content": "on"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:47.995157Z", "message": {"role": "assistant", "content": "a"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:48.096829Z", "message": {"role": "assistant", "content": "specific"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:48.198014Z", "message": {"role": "assistant", "content": "topic,"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:48.299585Z", "message": {"role": "assistant", "content": "feel"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:48.400117Z", "message": {"role": "assistant", "content": "free"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:48.500840Z", "message": {"role": "assistant", "content": "to"}, "done": false}

data: {"model": "mixtral:latest", "created_at": "2024-02-06T16:53:48.602705Z", "message": {"role": "assistant", "content": "ask!"}, "done": true, "total_duration": 1234567, "load_duration": 12345, "prompt_eval_count": 50, "prompt_eval_duration": 54321, "eval_count": 150, "eval_duration": 98765}



output true ollama
--
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.290994Z","message":{"role":"assistant","content":"."},"done":false}
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.319148Z","message":{"role":"assistant","content":" How"},"done":false}
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.349612Z","message":{"role":"assistant","content":" cool"},"done":false}
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.378559Z","message":{"role":"assistant","content":" is"},"done":false}
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.406734Z","message":{"role":"assistant","content":" that"},"done":false}
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.434575Z","message":{"role":"assistant","content":"?"},"done":false}
{"model":"mixtral:latest","created_at":"2024-02-06T16:55:29.463568Z","message":{"role":"assistant","content":""},"done":true,"total_duration":44653167041,"load_duration":38404189875,"prompt_eval_count":29,"prompt_eval_duration":533928000,"eval_count":198,"eval_duration":5711725000}