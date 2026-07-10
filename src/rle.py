# name: Run Length Encoding
# prefix: rle
# ---
rle = [(x, len(list(c))) for x, c in groupby($1)]