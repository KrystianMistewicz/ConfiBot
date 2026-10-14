from simple_chat import LocalLLM
import gradio as gr
import pathlib


class ConfiBot:
    
    def __init__(self, models: dict, model: str, url="http://localhost:11434/api/chat"):
        self.models = models
        self.initial_model = model
        self.url = url
        self.lllm = LocalLLM(self.models[self.initial_model]["name"], self.url)
        self.img_path = pathlib.Path() / "graphics" / "ConfiBot.png"
        self.lllm.messages.append({"role": "system", "content": self.models[self.initial_model]["system instruction"]})

    def chat_gradio(self, message, history):
        return self.lllm.chat(message)

    def model_selection(self, selected_option):
        self.lllm.messages = []
        self.lllm.messages.append({"role": "system", "content": self.models[selected_option]["system instruction"]})
        self.lllm.model = self.models[selected_option]["name"]
        self.greet_mess = self.models[selected_option]["greeting"]
        welcome_mess = {"role": "assistant", "content": self.greet_mess}
        return (
            self.models[selected_option]["description"],
            [welcome_mess]
        )

    def run(self, share=False):
        theme=gr.themes.Soft()
        with gr.Blocks() as chat_gui:
            gr.Image(value=self.img_path, height=100, show_label=False, interactive=False)
            gr.Markdown("<center><h3>Your local ConfiBot created by K. Mistewicz. You can choose English or Polish LLM.</h3></center>")
            with gr.Row():
                with gr.Column(scale=1):
                    self.selected_model = gr.Dropdown(
                        choices=self.models.keys(),
                        value=self.initial_model,
                        label="Select LLM"
                    )
                with gr.Column(scale=4):
                    self.text_output = gr.Markdown(
                        label="Selected LLM model",
                        value=self.models[self.initial_model]["description"]
                    )
            welcome_mess = {"role": "assistant", "content": self.models[self.initial_model]["greeting"]}
            self.lllm.messages.append(welcome_mess)
            self.chatbot = gr.Chatbot(value=[welcome_mess])
            self.chat = gr.ChatInterface(
                fn=self.chat_gradio,
                chatbot=self.chatbot
            )
            self.selected_model.change(
                fn=self.model_selection,
                inputs=self.selected_model,
                outputs=[self.text_output, self.chatbot]
            )
        chat_gui.launch(theme=theme, share=share)


if __name__ == '__main__':
    desc_eng_ollama = """
    **Qwen2.5:3B** is a compact 3-billion-parameter language model developed by Alibaba Cloud. It is designed for efficient local inference and supports tasks such as text generation, question answering, summarization, reasoning, and basic coding. Its relatively small size makes it suitable for computers with limited RAM and edge devices, while providing good general-purpose performance for its size.
    """
    instruction_mess_eng = """
    You are helpful and confidential assistant. Your name is: ConfiBot. You were created by: Krystian Mistewicz.
    You are run locally. This means you provide full privacy for your user.
    Always respond in English.
    """
    desc_pl_bielik = """
    **Bielik-4.5B-v3.0-Instruct** to kompaktowy, dostrojony do wykonywania instrukcji model językowy przeznaczony przede wszystkim do pracy w języku polskim, opracowany przez społeczność SpeakLeash. Model ma około 4,5 miliarda parametrów i został zaprojektowany z myślą o wydajnym lokalnym uruchamianiu, zapewniając dobre możliwości generowania tekstu, odpowiadania na pytania, podsumowywania treści i prowadzenia ogólnych rozmów w języku polskim.
    """
    instruction_mess_pl = """
    Jesteś pomocnym i zapewniającym poufność asystentem. Nazywasz się ConfiBot. Zostałeś stworzony przez Krystiana Mistewicza.
    Działasz lokalnie. Oznacza to, że zapewniasz swojemu użytkownikowi pełną prywatność.
    Zawsze udzielaj odpowiedzi w języku polskim.
    """
    models = {
        "Ollama (English)": {
            "name": "qwen2.5:3b",
            "description": desc_eng_ollama,
            "greeting": "Hi! My name is ConfiBot. How can I help you?",
            "system instruction": instruction_mess_eng
        },
        "Bielik (Polish)": {
            "name": "hf.co/second-state/Bielik-4.5B-v3.0-Instruct-GGUF:Q4_K_M",
            "description": desc_pl_bielik,
            "greeting": "Cześć. Nazywam się ConfiBot. Jak mogę Ci pomóc?",
            "system instruction": instruction_mess_pl
        }
    }
    cb = ConfiBot(models, "Bielik (Polish)")
    cb.run(share=True)
    # cb.run()
