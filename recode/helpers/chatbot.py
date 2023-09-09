import openai
from helpers.config import OPENAI_API_KEY


class OpenAI:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    async def generate(self, prompt):
        system_prompt = 'Ahora eres un bot llamado CheckAI, inetnta no actuar como un bot, intenta actuar como un humano, estas hablando ahora con un humano, no con un bot.'

        prompt = f'{system_prompt}\n\nUsuario: {prompt}\nCheckAI: (acuerdate de no mandar como esto, solo responde a lo que te diga el humano sin este formato)'

        response = await openai.Completion.acreate(
            engine='text-davinci-003',
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
        )

        # Return the generated text
        return response['choices'][0]['text']
