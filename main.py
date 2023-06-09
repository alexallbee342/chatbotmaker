import json
import easygui

class Chatbot:
    def __init__(self, name, responses, default_response):
        self.name = name
        self.responses = responses
        self.default_response = default_response
    
    def get_response(self, user_input):
        for key in self.responses:
            if key.lower() in user_input.lower():
                return self.responses[key]
        return self.default_response

    def add_response(self, user_input, response):
        self.responses[user_input] = response

    def edit_response(self, user_input, new_response):
        if user_input in self.responses:
            self.responses[user_input] = new_response
        else:
            print(f"No response found for '{user_input}'")

    def remove_response(self, user_input):
        if user_input in self.responses:
            del self.responses[user_input]
        else:
            print(f"No response found for '{user_input}'")

    def set_default_response(self, response):
        self.default_response = response

    def save_config(self, filename):
        with open(filename, 'w') as f:
            data = {
                'name': self.name,
                'responses': self.responses,
                'default_response': self.default_response
            }
            json.dump(data, f)

    @classmethod
    def load_config(cls, filename):
        with open(filename) as f:
            data = json.load(f)
            bot = cls(data['name'], data['responses'], data['default_response'])
            return bot

def create_chatbot():
    name = easygui.enterbox("Enter the chatbot name:")
    responses = {}
    default_response = easygui.enterbox("Enter the default response:")
    bot = Chatbot(name, responses, default_response)
    easygui.msgbox("Chatbot created successfully!")
    return bot

def edit_responses(bot):
    while True:
        response_choices = list(bot.responses.keys())
        response_choices.append("[Add New Response]")
        response_choices.append("[Remove Response]")
        response_choices.append("[Back to Main Menu]")
        
        try:
            response_choice = easygui.choicebox(f"Edit chatbot '{bot.name}' responses:", choices=response_choices)
            
            if response_choice == "[Add New Response]":
                user_input = easygui.enterbox("Enter the user input:")
                response = easygui.enterbox("Enter the response:")
                bot.add_response(user_input, response)
            elif response_choice == "[Remove Response]":
                if len(bot.responses) > 0:
                    response_choice = easygui.choicebox("Select a response to remove:", choices=list(bot.responses.keys()))
                    if response_choice:
                        bot.remove_response(response_choice)
                else:
                    easygui.msgbox("No responses to remove.")
            elif response_choice == "[Back to Main Menu]":
                break
            else:
                new_response = easygui.enterbox("Enter the updated response:", default=bot.responses[response_choice])
                bot.edit_response(response_choice, new_response)
        except ValueError as e:
            easygui.msgbox(str(e))

def edit_options(bot):
    choices = ["Edit default response", "Edit specific responses"]
    choice = easygui.buttonbox("Edit Options", choices=choices)

    if choice == "Edit default response":
        response = easygui.enterbox("Enter the updated default response:", default=bot.default_response)
        if response:
            bot.set_default_response(response)
            easygui.msgbox("Default response updated successfully!")
        else:
            easygui.msgbox("Invalid response. Default response not updated.")
    elif choice == "Edit specific responses":
        edit_responses(bot)

def main():
    chatbots = []

    while True:
        choices = ["Create new chatbot", "Edit chatbot", "Save chatbot configuration", "Load chatbot configuration", "Quit"]
        choice = easygui.buttonbox("Chatbot Maker", choices=choices)
        
        if choice == "Create new chatbot":
            bot = create_chatbot()
            chatbots.append(bot)
        elif choice == "Edit chatbot":
            if len(chatbots) > 0:
                chatbot_names = [bot.name for bot in chatbots]
                chatbot_names.append("[Back to Main Menu]")
                chatbot_name = easygui.choicebox("Select a chatbot to edit:", choices=chatbot_names)
                if chatbot_name != "[Back to Main Menu]":
                    for bot in chatbots:
                        if bot.name == chatbot_name:
                            edit_options(bot)
                            break
            else:
                easygui.msgbox("No chatbots available. Please create a chatbot first.")
        elif choice == "Save chatbot configuration":
            if chatbots:
                chatbot_names = [bot.name for bot in chatbots]
                chatbot_names.append("[Back to Main Menu]")
                chatbot_name = easygui.choicebox("Select a chatbot to save configuration:", choices=chatbot_names)
                if chatbot_name != "[Back to Main Menu]":
                    for bot in chatbots:
                        if bot.name == chatbot_name:
                            filename = easygui.enterbox("Enter the filename to save configuration:")
                            bot.save_config(filename)
                            easygui.msgbox("Chatbot configuration saved successfully!")
                            break
            else:
                easygui.msgbox("No chatbots available. Please create a chatbot first.")
        elif choice == "Load chatbot configuration":
            filename = easygui.enterbox("Enter the filename to load chatbot configuration:")
            try:
                bot = Chatbot.load_config(filename)
                chatbots.append(bot)
                easygui.msgbox("Chatbot configuration loaded successfully!")
            except FileNotFoundError:
                easygui.msgbox("File not found. Please try again with a valid filename.")
            except json.JSONDecodeError:
                easygui.msgbox("Invalid configuration file. Please make sure the file contains valid JSON.")
        elif choice == "Quit":
            easygui.msgbox("Exiting the Chatbot Maker...")
            break
        else:
            easygui.msgbox("Invalid choice")

if __name__ == "__main__":
    main()
