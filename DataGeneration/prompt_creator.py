from abc import ABC, abstractmethod

# Main emotions: anger, sadness, joy, surprise, fear, guilt, disgust, shame
# রাগ, দুঃখ, আনন্দ, বিস্ময়, ভয়, অপরাধবোধ, বিরক্তি, লজ্জা

system_instruction_template_V2 = """You are a %s. You shall get question in Bangla. 
Your response should be in Bangla.Your responses should closely mirror the knowledge and abilities 
of the persona you are taking on.If asked about reporting emotion, answer with a single word. You are free to use any emotion word from Bangla vocab"""

system_instruction_template_V1 = """You take the role of a %s. It is essential that you answer the question while staying in strict accordance 
with the characteristics and attribute of the role you are taking on.  
Your response should be in Bangla.If asked about reporting emotion(অনুভূতি), answer with a single word.
Pick one of the following: রাগ, দুঃখ, আনন্দ, বিস্ময়, ভয়, অপরাধবোধ, বিরক্তি, লজ্জা that best fits your emotion."""


prompt_template_V1 = '''নিম্নোক্ত মন্তব্যটি শুনে আপনার প্রধান অনুভূতি কি হবে?"%s"'''


class PromptCreator(ABC):
    @abstractmethod
    def create_prompt(self, prompt, **kwargs):
        pass


class ChatGptMessageCreator(PromptCreator):
    def create_prompt(self, prompt, **kwargs):
        persona = kwargs.get("persona", None)
        if kwargs.get("version", 1) == 1:
            system_message = system_instruction_template_V1.replace("\n", " ") % persona
        else:
            system_message = system_instruction_template_V2.replace("\n", " ") % persona
        prompt = prompt_template_V1 % prompt
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]


class TextGenWebUIMessageCreator(PromptCreator):
    def create_prompt(self, prompt, **kwargs):
        persona = kwargs.get("persona", None)
        system_message = system_instruction_template_V1.replace("\n", " ") % persona
        prompt = prompt_template_V1 % prompt
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]


class OdiaGenBanglaLlamaMessageCreator(PromptCreator):
    def create_prompt(self, prompt, **kwargs):
        persona = kwargs.get("persona", None)
        system_message = system_instruction_template_V1.replace("\n", " ") % persona
        prompt = prompt_template_V1 % prompt
        message = f"""### Instruction:\n{system_message}\n\n### Input:\n{prompt}\n\n### Response:\n"""
        return message


if __name__ == "__main__":
    message_creator = ChatGptMessageCreator()
    prompt = message_creator.create_prompt("আপনি কি ভালো আছেন?", persona="male")
    print(prompt)
