categories_list = [
    "Culture and Art",
    "Geography",
    "History",
    "Business",
    "Politics",
    "Science",
    # "War",
    "Religion and Philosophy",
    "Sport",
    "Games",
    "Technologies",
    "Machines and mechanisms",
    "Adult",
    "Gambling",
    #"Pharma"
]

obj_template = {
    '_time': None,
    'err': None,
    'res': None
}

model_name = "Text_classificator_net_40k.h5"
#weight_name = "Text_classificator_weights_600.h5"
token_name = "token_40k.pkl"

max_words = 40000

language_val_dict = {
    'ja': 3,
    'ar': 3,
    'zh-cn': 3,
    'uk': 5,
    'az': 5,
    'hu': 5,
    'ru': 6,
    'es': 7,
    'fr': 7,
    'de': 7,
    'pl': 5,
    'it': 7,
    'pt': 7
}
