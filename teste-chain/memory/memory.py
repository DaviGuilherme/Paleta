def save_conversation_buffer_memory(conversationBufferMemory, name):
    extracted_messages = conversationBufferMemory.chat_memory.messages
    import json
    from langchain.schema import messages_to_dict
    with open(f'./memory/{name}.json', 'w') as f:
        json.dump(messages_to_dict(extracted_messages), f)

def load_conversation_buffer_memory(name, return_messages=False):
    import json
    from langchain.schema import messages_from_dict
    from langchain.memory import ChatMessageHistory, ConversationBufferMemory
    if not verify_file_exists(f'./memory/{name}.json'):
        return ConversationBufferMemory(memory_key="chat_history", return_messages=return_messages)
    with open(f'./memory/{name}.json', 'r') as f:
        messages = json.load(f)
    chat_message_history = ChatMessageHistory(messages=messages_from_dict(messages))
    return ConversationBufferMemory(chat_memory=chat_message_history, memory_key="chat_history", return_messages=return_messages)

def verify_file_exists(filename):
    import os

    path_to_file = os.path.join(os.getcwd(), filename)
    return os.path.isfile(path_to_file)