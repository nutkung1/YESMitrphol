from pathlib import Path
import streamlit as st
import torch
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from transformers import (
    AutoTokenizer,
    GenerationConfig,
    TextStreamer,
    pipeline,
    AutoModelForCausalLM,
)

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
model_name_or_path = "TheBloke/Nous-Hermes-13B-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
generation_config = GenerationConfig.from_pretrained(model_name_or_path)
streamer = TextStreamer(
    tokenizer, skip_prompt=True, skip_special_tokens=True, use_multiprocessing=False
)
model = AutoGPTQForCausalLM.from_quantized(
    model_name_or_path,
    model_basename="model",
    use_safetensors=True,
    trust_remote_code=True,
    device=DEVICE,
    use_triton=False,
    quantize_config=None,
)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=2048,
    temperature=0,
    top_p=0.95,
    repetition_penalty=1.15,
    generation_config=generation_config,
    streamer=streamer,
    batch_size=1,
)
llm = HuggingFacePipeline(pipeline=pipe)
embeddings = HuggingFaceEmbeddings(
    model_name="embaas/sentence-transformers-multilingual-e5-base",
    model_kwargs={"device": DEVICE},
)

DEFAULT_TEMPLATE = """
### Instruction: You're a advisor of a company that need to give the company information to customers. Use only the chat history and the following information
{context}
to answer in a helpful manner to the question. IF you don't know the answer ~ say that you don't know.
Keep your replies short, compassionate and informative.
{chat_history}
### input: {question}
### Response:
""".strip()


class Chatbot:
    def __init__(
        self,
        text_pipeline: HuggingFacePipeline,
        embeddings: HuggingFaceEmbeddings,
        documents_dir: Path,
        prompt_template: str = DEFAULT_TEMPLATE,
        verbose: bool = False,
    ):
        prompt = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=prompt_template,
        )
        self.chain = self._create_chain(text_pipeline, prompt, verbose)
        self.db = self._embed_data(documents_dir, embeddings)

    def _create_chain(
        self,
        text_pipeline: HuggingFacePipeline,
        prompt: PromptTemplate,
        verbose: bool = False,
    ):
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            human_prefix="### Input",
            ai_prefix="### Response",
            input_key="question",
            output_key="output_text",
            return_messages=False,
        )
        return load_qa_chain(
            text_pipeline,
            chain_type="stuff",
            prompt=prompt,
            memory=memory,
            verbose=verbose,
        )

    def _embed_data(
        self, documents_dir: Path, embeddings: HuggingFaceEmbeddings
    ) -> Chroma:
        loader = DirectoryLoader(documents_dir, glob="**/*txt")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return Chroma.from_documents(texts, embeddings)

    def __call__(self, user_input: str) -> str:
        docs = self.db.similarity_search(user_input)
        return self.chain.run({"input_documents": docs, "question": user_input})


chatbot = Chatbot(llm, embeddings, ".data1/")

st.title("Farmer Bot")
