from django import template

register = template.Library()

obscene = ['bad_word', 'редиска', 'superbadword']


@register.filter()
def censor(text):
    l_word = text.split()
    for i, word in enumerate(l_word):
        if word in obscene:
            l_word[i] = word[0] + '***'
    return ' '.join(l_word)