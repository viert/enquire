from prompt_toolkit.styles import Style


DEFAULT_STYLE = Style.from_dict({
    'separator': '#6C6C6C',
    'qmark': '#5F819D',
    'choice-selected': 'bold',
    'choice-unselected': '',
    'checkbox-selected': 'bold',
    'checkbox-unselected': '',
    'pointer': '#FF9D00 bold',
    'instruction': '',
    'answer': '#FF9D00 bold',
    'question': '#FFFFFF bold',
})
