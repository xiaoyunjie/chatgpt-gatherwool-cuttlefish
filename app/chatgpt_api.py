#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/29
# @Author  : browser
# @Software: PyCharm
# @File    : chatgpt_api.py

import openai

# Set your API key
openai.api_key = "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"

# Use the ChatGPT model to generate a response to a prompt
response = openai.Completion.create(
    model="text-davinci-003",
    prompt="告诫人们居安思危的诗句",
    max_tokens=4000,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Print the response
# print(response.text)
print(response.choices[0].text)
