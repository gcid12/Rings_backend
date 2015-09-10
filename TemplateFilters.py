from app import app

@app.template_filter()
def diablify(string): 
    return '666'+str(string)

@app.template_filter()
def nonone(val):
    if not val is None:
        return val
    else:
        return ''