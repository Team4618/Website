def htmlNavBarTab(text, is_selected, style):
   result =  '<div style="' + style + '" class="nav_tab_div ' + ("nav_tab_selected" if is_selected else "nav_tab_not_selected") + '" onclick="">\n'
   result += '\t<a class="nav_tab_text">' + text + '</a>\n'
   result += '</div>\n'
   return result

def htmlNavBar(pages):
   pass

# Load template.html
# replace "REPLACE WITH NAV TABS" & "REPLACE WITH CONTENT"

print(htmlNavBarTab("Home", True, "border-top-left-radius: 5px"))