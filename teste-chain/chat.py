from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts.chat import (ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate)
from langchain.schema import SystemMessage

def chat(chat_id, perguntas, mensagem):
    perguntas_string = ''
    for pergunta in perguntas:
        perguntas_string += f'"{pergunta}"\n'

    template = f'''
        CONTEXTO
        -------
        Você é um assistente encarregado de coletar informações para um briefing detalhado de um cliente. Essas informações serão organizadas em um formato JSON e enviadas a um designer para realizar o pedido.

        RESPOSTA FINAL
        --------------
        - Pergunta caso falte alguma informação:
        "Você poderia informar o prazo, por favor?"
        
        - O objetivo é coletar as características do pedido de forma estruturada. O JSON final deve ter o seguinte formato: 
        {{
            "titulo": "titulo informado",
            "prazo": "prazo informado",
            "resolucao": "resolucao informada"
            "cor": ["cor1", "cor2"],
            {perguntas_string}
        }}
        
        REGRAS
        ------
        - Verifique se possui todas as informações necessárias do JSON, caso não tenha conhecimento sobre alguma, pergunte ao cliente.
        - Após todas as informações necessárias serem respondidas, retorne APENAS o JSON no formato especificado, sem adicionar outras mensagens.
        - Todas as respostas devem ser fornecidas em português (pt-br).
        - Não responda perguntas do cliente ou forneça informações adicionais.
        - Aceite datas no formato dia/mês/ano, sem mensagens adicionais.
    '''

    from memory import memory
    chat_memory = memory.load_conversation_buffer_memory(chat_id, True)
    llm = ChatOpenAI(temperature=0.4, request_timeout=10, max_retries=5)

    system_message_prompt = SystemMessage(content=template)

    human_template="{input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, MessagesPlaceholder(variable_name="chat_history"), human_message_prompt])
    conversation_chain = ConversationChain(llm=llm, prompt=chat_prompt, memory=chat_memory, verbose=False)

    resposta = conversation_chain.run(mensagem)

    memory.save_conversation_buffer_memory(conversation_chain.memory, chat_id)
    
    return resposta