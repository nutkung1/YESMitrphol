import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS, Chroma
from langchain.memory import ConversationBufferMemory
from pythainlp.translate import Translate
from translate import Translator
# from googletrans import Translator

# translator = Translator()

#load the pdf files from the path
loader = DirectoryLoader('/Users/suchanatratanarueangrong/Mitrphol/streamlit/data1/',glob="*.txt")
documents = loader.load()

#split text into chunks
text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
text_chunks = text_splitter.split_documents(documents)

#create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                   model_kwargs={'device':"cpu"})

#vectorstore
vector_store = Chroma.from_documents(text_chunks,embeddings)

#create llm
llm = CTransformers(model="/Users/suchanatratanarueangrong/Mitrphol/streamlit/llama-2-7b-chat.ggmlv3.q6_K.bin",model_type="llama",
                    config={'max_new_tokens':256,'temperature':0.01,'repetition_penalty': 1.1})

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(llm=llm,chain_type='stuff',
                                              retriever=vector_store.as_retriever(search_kwargs={"k":3}),
                                              memory=memory)

st.title("🧑‍🌾 Mitr Phol Bot 👩‍🌾")

def language_selection_button(label, language):
  """Creates a language selection button."""
  if st.button(label):
    st.session_state['language'] = language
# Set the initial language of the app
if 'history' not in st.session_state:
    st.session_state['language'] = 'None'
# Create a language selection button for English
language_selection_button('ภาษาอังกฤษ', 'en')
# Create a language selection button for Spanish
language_selection_button('ภาษาไทย', 'th')
language_selection_button('คำเตือน', 'warn')
language_selection_button('ข้อมูลไร่ของคุณ', 'pop')
# new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Please Select The Language</p>'
# st.markdown(new_title, unsafe_allow_html=True)
# Get the current language of the app
language = st.session_state['language']
# Display the current language of the app
st.write(f'Current language: {language}')
# prompt = "คุณควรปลูกถั่วในไร่ที่1และไร่ที่2ของคุณไม่ต้องทำอะไร"
# st.session_state['generated'].append(output)
def conversation_chat(query):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]
        # st.session_state['generated'] = ["คุณควรปลูกถั่วในไร่ที่1และไร่ที่2ของคุณไม่ต้องทำอะไรและไร่คุณจะมีใบที่สมบูรณ์แบบ"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your problem", key='input')
            submit_button = st.form_submit_button(label='Send')
        if submit_button and user_input:
            if language == 'en':
                output = conversation_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
                st.session_state['language'] = 'en'
            elif language == 'th':
                output = conversation_chat(user_input)
                th2en = Translator(to_lang='th')
                th2en_output = th2en.translate(output)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(th2en_output)
                st.session_state['language'] = 'th'
            elif language == 'None':
                new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Please Select The Language</p>'
                st.markdown(new_title, unsafe_allow_html=True)
            elif language == 'pop':
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append('ผลผลิตต่อไร่โดยประมาณของพื้นที่คุณคือ10ตัน/ไร่ และมีcarbon creditประมาณ2ตันคาร์บอน รายได้ของไร่คุณจะตกที่ประมาณ2000บาท/ตันอ้อย')
            elif language == 'warn':
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append('แจ้งเตือน ตอนนี้ในไร่ของคุณมีการปล่อยก๊าซเรือนกระจกมากเกินข้อกำหนดแล้ว ดังนั้นเราจึงมีวิธีที่จะช่วยลดการปล่อยก๊าซเรือนกระจกให้กลับมาเป็นปกติ โดยวิธีแรกคือการนำปุ๋ยละลายช้ามาใช้แทนปุ๋ยธรรมดา รวมถึงการนำพลังงานสะอาดเช่น โซล่าเซลล์ มาใช้แทน รวมถึงการปลูกพืชตระกูลถั่วเพื่อเพิ่มไนโตรเจนในดิน')
                
    if 'generated' in st.session_state and st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                if i < len(st.session_state['past']) and i < len(st.session_state['generated']):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")


# Initialize session state
initialize_session_state()
# Display chat history
display_chat_history()