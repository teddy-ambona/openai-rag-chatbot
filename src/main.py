import tiktoken
import pandas as pd

df = pd.read_csv("laser_eye_surgery_complications.csv")


# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

df["token"] = df["text"].apply(enc.encode)

x = 1
# assert enc.decode(enc.encode("hello world")) == "hello world"
