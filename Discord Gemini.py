import discord
from discord.ext import commands
from google import genai
from google.genai import types
import os
import sys
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
discord_token = "PUT YOUR DISCORD TOKEN HERE"
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",
    google_api_key="PUT YOUR GEMINI API KEY HERE",
)
prompt = ChatPromptTemplate.from_messages(
    [
        "You are a chat Assistant. You provide helpful replies to human queries. Sometime your prompt may seem unrelated to the previous prompts. If this happens just answer it anyways. Your response may contain personal opinion based on evidence if needed. Do not include the history or the humans prompt in your response. Also please do not repeat your response after saying it once. Limit your responses to 200 words. The chat history upto this point is provided below:"
        "{chat_history}"
        "Answer the following human query ."
        "Human: {input}"
        "Assistant:"
    ]
)

history = InMemoryChatMessageHistory()


def get_history():
    return history


chain = prompt | llm | StrOutputParser()

wrapped_chain = RunnableWithMessageHistory(
    chain,
    get_history,
    history_messages_key="chat_history",
)

client = commands.Bot(command_prefix='!', self_bot=True)

@client.event
async def on_message(message):
    if "Hey Gemini" in message.content:
        await message.channel.send(wrapped_chain.invoke({"input": message.content}))

client.run(discord_token)

