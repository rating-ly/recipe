import json

def generateHTML(js):
    
    html_content = ""

    head = "<head><title>"+js['description']+"</title></head>"

    html_content +=head

    html_content += "<body>"

    title = "<h1>"+js['description']+"</h1>"
    html_content += title


    image = "<img src="+ js['image'] + ">"
    html_content += image

    html_content += "</body>"

    html_content += "<br/><br/><br/><br/><br/><br/>"
    html_content += json.dumps(js, sort_keys=True, indent=2, separators=(',<br/>', ': '))

    return html_content






