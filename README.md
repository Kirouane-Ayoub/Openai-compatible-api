# OpenAI-Compatible API Example

This project demonstrates how to create a text generation API using Google Gemini as an example. Although Google Gemini already provides an OpenAI-Compatible API, this example is intended to illustrate the implementation of a text generation endpoint and optional streaming functionality. Please note that this example is not perfectly optimized.

For a detailed explanation of this project, check out my [blog post](https://sembosa.netlify.app/other/openai-compatible-api).

## Getting Started

### Clone the Repository

To get started, clone the repository:

```sh
git clone https://github.com/Kirouane-Ayoub/Openai-compatible-api
```

### Install Requirements

Navigate to the project directory and install the required dependencies:

```sh
cd Openai-compatible-api
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the project directory and set your `GEMINI_API_KEY` as follows:

```env
GEMINI_API_KEY=your_api_key_here
```

You can obtain your API key from [Google AI Studio](https://aistudio.google.com).

### Run the Server

Start the server by running:

```sh
python app.py
```

### Running the Client

#### With Streaming

Use the following code to run the client with streaming enabled:

```py
from openai import OpenAI
import sys

client = OpenAI(
    api_key="fake-api-key",
    base_url="http://localhost:8000"  
)

res = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=True,
)

for chunk in res:
    sys.stdout.write(chunk.choices[0].delta.content or "")
    sys.stdout.flush()
```

#### Without Streaming

Use the following code to run the client without streaming:

```py
from openai import OpenAI

client = OpenAI(
    api_key="fake-api-key",
    base_url="http://localhost:8000"  
)

res = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=False,
)

print(res.choices[0].message.content)
```
