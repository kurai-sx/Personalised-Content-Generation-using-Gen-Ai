import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

client = AzureOpenAI(
    api_key=os.environ["API_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://teamstrawhats.openai.azure.com/"
)



# This will correspond to the custom name you chose for your deployment when you deployed a model.
# Use a gpt-35-turbo-instruct deployment.
deployment_name = "strawhacksproject"



st.set_page_config(
    page_title="Personalised Content Generator",
    page_icon="img_1.png",
)

# st.image("img.png")
st.columns(3)[1].image("img.png")

st.title('Personalised Content Generator')
st.sidebar.subheader("Select the parameter:",divider='rainbow')



# type = st.text_input("Enter the Type")
platform = st.sidebar.selectbox(
    "Select platform:",
    ("Instagram", "Facebook", "LinkedIn", "Twitter"),index=None,
)

output_size = (st.slider("Select the Content Word Count:", 0, 200, 100))


content_type = st.sidebar.radio(
    "Select Content type:",
    ["Post Caption", "Image (Coming Soon!)", "Comment", "Recommendation"],index=None,
)



if (content_type == "Image (Coming Soon!)"):
    st.toast('Image Generation is not Supported Yet!', icon='🚫')
    st.sidebar.error("Can't Generate Image!, Select other Content Type")

goal = st.text_input("Define the goal of the Content:")

context = st.text_input("Define the Context of the for the Content:")



content_level = st.sidebar.radio(
    "Select Content Category",
    ["Creative", "Descriptive", "Logical", "Joyful"],index=None,
)



#load model
def load_model(prompt):
    with st.spinner('Generating the Content...'):
        #model calling
        # response = model.generate_content(prompt)
        result = client.completions.create(
            model=deployment_name,
            prompt=prompt,
            temperature=1,
            max_tokens=350,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )


    if result.choices[0]:
        output = result.choices[0].text
        return output
    else:
        st.error("Sorry, but I think Azure OpenAI didn't want to answer that!")

try:
    if st.button("Generate", type="primary"):
        if goal and context and platform and (content_type != None) and (content_level != None):

            if (content_type != "Image (Coming Soon!)"):

                prompt = "You are a professional in personalised content (content is generation and you can generate any social media content based on the given data." \
                          "generate a "+ str(content_type) + "for a post related to the " + str(context)+" goal of the post is " + str(goal) + " give in only "+ str(output_size)+ " words" \
                        "the "+ str(content_type) + " is going to be used for posting on the platform " + str(platform) + "constraint is give me the content according to the prompt dont give me the content out of the concept. give me only content, dont give explanation and description. give content only in "+ str(output_size) +" words only"


                output = load_model(prompt)

                st.success("Here is Your Generated Content")
                st.toast('Content Generated Successfully')
                st.balloons()
                # st.write("Content")
                container = st.container(border=True)
                output2= content_type+ " in " +str(output_size) + " words."
                container.subheader(output2)
                container.write(output)

            else:
                st.error("Can't Generate Image!, Select other Content Type")
                st.toast('Image Generation is not Supported Yet!', icon='🚫')

        else:
            st.error("Enter Data Completely")
            st.toast('Fill All Values Completely', icon='🚫')

except Exception as e:
    print(e)
    print("Sorry, but Gemini didn't want to answer that!")
    st.error("Sorry, but Model didn't want to answer that!")




footer_html = """<div style='text-align: center;'>
  <p>Developed with ❤️ by Team Straw Hats</p>
</div>"""

st.markdown(footer_html, unsafe_allow_html=True)



