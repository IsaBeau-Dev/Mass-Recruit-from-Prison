import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'steam_desc.txt')

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

def discord_to_steam(text):
    # Replace Discord formatting with Steam formatting
    text = text.replace('**', '[b]').replace('**', '[/b]')  # Bold
    text = text.replace('*', '[i]').replace('*', '[/i]')  # Italics
    text = text.replace('__', '[u]').replace('__', '[/u]')  # Underline
    text = text.replace('~~', '[strike]').replace('~~', '[/strike]')  # Strikethrough
    text = text.replace('||', '[spoiler]').replace('||', '[/spoiler]')  # Spoilers

    # Handle code blocks (Discord uses ``` tags)
    text = text.replace('```', '[code]').replace('```', '[/code]')

    # Handle block quotes (Discord uses > tags)
    text = text.replace('> ', '[quote]').replace('\n', '[/quote]\n')

    # Handle images (Discord uses direct URLs)
    # Note: Steam uses [img] tags, but Discord uses direct URLs, so this might need manual adjustment
    text = text.replace('', '[img]').replace('', '[/img]')

    # Handle lists (Discord uses - for bullet points)
    text = text.replace('- ', '[*]')  # Convert Discord bullet points to Steam list items

    # Handle URLs (Discord uses direct URLs)
    # Note: Steam uses [url] tags, but Discord uses direct URLs, so this might need manual adjustment
    text = text.replace('', '[url]').replace('', '[/url]')

    # Handle headers (Discord uses #, ##, ### for headers)
    text = text.replace('# ', '[h1]').replace('\n', '[/h1]\n')  # Steam h1 (largest header)
    text = text.replace('## ', '[h2]').replace('\n', '[/h2]\n')  # Steam h2 (second largest header)
    text = text.replace('### ', '[h3]').replace('\n', '[/h3]\n')  # Steam h3 (third largest header)

    return text

def read_steam_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            steam_text = file.read()
            discord_text = steam_to_discord(steam_text)
            return discord_text
    except FileNotFoundError:
        return "File not found. Please provide a valid file path."

def read_discord_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            discord_text = file.read()
            steam_text = discord_to_steam(discord_text)
            return steam_text
    except FileNotFoundError:
        return "File not found. Please provide a valid file path."

def convert_text_to_readme(text, format_type):
    if format_type == 'steam':
        discord_text = steam_to_discord(text)
        readme_text = discord_to_steam(discord_text)
    elif format_type == 'discord':
        steam_text = discord_to_steam(text)
        readme_text = steam_to_discord(steam_text)
    else:
        return "Invalid format type. Please provide 'steam' or 'discord'."
    return readme_text

# Example usage:
converted_text = read_steam_text_from_file(file_path)
print(converted_text)

# Example usage for README files:
readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
converted_readme_text = read_discord_text_from_file(readme_path)
print(converted_readme_text)

# Example usage for converting input text to README text:
input_text = "[b]Bold text[/b] and [i]italic text[/i]"
format_type = "steam"
readme_text = convert_text_to_readme(input_text, format_type)
print(readme_text)
