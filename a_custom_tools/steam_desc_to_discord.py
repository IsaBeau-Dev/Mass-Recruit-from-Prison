file_path = r"secret"


def steam_to_discord(text):
    # Replace Steam formatting with Discord formatting
    text = text.replace('[b]', '**').replace('[/b]', '**')  # Bold
    text = text.replace('[i]', '*').replace('[/i]', '*')  # Italics
    text = text.replace('[u]', '__').replace('[/u]', '__')  # Underline
    text = text.replace('[strike]', '~~').replace('[/strike]', '~~')  # Strikethrough
    text = text.replace('[spoiler]', '||').replace('[/spoiler]', '||')  # Spoilers

    # Handle code blocks (Steam uses [code] tags)
    text = text.replace('[code]', '```').replace('[/code]', '```')

    # Handle block quotes (Steam uses [quote] tags)
    text = text.replace('[quote]', '> ').replace('[/quote]', '')

    # Handle images (Steam uses [img] tags)
    text = text.replace('[img]', '').replace('[/img]', '')  # Remove image tags

    # Handle lists (Steam uses [list] and [*] tags)
    text = text.replace('[list]', '').replace('[/list]', '')  # Remove list tags
    text = text.replace('[*]', '- ')  # Convert list items to Discord bullet points

    # Handle URLs (Steam uses [url] tags)
    text = text.replace('[url]', '').replace('[/url]', '')  # Remove URL tags

    # Handle headers (Steam uses [h1], [h2], [h3] tags)
    text = text.replace('[h1]', '# ').replace('[/h1]', '')  # Discord h1 (largest header)
    text = text.replace('[h2]', '## ').replace('[/h2]', '')  # Discord h2 (second largest header)
    text = text.replace('[h3]', '### ').replace('[/h3]', '')  # Discord h3 (third largest header)

    return text

def read_steam_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            steam_text = file.read()
            discord_text = steam_to_discord(steam_text)
            return discord_text
    except FileNotFoundError:
        return "File not found. Please provide a valid file path."

# Example usage:
converted_text = read_steam_text_from_file(file_path)
print(converted_text)