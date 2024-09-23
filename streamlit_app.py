import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import FAISS, Chroma
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
#load the pdf
loader = DirectoryLoader("./data1/", glob="**/*txt")
documents = loader.load()
#split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_chunks = text_splitter.split_documents(documents)

#create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':"cpu"})

#vectorstore
vectors_store = Chroma.from_documents(text_chunks, embeddings)

#create llm
llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens':128, "temperature":0.8})
template = """
### Instruction: You're a advisor of a company that need to give the company information to customers. Use only the chat history and the following information
{context}
to answer in a helpful manner to the question. IF you don't know the answer ~ say that you don't know.
Keep your replies short, compassionate and informative.
{chat_history}
### input: {question}
### Response:
""".strip()
prompt = PromptTemplate(
    input_variables={"context", "question", "chat_history"}, template=template
)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    human_prefix="### Input",
    ai_prefix="### Response",
    output_key="answer",
    return_messages=True,
)

chain = ConversationalRetrievalChain.from_llm(
    llm,
    chain_type="stuff",
    retriever=vectors_store.as_retriever(),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
    return_source_documents=True,
    verbose=True,
)
# question = "What is mitr phol"
# answer = chain(question)
# print(answer.keys())
st.title("👩‍🌾 Farmer Bot")
def conversation_chat(query):
    result=chain({"question" :query,"chat_history":st.session_state['history']})
    st.session_state['history'].append((query,result['answer']))
    return result['answer']

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything"]
    if "past" not in st.session_state:
        st.session_state['past'] = ['Hey!']
def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_input("Question:",placeholder="Ask about your problem", key='input')
            submit_button = st.form_submit_button(label="Send")

            if submit_button and user_input:
                output = conversation_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i],is_user=True,key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state['generated'][i],is_user=False,key=str(i), avatar_style="fun-emoji")
#Initialize session state
initialize_session_state()
#display chat history
display_chat_history()
