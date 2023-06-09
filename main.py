# pip install openai fpdf pygments
import openai
from fpdf import FPDF
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

directory = "YOUR_FILE_SAVE_DIRECTORY/"
openai.api_key = "YOUR_API_KEY
# Download Dejavu Fonts for better coverage of non-ascii characters
# Download -> https://dejavu-fonts.github.io/Download.html 
font_directory = "DIRECTORY_FOR_/DejavuSans.ttf"

def chat_completion(param, quantity):
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': ''},
            {'role': 'user', 'content': 'Give me a '+str(quantity)+' question hard level - exam regarding the following subject (Give me various types of questions, but dont explicity state the type of question, just give me the questions), and give me the answers at the end : ' + param}
        ],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']

# If coding subject, HTML file for Syntax Highlighting
def save_html(ans, subject, language):
    lexer = get_lexer_by_name(language)
    html_content = highlight(ans, lexer, HtmlFormatter(full=True, noclasses=True))
    html_address = directory + subject + "_GPTQuiz.html"
    with open(html_address, "w") as html_file:
        html_file.write(html_content)

# If not coding subject, regular PDF file
def save_pdf(ans, subject):
    pdf_address = directory + subject + "_GPTQuiz.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", style="", fname=font_directory)
    pdf.set_font("DejaVu", size=8)
    pdf.multi_cell(0, 10, txt=ans)
    pdf.output(pdf_address)

n = int(input("Enter the number of subjects >> "))

subs = []
quants = []
lang = ['x' for _ in range(n)]

for i in range(n):
    print("\n")
    temp1 = input(f'Subject {i + 1} >> ').strip()
    k = input("\nIf programming subject, Enter language \nIf not, type x\n>> ").strip()
    lang[i] = k
    temp2 = int(input("\nNumber of questions >> "))
    subs.append(temp1)
    quants.append(temp2)
print("\n")
for i in range(n):
    if lang[i] == 'x':
        print(f'PDF File Generating ... {i+1}/{n}')
        save_pdf(chat_completion(subs[i],quants[i]),subs[i])
    else:
        print(f'HTML File Generating ... {i+1}/{n}')
        save_html(chat_completion(subs[i],quants[i]),subs[i],lang[i])

print("Process Finished")
