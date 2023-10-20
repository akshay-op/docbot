import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.let_it_rain import rain

def main():
    st.set_page_config(layout="wide", page_title="Chat page")
    st.title("Data Ask Page")
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
                    object_LLMmodel = st.session_state["LLMmodel_object"]
                    response = object_LLMmodel.question(user_input, repo_id=st.session_state["settings"]["repo_id"])
                    st.session_state.past.append(user_input)
                    st.session_state.generated.append(response)

            if st.session_state["generated"]:
        
                    for i in range(len(st.session_state["generated"])-1, -1, -1):
                        question = st.session_state["past"][i]
                        st.markdown(f"<h3 style='text-align: center; color: black;'> ........................................................................</h3>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style='text-align: center; color: black;'> Question:</h4>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style=' color: red;'>  {question}</h4>", unsafe_allow_html=True)
                        chat_message = st.session_state["generated"][i]["output_text"]
                        st.markdown(f"<h4 style='text-align: center; color: black;'> Anwser:</h4>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style=' color: green;'>  {chat_message}</h4>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()