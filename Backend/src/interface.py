#src/interface.py
"""
This module contains the `get_html` function that generates the custom HTML and CSS 
for styling the chatbot interface.

The `get_html` function provides a set of CSS rules to style the chatbot interface 
in a clean and responsive way. It sets up the layout for the chatbot container, 
user input area, and the messages displayed in the chat.

It is intended to be used in conjunction with a Gradio-based chatbot application 
to give it a professional and consistent look.

Functions:
- `get_html`: Returns the HTML and CSS code used for the custom styling of the chatbot interface.
"""
def get_html():
    """
    Returns the HTML and CSS code that defines the custom styling for the chatbot interface.

    This function provides the necessary CSS to style the chatbot interface, including 
    layout, colors, fonts, and positioning of elements like the chat container, input field, 
    and buttons. The CSS is returned as a string which can be embedded in the Gradio app for 
    customizing the visual appearance of the chatbot.

    Returns:
        str: The HTML and CSS code for styling the chatbot interface.
    """
    return """
<style>
    body, html {
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif;
    }

    .gradio-container {
        width: 100% !important;
        max-width: none !important;
        height: 90vh !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #f7f7f8 !important;
    }

    #main_container {
        display: flex;
        flex-direction: column;
        height: 90vh;
        max-width: 1000px;
        margin: 0 auto;
        background: white;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }

    #header {
        padding: 0px 0px;
        background: white;
        border-bottom: 0px solid #e5e5e6;
        z-index: 10;
    }

    #chat_container {
        flex: 1;
        overflow-y: auto;
        padding: 0 20px;
        background: #f7f7f8;
        display: flex;
        flex-direction: column;
    }

    #chatbot {
        height: 70vh !important;
        padding: 1px 0;
        margin: 0;
    }

    #chatbot .user, #chatbot .bot {
        max-width: 100%;
        padding: 15px 25px;
        margin-bottom: 5px;
        font-size: 13px;
        line-height: 1;
        overflow-wrap: break-word;
        word-break: break-word;
        white-space: pre-wrap;
        display: inline-block;
        border-radius: 20px;
        background: #e9ecef;
    }

    #input_container {
        padding: 15px 20px;
        background: white;
        border-top: 1px solid #e5e5e6;
        position: sticky;
        bottom: 0;
        display: flex;
        align-items: center;
    }

    #query_input {
        flex-grow: 1;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 16px;
        border: 1px solid #ccc;
        width: 100%;
    }

    #submit_button {
        margin-left: 10px;
        padding: 6px 12px;
        border-radius: 8px;
        background-color: #007bff;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 14px;
        height: 65px;
        min-width: 85px;
        max-width: 85px;
        text-align: center;
    }

    #chatbot::-webkit-scrollbar {
        width: 8px;
    }

    #chatbot::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    #chatbot::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }

    @media (min-width: 1600px) {
        #main_container {
            max-width: 1400px;
        }

        #chatbot {
            min-height: 80vh !important;
            max-height: 80vh !important;
        }
    }
</style>
"""
