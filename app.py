import streamlit as st
from hugchat import hugchat
from hugchat.login import Login




# App title
st.set_page_config(page_title=" UTY CORPORATION")

col1, col2 = st.columns([0.5, 3])
col2.markdown("#### PHOENIX - AMAZON LISTING SUPPORT & CHAT 💬")
col1.image("./logo/phoenix.png", width=100)

hf_email = st.secrets['EMAIL']
hf_pass = st.secrets['PASS']

st.sidebar.image("./logo/UTY_logo.png", width=250)


st.sidebar.markdown(""" ___Please follow the format if you want to make the listing___""")

st.sidebar.code("""Product: <name of product>; 
Key: <important list of keys>; 
CUSTOMERS: <target customers>
""",language="html")

st.sidebar.markdown("""___Example:___""")
st.sidebar.code("""PRODUCT: Coconut Milk Tea; 
KEYS: Vietnamese, fresh, no added sugar; 
CUSTOMERS: young kids, gym members""",language="html")

def create_prompt(input_user:str) -> str:
    if ("product" not in input_user.lower())|("key" not in input_user.lower())|(input_user[0:8].lower()!="product:"):
        prompt = input_user
    else:
        product_name = input_user.lower().split("product:")[1].split("keys:")[0]
        keys = input_user.lower().split("keys:")[1].split("customers:")[0]
        customers = input_user.lower().split("customers:")[1]
        
        prompt=f"""
            You are doing the role of a Amazon Product Listing expert. 
                    Giving a product with {product_name} with some important key: {keys}, 
                    write a whole LISTING product for me to sale in Amazon US. 

                    The listing MUST push the brand "AMAZIN CHOICES" in the first place in title, to make the branding.
        

                    There are rules you MUST follow:
                    - Title does not contain symbols or emojis
                    - Title contains around 150 characters
                    - Description has greater than 5 and less than 10 bullet points
                    - Description has greater than 150 characters in each bullet point
                    - MUST USE the icons, emojis, and symbols at the begin of each bullet point.
                    - First letter of bullet points is capitalized
                    - Bullet points are not in all caps or contain icons
                    - 1000+ characters in description or A+ content
                    - NOT using words or term phrase which I need to make verify. Example: Guaranteed, Approved, Verified, ...
                    

                    The response in format:

                    ## Title: 
                    Appropriate title of product using best keyword list, format as a header
                    ## Description: 
                        - description of the product, in bullet points, contains best keyword list to increase highest possibility of keyword search in amazon
                        - description MUST adapt style of sentenses to target to the group of customers on amazon: {customers}.
                    The return will be on MARKDOWN format.
                    """
    return prompt
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Tell me what you want to sell?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# User-provided prompt
if input_user := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": input_user})
    with st.chat_message("user"):
        st.write(input_user)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt = create_prompt(input_user)
            response = generate_response(prompt, hf_email, hf_pass) 
            st.markdown(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)