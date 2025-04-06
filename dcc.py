# Basic FAQ Bot in Python

# Dictionary containing FAQ questions and answers
faq_dict = {
    "What is your name?": "I am a chatbot created to assist you with FAQs.",
    "How do I contact support?": "You can contact support via email at support@example.com.",
    "What are your operating hours?": "We operate from 9 AM to 5 PM, Monday to Friday.",
    "Where are you located?": "We are located in San Francisco, California.",
    "What services do you offer?": "We offer a variety of services, including tech support and customer service."
}

def faq_bot():
    print("Welcome to the FAQ Bot! Ask me anything.")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Check if the user's input matches any FAQ
        response = faq_dict.get(user_input, "Sorry, I don't have an answer to that question.")
        print(f"Bot: {response}\n")

# Start the bot
faq_bot()
