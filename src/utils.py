
from openai import OpenAI 
import yaml


def generate_translation(config, language):
    system_prompt = f"""
    You are a translator.
    Translate the yaml document into {language}.
    Return the exact same yaml format as input, without translating the keys, only translate values.
"""
    user_prompt = yaml.dump(config.translations)
    
    client = OpenAI(api_key=config.llm["api_key"])
    stream = client.chat.completions.create(
                model=config.llm["model_version"],
                messages=[
                    {"role": "user", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )
    return stream.choices[0].message.content

def reset_page_language(config, language, max_attempts=3):
    attempts = 0
    parsed_translation = None
    while attempts < max_attempts:
        #try:
        if True:
            updates = 0
            yaml_translation = generate_translation(config, language)
            parsed_translation = yaml.safe_load(yaml_translation)
            for k in config.translations.keys():
                if k in parsed_translation.keys():
                    parsed_translation[k] = config.translations[k]
                    updates += 1
            if updates == len(config.translations):
                break
        #except Exception as e:
        #    print(e)
        #    pass
        attempts += 1
    
    if parsed_translation:
        print("Successfully translated")
        config.translations = parsed_translation