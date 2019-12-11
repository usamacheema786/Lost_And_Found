item_schema = {
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'location': {'type': 'string'},
        'date': {'type': 'string'},
    },
    'required': ['name', 'category', 'location', 'date']
}
user_schema = {
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string','minLength': 6 }
    },
    'required': ['email', 'password']
}