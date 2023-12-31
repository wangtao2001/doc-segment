import pdfplumber
import docx
import os


def load_pdf(path):
    contents = []
    x0, top, x1, bottom = 0, 0.07, 1, 0.92
    with pdfplumber.open(path) as pdf:

        for _, page in enumerate(pdf.pages):
            bbox = (
                x0 * float(page.width), top * float(page.height), x1 * float(page.width), float(bottom * page.height))
            page = page.within_bbox(bbox)

            content = page.extract_text_simple()
            for c in content.split(' \n'):
                c = c.replace("\n", "").strip()
                if c:
                    contents.append(c)
    return contents

def load_docx(path):
    contents = []
    doc = docx.Document(path)
    for para in doc.paragraphs:
        content = para.text.strip()
        if content:
            contents.append(content)
    return contents

def load_doc(path):
    os.system(f"libreoffice --headless --convert-to docx --outdir {'/'.join(path.split('/')[:-1])} {path}")
    os.system(f'rm {path}')
    return load_docx(path+'x')


def doc2text(path, save_path):
    if path.endswith('.pdf'):
        out = load_pdf(path)
    elif path.endswith('.docx'):
        out = load_docx(path)
    elif path.endswith('.doc'):
        out = load_doc(path)
    else:
        raise Exception('文件格式不支持')
    file_name = path.split('/')[-1].split('.')[0]
    with open(os.path.join(save_path, f'{file_name}.txt'), 'w', encoding='utf-8') as f:
        for line in out:
            f.write(line + '\n')