from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    unwanted_words = ['редиска', 'плохое слово', 'еще слово']  # Список нежелательных слов
    for word in unwanted_words:
        value = value.replace(word, '*' * len(word))
    return value