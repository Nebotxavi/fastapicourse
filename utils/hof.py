def find(function, items, *args):
        return next(filter(lambda i: function(i, *args), items), None)