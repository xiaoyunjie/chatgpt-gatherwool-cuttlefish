#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/29
# @Author  : browser
# @Software: PyCharm
# @File    : chatgpt_api.py

import openai

# Set your API key
openai.api_key = "xxxxxxxxxxxx"

name: str = '招聘感想'

prompt = f'以 {name} 为题，写一篇800字的文章'

# Use the ChatGPT model to generate a response to a prompt
response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=4000,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Print the response
# print(response.text)
print(response.choices[0].text)
