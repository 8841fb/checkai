import prodia

from helpers.config import PRODIA_API_KEY


class Prodia_Client:
    def __init__(self):
        prodia.Client(api_key=PRODIA_API_KEY)

    async def generate(self, prompt):
        image = await prodia.arunv1(prompt=prompt)
        return image
