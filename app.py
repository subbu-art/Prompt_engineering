from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
import streamlit as st
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.prompts import example_selector
import os
from langchain_core.prompts import FewShotPromptTemplate

os.environ["OPENAI_API_KEY"] = 'your_api_key'

llm = OpenAI(model_name = 'gpt-3.5-turbo-instruct')





def get_response(user_query,task_type,age_type,numberOfWords):
    examples = [
        {
            "query": "What is a mobile?",
            "answer": "A mobile is a magical device that fits in your pocket, like a mini-enchanted playground. It has games, videos, and talking pictures, but be careful, it can turn grown-ups into screen-time monsters too!"
        }, {
            "query": "What are your dreams?",
            "answer": "My dreams are like colorful adventures, where I become a superhero and save the day! I dream of giggles, ice cream parties, and having a pet dragon named Sparkles.."
        }, {
            "query": " What are your ambitions?",
            "answer": "I want to be a super funny comedian, spreading laughter everywhere I go! I also want to be a master cookie baker and a professional blanket fort builder. Being mischievous and sweet is just my bonus superpower!"
        }, {
            "query": "What happens when you get sick?",
            "answer": "When I get sick, it's like a sneaky monster visits. I feel tired, sniffly, and need lots of cuddles. But don't worry, with medicine, rest, and love, I bounce back to being a mischievous sweetheart!"
        }, {
            "query": "WHow much do you love your dad?",
            "answer": "Oh, I love my dad to the moon and back, with sprinkles and unicorns on top! He's my superhero, my partner in silly adventures, and the one who gives the best tickles and hugs!"
        }, {
            "query": "Tell me about your friend?",
            "answer": "My friend is like a sunshine rainbow! We laugh, play, and have magical parties together. They always listen, share their toys, and make me feel special. Friendship is the best adventure!"
        }, {
            "query": "What math means to you?",
            "answer": "Math is like a puzzle game, full of numbers and shapes. It helps me count my toys, build towers, and share treats equally. It's fun and makes my brain sparkle!"
        }, {
            "query": "What is your fear?",
            "answer": "Sometimes I'm scared of thunderstorms and monsters under my bed. But with my teddy bear by my side and lots of cuddles, I feel safe and brave again!"
        }
    ]


    example_template = '''
    Questions = {query},
    Answer = {answer}
    '''

    example_prompt = PromptTemplate(
        input_variables=['query','answer'],
        template = example_template
    )

    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )
    prefix = """You are a {age_option}, generate a {task_type} in {numberOfWords} words. : 
    Here are some examples: 
    """


    suffix = """
    Question: {userInput}
    Response: """

    new_prompt_template = FewShotPromptTemplate(
        example_selector = example_selector,
        example_prompt = example_prompt,
        prefix = prefix,
        suffix = suffix,
        input_variables = ['userInput', 'age_option','task_type','numberOfWords'],
        example_separator = '\n\n'
    )

    response = llm(new_prompt_template.format(userInput=user_query,age_option =age_type,task_type= task_type, numberOfWords = str(numberOfWords)))
    return response

st.set_page_config(page_title='Marketing Campain', page_icon=':robot:',layout = 'centered', initial_sidebar_state = 'collapsed')
st.header('MArketing Campaign Survey')

user_query = st.text_area('Enter Text', height=225)

task_type = st.selectbox('Please select the task',
                         ('Write a sales copy', 'Create a tweet', 'Write a product description'),
key =1)

age_type = st.selectbox("please select the age type", ('Senior Citizen', 'Teenager', 'Kid'), key = 2)

numberOfWords= st.slider('Words limit', 1, 200, 25)

submit = st.button("generate")
if submit:
    st.write(get_response(user_query,task_type,age_type,numberOfWords))