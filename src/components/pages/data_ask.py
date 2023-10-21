import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import streamlit_scrollable_textbox as stx

def main():
    st.set_page_config(layout="wide", page_title="Chat page")
    st.title("Data Chat Page")
    st.write("Welcome to the Data bot, Chat with the doc here.")

    chatcolumn,  = st.columns(1)
    with chatcolumn:

        # st.markdown("<h1 style='text-align: center'>Chat with the document</h1>", unsafe_allow_html=True)

        if not 'db' in st.session_state:
            st.markdown("<h3 style='text-align: center ; color: red;'>Chat database not found</h3>", unsafe_allow_html=True) 
        else:
            db = st.session_state['db']
            # Initialize session state variables for user input and responses
            if "generated" not in st.session_state:
                    st.session_state["generated"] = []
                
            if "past" not in st.session_state:
                st.session_state["past"] = []

            user_input = st.text_input(label=f"Question",
                                    value="Ask me about the document")
       
            if st.button("ASK"):
                    object_LLMmodel = st.session_state["LLMmodel"]
                    response = object_LLMmodel.question(user_input, repo_id=st.session_state["repoid"])
                    st.session_state.past.append(user_input)
                    st.session_state.generated.append(response)

            if st.session_state["generated"]:
        
                    for i in range(len(st.session_state["generated"])-1, -1, -1):
                        question = st.session_state["past"][i]
                        st.markdown(f"<div div style='text-align: right; background-color: #EFEFEF; padding: 10px; border-radius: 10px;'><h6 >  {question}</h6></div>", unsafe_allow_html=True)
                        chat_message = st.session_state["generated"][i]["output_text"]
                        st.markdown(f"<div style='text-align: left; background-color: #D3E5FA; padding: 10px; border-radius: 10px;'><h6>  {chat_message}</h6></div>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()