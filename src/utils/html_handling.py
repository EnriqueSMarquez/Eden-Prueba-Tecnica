from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n")
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    clean_text = "\n".join(lines)
    
    clean_text = clean_text.replace(u'\xa0', u' ')
    
    return clean_text