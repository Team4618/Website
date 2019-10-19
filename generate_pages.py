import os
import time

#Utils
def readFile(path):
   f = open(path, "r")
   result = f.read()
   f.close()
   return result

def writeFile(path, text):
   f = open(path, "w")
   f.write(text)
   f.close()

def prettyIndentation(template, replace_text, raw_text):
   indentation = template[template.rfind("\n", 0, template.find(replace_text)) + 1 : template.find(replace_text)]

   result = ""
   lines = raw_text.split("\n")
   for line_i in range(len(lines)):
      result += ("" if line_i == 0 else indentation) + lines[line_i] + ("\n" if line_i != (len(lines) - 1) else "")

   return result

#HTML generation stuff
def htmlNavBarTab(text, is_selected, style, link):
   result =  '<div' + ((' style="' + style + '"') if len(style) > 0 else "") + ' class="nav_tab_div ' + ("nav_tab_selected" if is_selected else "nav_tab_not_selected") + '"' + ((" onclick=\"window.location.href='" + link + "'\"") if len(link) > 0 else "") + '>\n'
   result += '\t<a class="nav_tab_text">' + text + '</a>\n'
   result += '</div>\n'
   return result

def htmlNavBar(pages, current_page):
   result = ""
   for i in range(len(pages)):
      page = pages[i]
      result += htmlNavBarTab(page["title"], page["title"] == current_page, "border-top-left-radius: 5px" if i == 0 else "", "/generated/" + page["title"] + ".html")
   return result[:-1] #NOTE: removes the trailing newline so it looks nicer

def generatePage(template_html, title, nav_tabs_raw, content_raw):
   nav_tabs = prettyIndentation(template_html, "<!-- REPLACE WITH NAV TABS -->", nav_tabs_raw)
   content = prettyIndentation(template_html, "<!-- REPLACE WITH CONTENT -->", content_raw)

   return template_html.replace("<!-- REPLACE WITH TITLE -->", "<title>" + title + "</title>").replace("<!-- REPLACE WITH NAV TABS -->", nav_tabs).replace("<!-- REPLACE WITH CONTENT -->", content)

#Page specification & generation
def makePage(title, content):
   if isinstance(content, str):
      return {"title": title, "content": (lambda: readFile(content)), "path": content}
   else:
      assert callable(content)
      return {"title": title, "content": content}

def generate(get_template_html, pages):
   template_html = get_template_html()
   for page in pages:
      writeFile("generated/" + page["title"] + ".html", generatePage(template_html, "Newman Robotics - " + page["title"], htmlNavBar(pages, page["title"]), page["content"]() ))

#live regen stuff
def getWatchFiles(pages):
   watch_files = []
   for page in pages:
      if "path" in page:
         path = page["path"]
         watch_files.append({"path": path, "timestamp": os.stat(path).st_mtime})
   return watch_files

def checkFiles(watch_files):
   result = False
   for f in watch_files:
      timestamp = os.stat(f["path"]).st_mtime
      if timestamp != f["timestamp"]:
         result = True
         f["timestamp"] = timestamp
   return result

#--------------------------
template_html = lambda: readFile("template.html")
pages = [
   makePage("Home", "content/home_content.html"), 
   makePage("Sponsors", "content/sponsors_content.html"), 
   makePage("Blog", "content/blog_content.html"), 
   makePage("Robots", "content/robot_content.html"), 
   makePage("Gallery", "content/gallery_content.html")
   # makePage("Gallery", lambda: generateGallery()) #TODO: automatically generate gallery content
]

watch_files = getWatchFiles(pages)

gen_count = 0
generate(template_html, pages)
while True:
   if checkFiles(watch_files):
      gen_count += 1
      print("Generating " + str(gen_count))
      generate(template_html, pages)
   time.sleep(0.5)