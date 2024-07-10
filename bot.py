import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage, trim_messages
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
import json

config_file_path = 'static/config.json'

# Open and read the JSON file
with open(config_file_path, 'r') as file:
    config_data = json.load(file)

# Access the Google API Key
GOOGLE_API_Key = config_data['GOOGLE_API_Key']
google_llm = ChatGoogleGenerativeAI(model = 'gemini-pro',google_api_key = GOOGLE_API_Key)

#creating a bot class
class BOT:
    # intializing
    def __init__(self, user_input):
        self.user_input = user_input
        self.trimmer = trim_messages(
            max_tokens= 512,
            strategy='last',
            token_counter= google_llm,
            include_system=True,
            allow_partial=False,
            start_on='human'
        )
    def get_session_history(self, session, session_id):
        if session_id not in session:
            session[session_id] = ChatMessageHistory()
        return session[session_id]

    # def generate_output(self, session, session_id):
    def generate_output(self):
        prompt_template = PromptTemplate(
            input_vairalbe = ['user_input'],
            template = 'You are a helpful assistant. Answer all {user_input} to the best of your ability'
        )

        self.chain = prompt_template | google_llm
            # RunnablePassthrough.assign(messages = itemgetter('user_input') | self.trimmer)
        
        # self.chain = (
        #     RunnablePassthrough.assign(messages = itemgetter('user_input') | self.trimmer)
        #     | prompt_template
        #     | google_llm
        # )
            
        # session_history = self.get_session_history(session, session_id)
        # self.with_message_history = RunnableWithMessageHistory(
        #     self.chain, 
        #     lambda *_:session_history,
        #     input_messages_key="user_input",
        # )
        # self.config = {"configurable": {"session_id":session_id}}
        self.query = self.user_input

        self.result = self.chain.invoke(
            self.query,
            # {"user_input" : HumanMessage(content = self.query)},
            # config=self.config,
        )
        # self.result = self.with_message_history.invoke(
        #     # self.query,
        #     {"user_input": [HumanMessage(content=self.query)]},
        #     config = self.config,
        # )
        return self.result.content

