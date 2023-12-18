from IPython.display import HTML as html_print
import math

bosluk = 13

def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)

def space(times):
    space_str = ""
    for n in range(times):
        space_str += "&nbsp;"
    return space_str

isim = "Azizhan"
star_space = space(len(isim) + bosluk-2)
star = star_space + "🌟"
html_output = star

# Print the top part of the pyramid
for n in range(len(isim) + 1):
    line = space(len(isim) - n + bosluk) + " ".join([isim[i] for i in range(n)])
    html_output += cstr(line, color='green') + "<br>"

# Determine the number of 🟫 symbols logarithmically
num_symbols = int(math.log(len(isim), 2))
for _ in range(num_symbols):
    html_output += space(len(isim) + bosluk-1) + "🟫" + "<br>"

html_print(html_output)
