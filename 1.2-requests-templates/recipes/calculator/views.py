from django.shortcuts import render
import copy

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def cook(request, meal: str):
    servings = int(request.GET.get('servings', 1))
    err = False
    recipe = None
    if servings < 1:
        err = True
    elif meal in DATA:
        recipe = copy.deepcopy(DATA[meal])
        for ingredient, amount in recipe.items():
            recipe[ingredient] = amount*servings

    context = {
        'is_error': err,
        'recipe': recipe,
    }

    return render(request, 'calculator/index.html', context)
