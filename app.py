from flask import Flask , request, render_template, jsonify
import google.generativeai as genai
import os 

app= Flask(__name__)

#setting Api keys 

os.environ["GOOGLE_API_KEY"] = "Your_Api"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-pro")

# Global variables to store conversation history and context
conversation_history = []

# Voice assistance function with enhanced topic management
def voice_assistance(user_input):
    global conversation_history

    # Improved prompt with focus on concise and direct answers
    prompt = f"""
    You are an AI assistant in an engaging conversation with a user. The user just asked the following question:
    '{user_input}'
    Provide a direct and informative answer, focusing on the exact details the user is asking for. Avoid unnecessary elaboration or asking follow-up questions unless essential to the user’s inquiry. Keep the response clear, concise, and to the point. If the topic is complex, briefly summarize the key aspects. Make sure You belong from India so answer should be simple and in friendly manner.
    """

    response = model.generate_content(prompt).text

    # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response



#url or end points 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_voice',methods =['POST'])
def process_voice():
    user_input = request.json.get('user_input')

    response = voice_assistance(user_input)
    return jsonify({'response': response , 'conversation_history': conversation_history})



if __name__=="__main__":
    app.run(debug=True)
